class IterableToAwait:
    """
    Wrap a iterable so it can be awaited
    """

    def __init__(self, iterable: Iterable):
        self.iterable = iterable

    def __await__(self):
        return (yield from self.iterable)


class Coroutine:
    """
    Coroutine abstraction around native coroutine and generator functions.
    This class implements __iter__ and __await__ interfaces so its instances
    can be used after yield/yield from/await syntax. It shares attributes
    with its manager object for better code reuse. To pass argument to actual
    coroutine object it produces, set the attributes via __init__ or __call__.

    The concrete implemntation MUST overide either __iter__ in yield style or
    await_impl in await style, or one can overide both.
    """

    def __init__(self, manager: "Manager" = object()):
        """
        Parameters
        ----------
        manager : Manager
            A coroutine Manager shares attributes with the Coroutine object
        """
        self.set_manager(manager)

    @Builder.method
    def set_manager(self, manager: "Manager" = object()):
        """
        Set coroutine manager. A Coroutine object shares and mutates
        attributes from a coroutine manager, this makes multiple Coroutine
        used by the same coroutine manager more reusable.

        Parameters
        ----------
        manager : Manager
            A coroutine Manager may register multiple Coroutine that function exactly
            the same, and choose compatible one based on the session object of the
            Manager. To avoid repeating ourself, the coroutine objects should access
            resource from the shared Manager object. Thus, Coroutine object is always
            coupled with a Manager object, and it only uses attributes from the manager
            object, and doesn't create its own.
        """
        self.manager = manager

    def __getattr__(self, k):
        """Use everything from coupled manager object"""
        try:
            return self.manager.__getattribute__(k)
        except AttributeError:
            return self.manager.__getattr__(k)

    def __await__(self):
        """
        Return itself as an iterator, to be used in await syntax directly.
        Concrete implementation only has to replace await_impl.
        """
        # First wrap self.await_impl in a native coroutine object,
        # then use its __await__ method, to avoid
        # __await__() returned a coroutine error
        # see https://stackoverflow.com/a/33420721
        return await_wrap(self).__await__()

    async def await_impl(self):
        """
        Actual coroutine implementation used in await syntax,
        Default to await itself, by returning itself as an iterator, works
        when __iter__ is defined. Since default __iter__ use
        self.await_impl, the base doesn't work out of the box.
        """
        # Default to using self as iterable, wrap it in IterableToAwait
        # so it can be awaited
        await IterableToAwait(self)

    def __iter__(self):
        """
        Actual coroutine implementation used in yield syntax
        Default to yield from await_impl. Since default await_impl uses
        self.__iter__, the base doesn't work out of the box.
        """
        yield from self.await_impl().__await__()


class ForkedObject(NamedTuple):
    """
    Manage the objects created when using fork, useful when calling
    terminate()

    Attributes
    ----------
    coro:
        The actual generator or native coroutine object
    forked:
        Object created by testing framework specific fork interface

    """

    coro: Union[typing.Generator, typing.Coroutine]
    forked: Any


class Terminator:
    @classmethod
    def method(cls, func: Callable):
        def wrap(*args, **kwargs):
            self: Manager = args[0]
            logger.debug(f"Terminate Manager {self}")
            func(*args, **kwargs)
            self.close_forked()

        return wrap


class Manager:
    """
    Coroutine Manager provides interfaces to link, create Coroutine object.
    A coroutine object will register a Manager object and accesses, operates
    on its attribute as if they are its own.

    Attributes
    ----------
    session : gzsim.session.Session
        simulation session
    event_mgr: gzsim.event.Manager
        event manager
    forked: Set[ForkedObject]
        A set of forked background generator/coroutine objects. Any
        background coroutines created by the manager should be put in
        the set so they can be handled, terminated by the manager.
    """

    def __init__(self, session: "Session"):
        """
        Parameters
        ----------
        session : gzsim.session.Session
            simulation session
        """
        self.session = session
        self.event_mgr = session.event_manager_factory()
        self.forked: Set[ForkedObject] = set()
        self.terminate_monitors = []

    @Builder.method
    def set_terminate_monitor(
        self, monitor: "gzsim.coroutine.terminate.Terminate"
    ):
        """
        Add monitor to terminate monitors list, and set self to one of
        the target of the terminate monitor. A
        """
        self.terminate_monitors.append(monitor)
        monitor.set_targets([self])

    def register_event(self, name: str) -> None:
        event = self.event_mgr.local_events.get(name)
        if event is not None:
            setattr(self, name, event)

    def register_events(self) -> None:
        """Register events as attributes"""
        for k, v in self.event_mgr.local_events.items():
            setattr(self, k, v)

    def fork(self, coro: Coroutine) -> ForkedObject:
        """
        Fork a Coroutine in the background, add generator/coroutine
        objects created by it to forked list.
        """
        logger.debug(f"fork coroutine {coro} to event loop")
        event_loop = self.session.event_loop_factory()
        coro_obj = coroutinewrap(coro)
        forked_obj = event_loop.fork(coro_obj)
        obj = ForkedObject(coro_obj, forked_obj)
        self.forked.add(obj)
        return obj

    def close(self, forked_obj: ForkedObject) -> None:
        if not forked_obj in self.forked:
            logger.warning(f"The forked object {forked_obj} does not exist")
            return
        try:
            forked_obj.coro.close()
        except ValueError:  # ValueError?
            logger.warning()

        try:
            forked_obj.forked.close()
            forked_obj.forked.kill()
        except AttributeError:
            logger.warning(
                f"Forked {forked_obj.forked} coroutine has no kill() interface, "
                ", moving on"
            )
        self.forked.discard(forked_obj)
        logger.debug(f"Closed forked object {forked_obj}")

    def close_forked(self) -> None:
        """
        Close all background coroutine forked by the manager stored
        in the list forked.
        """
        for c in copy.copy(self.forked):
            self.close(c)
        self.forked.clear()

    @Terminator.method
    def terminate(self) -> None:
        """
        Default implementation of terminate interface, will be called
        by terminate monitor stored in terminate_monitors when terminate
        conditions are satisfied
        """
        self.close_forked()

    @property
    def forkable(self) -> Optional[Callable]:
        """
        Return the coroutine method that can be passed to EventLoop.fork
        If not overidden, return None

        Examples
        --------
        .. code-block::

            class Foo(Driver):
                @Driver.coroutine
                def bar(self):
                    pass

                def forkable(self):
                    # Mark method bar as forkable
                    self.bar

        """
        return None


class Callable(Coroutine):
    """
    Coroutine that implements __call__.
    A coroutine manager will keep only an instance of such Coroutine object,
    and return this object in its coroutine methods.
    To support argument passing, implement __call__, so that
    Ex:
        coro = SharedState()
        # __iter__ will use attributes set by __call__ to achieve
        # argument passing
        yield from coro(*args, **kwargs)
    """

    def __call__(self):
        """
        Setting attributes, so they can be used in __await__, __iter__
        calls
        """
        return self


def yield_wrap(coro: Coroutine):
    """
    Create generator object as coroutine from a Coroutine object
    """
    yield from coro


async def await_wrap(coro: Coroutine):
    """
    Create native coroutine object as coroutine from a Coroutine object,
    by awaiting on its await_impl method.
    """
    await coro.await_impl()


def coroutinewrap(coro: Coroutine) -> Union[typing.Generator, typing.Coroutine]:
    """
    Wrap Coroutine object in native coroutine or generator object
    """
    # registered Coroutine manager should have a session registered
    coro_style = coro.manager.session.event_framework.coro_style
    # TODO (enho.shen): BOTH should be removed
    if coro_style == CoroStyle.BOTH:
        return yield_wrap(coro)
    if coro_style == CoroStyle.YIELD:
        return yield_wrap(coro)
    if coro_style == CoroStyle.AWAIT:
        return await_wrap(coro)


def coroutineswrap(coros: List[Coroutine]):
    """
    Wrap list of Coroutine objects in native coroutine or generator object
    """
    return [coroutinewrap(c) for c in coros]


def coroutinemethod(orig):
    """
    Decorate method of a Manager as a coroutine that returns a Coroutine
    object. When called, the Coroutine object will be wrapped in function
    to produce generator or native coroutine object so they can actually
    be used as coroutine.
    """

    def wrap(*args, **kwargs):
        self = args[0]
        coro_style = self.session.event_framework.coro_style
        coro = orig(*args, **kwargs)
        return coroutinewrap(coro=coro, coro_style=coro_style)

    return wrap


class GeneralCoroutine(Coroutine):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        if inspect.isgeneratorfunction(self.func):
            yield from self.func(*self.args, **self.kwargs)
        else:
            yield from self.await_impl().__await__()

    async def await_impl(self):
        if inspect.isgeneratorfunction(self.func):
            await IterableToAwait(self.func(*self.args, **self.kwargs))
        else:
            await self.func(*self.args, **self.kwargs)


def to_coroutine(func):
    """
    A decorator that wrap a generator or async function to a ``Coroutine`` object.

    Example
    -------
    @coroutine.to_coroutine
    def gen_function(value):
        yield value
        yield 123
        yield 456

    def mock_yield_wrap(coro: Coroutine):
        yield from coro

    coro = gen_function(111)
    yield_wrap = mock_yield_wrap(coro)

    assert yield_wrap.send(None) == 111
    assert yield_wrap.send(None) == 123
    assert yield_wrap.send(None) == 456
    """

    def wrap(*args, **kwargs):
        return GeneralCoroutine(func, *args, **kwargs)

    return wrap


class Event:
    @property
    def yieldable(self) -> Optional[Any]:
        """
        Return yieldable object used by the event queue
        Return None if yieldable handle is not supported
        """
        return None

    @property
    def awaitable(self) -> Optional[Any]:
        """
        Return awaitable object used by the async await
        Return None if awaitable handle is not supported
        """
        return None

    def _native_await(self):
        """Use this in ``__await__`` if self.awaitable supports ``__await__``"""
        return self.awaitable.__await__()

    def _native_iter(self):
        """
        Default behavior yield from support used in ``__iter__``, simply yield
        self.yieldable
        """
        yield self.yieldable

    def _await_from_iter(self):
        """
        used in __await__ and return self as the iterator, when __iter__
        has already been defined
        """
        return (yield from self)

    def __await__(self):
        """
        Magic method for await keyword
        used for await coroutine style simulation
        Default to ``_await_from_iter``, where yieldable thus ``__iter__`` are
        implemented
        """
        return self._await_from_iter()

    def __iter__(self):
        """
        Magic method for yield from keyword
        used for generator style coroutine simulation
        Default to ``_native_iter``, where yieldable is implemented
        """
        yield from self._native_iter()
