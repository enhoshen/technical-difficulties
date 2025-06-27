# The "I don't know where to put them" topics

<!--toc:start-->

- [The "I don't know where to put them" topics](#the-i-dont-know-where-to-put-them-topics)
  - [The self argument of bound method called by other objects](#the-self-argument-of-bound-method-called-by-other-objects)
  - [subscription of np array](#subscription-of-np-array)
  <!--toc:end-->

## The self argument of bound method called by other objects

Let's see the following code:

```python
class A:
    def __init__(self):
        self.a = 12

    def action(self):
        self.a = 34


>>> a = A()
>>> a.a
12
>>> b = A()
>>> b.action = a.action
>>> b.action()
>>> b.a
12
>>> a.a
34
```

We know the first argument of a method is the `self` object, it might be intuitive to think that when calling `b.action()`, the `self` object would be `b`.

This behavior is called `bound method`, where a method is assoiciated with the instance of the class in which they are defined. How is it done? We need to look at the special attribute `__self__`.

> When an instance method object is created by retrieving a user-defined function object from a class via one of its instances, its **self** attribute is the instance

So for a bound method, the `self` object is not whatever object calling it, but the object recorded in the special attribute `__self__`.

```python
>>> id(b)
140135618006848
>>> id(a)
140135618010064
>>> id(b.action.__self__)
140135618010064
```

Overall, I wouldn't recommand doing such questionable attribute manipulation, it may applies to attribute overide in general.

Ref: [Instance methods](https://docs.python.org/3/reference/datamodel.html)

## subscription of np array

Slicing are tuple of slice or int. When we write `a[0, 1, 2:3]`, it equals `a[(0, 1, slice(2,3))]`.
You might think a list of iterable can be used in place of tuple but not quite:

- unpack arguments: syntax error, subscription (square bracket) does not work like
  function call

  ```python
  slicing = [0, 1, slice(2,3)]
  a[*slicing]

  ```

- list: this is called fancy indexing with list of integer. It also can be a list
  of booleans acting like a mask
  ```python
  a = [[0,1], [2,3]]
  a[[0, 0]] == [[0,1], [0,1]]
  ```

```

```
