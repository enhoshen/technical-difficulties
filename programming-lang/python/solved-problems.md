# Problem encountered and solved in Python

<!--toc:start-->

- [Problem encountered and solved in Python](#problem-encountered-and-solved-in-python)
  - [Shareing attributes with both getattr and getattribute](#shareing-attributes-with-both-getattr-and-getattribute)
  - [Descriptor as decorator to achieve classmethod as decorator that alters class attribute](#descriptor-as-decorator-to-achieve-classmethod-as-decorator-that-alters-class-attribute)
  - [Regsiter class as factory method in class definition with classmethod decorator](#regsiter-class-as-factory-method-in-class-definition-with-classmethod-decorator)
  - [Don't use empty list as default argument](#dont-use-empty-list-as-default-argument)
  <!--toc:end-->

## Shareing attributes with both getattr and getattribute

## Descriptor as decorator to achieve classmethod as decorator that alters class attribute

```python
class Base:
    cls_attr = None
    @classmethod
    def decor(cls, func):
        def wrap(cls, wrapped_cls):
            # work on cls.cls_attr
            ...
            return wrapped_cls
        return wrap


class Foo(Base):
    @Base.decor
    def method(*args, **kwargs):
        ...

#TypeError: wrap() missing 1 required positional argument: 'wrapped_cls'
@Foo.method
class Bar(Yield):
    ...
```

`@Foo.method` equals to `wrap`, and it is not called by `Foo` as if doing `@Foo.wrap`,
making it unable to reference the `Foo` class.

If we change the `wrap` function signature to eliminate the error:

```python
class Base:
    cls_attr = None
    @classmethod
    def decor(cls, func):
        def wrap(wrapped_cls):
            # work on cls.cls_attr
            return wrapped_cls
        return wrap


class Foo(Base):
    @Base.decor
    def method(*args, **kwargs):
        ...

@Foo.method
class Bar(Yield):
    ...
```

Now there is no error, but you can see that Foo is still not referenced
in `wrap`, meaning that the `cls` of `cls.cls_attr` is from the `Base` class,
thus breaking all the subclasses, unwanted sharing of mutable class attributes
among base and derived classes.

Solution is to write a `Descriptor` class just like `@classmethod`.

```python
class decormethod(object):
    def __init__(self, method):
        self.method = method

    def __get__(self, instance, cls):
        def wrap(wrapped_cls):
            # work on cls.cls_attr
            return wrapped_cls
        return wrap

class Base:
    cls_attr = None
    ...

class Foo(Base):
    @decormethod
    def method(*args, **kwargs):
        ...

@Foo.method
class Bar:
    ...
```

Now, the `cls_attr` of `Base` will not be undesirably altered by the classmethod
decorator of the subclass `Foo`.

## Regsiter class as factory method in class definition with classmethod decorator

```python
class Foo:
    factory = None

    def __init__(self):
        self.register_objects()

    @classmethod
    def register_factory(cls, wrapped: Callable):
        if cls.factory is None:
            cls.factory = []
        cls.factory.append(wrapped)

    def register_objects(self, *args, **kwargs) -> None:
        self.object = [fac(*args, **kwargs) for fac in self.factory]

@Foo.register_factory
class Factory:
    def __init__(*args, **kwargs):
        ...

@Foo.register_factory
def factory_func(*args, **kwargs):
    ...
```

## Don't use empty list or any mutable object as default argument

All instances will reference to the same list object as the argument,
if it is directly assigned to an attribute, the attribute points to
the same list across all instances, any changes to the list will be
shared across all instances.
This is mentioned specifically in the
[offical doc](https://docs.python.org/3/reference/compound_stmts.html#function-definitions):

> Default parameter values are evaluated from left to right when the
> function definition is executed

```python
class Foo:
    def __init__(self, l=[]):
        self.l = l
a, b = Foo(), Foo()
# True
a.l is b.l
```

We know what to do: use `None` as default arguments

```python
class Foo:
    def __init__(self, l=None):
    self.l = l
    if l is None:
        self.l = []
```

Be aware, not just list/dict, your user defined classes and their instances
are no exception. In dataclass this feels intutive to do but to be safe,
use None.

```python
# Even if Bar only has immutable attributes
@dataclass
class Bar:
    a: str = ""

class Foo:
    def __init__(self, arg=Bar()):
        self.arg = arg
a, b = Foo(), Foo()
a.arg.a = "123"
# True
assert b.arg.a == "123"
```
