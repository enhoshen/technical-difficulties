# Problem encountered and solved in Python

## Unwanted sharing of mutable class attributes among base and derived classes

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
thus breaking all the subclasses.  

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
