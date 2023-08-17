# Oversights encountered when writing tests 

<!--toc:start-->
- [Oversights encountered when writing tests](#oversights-encountered-when-writing-tests)
  - [Didn't Test the most obvious](#didnt-test-the-most-obvious)
  - [Write unit test as if writing a library](#write-unit-test-as-if-writing-a-library)
  - [False sense of correctness](#false-sense-of-correctness)
<!--toc:end-->

## Didn't Test the most obvious
Sometimes I write unit-tests starting with edge cases when the regular behavior is very unlikely to go wrong. And then it will be exactly what goes wrong. 

### In short
* Write your test starting from the most basic behavior
* Test every conditions

### example
```python
def foo(option: int) -> str:
    if option == 0:
        return 'success'
    # normal behavior missing
    # return f"error code {option}"

def test_foo():
    # start unit-test from special cases
    assert foo(0) == 'success'
    # forget to test the normal behavior
    # n = random.randint(0, 10)
    # assert foo(n) == f"error code {n}"
```

## Write unit test as if writing a library
Sometimes I see tests iterating through all kinds of situations parametrically. From personaly experience, hard-coded simple test case is more preferrable than complex general test cases, if iterating through range/set of parameters doesn't provide more coverage. 

Test should help you find the problem in your code, if the test itself is too complex you have to debug your test, it is actually producing problems and failing its job. 

When writing test configurations, I'd like to start with thinking the situation when that configuration **fails** and if that helps me pinpoint the problem. If two sets of configurations both fails and provide the same set of diagonistics/coverage of the problem, I only need one of them.

Simple hard-coded test case provides some advantages:
* You immediately see the parameters used when the test fails
* When writing test you have to provide golden/answer, if the answer is hard to come by yourself because of complex configurations, you may spend time debugging your golden than your design under test
* Tests don't test themself, a general parametric test is less likely to guartee their own correctness

### In short
* Use simple configuration you can easily acquire golden from when writing unit-test
* Hard-coded simple configuartion beats complex parameterized configuration when they provide the same coverage

### example 
```python
def myadd(a, b):
    return a + b
# parameterized complex unit-test that doesn't provide more coverage.
@pytest.fixture()
def addend():
    return 10 
@pytest.fixture(params=[1, 10, 100])
def random_range():
    return request.param 
def test_foo_complex (random_range, adden):
    complex_parameter = np.random.randint(random_range)
    assert myadd(complex_parameter, adden) == complex_parameter + adden 

# The different parameters provide the same set of coverage, I should
# just pick one
# Nothing wrong with hard-coded constant to me in this case, I can easily
# verify if the answer is right
def test_foo_simple():
    assert myadd(1234, 5678) == 6912
```

## False sense of correctness
If testing the wrong thing, it may be something
* irrelevent
* not reflecting real-world scenario

and it passes, it gives a false sense of confidence for the design, which sometimes is more trickier than a test that fails, because when you see a problem, you are not gonna digging into tests that pass.

### In short
* Test things that are relevant
* Test scenario that is going to happen, unless testing error-handling

### example
```python
# testing something irrelevant
def foo(mutable_list: List) -> None:
    mutable_list.append('end')

def test_foo():
    # this test passes, so what?
    assert foo([]) == None

# testing something that is never going to happen
def not_gonna_happen(mutable_object):
    mutable_object[0] = 'state changed'

def test_foo():
    mutable_object = ['initial state']
    # this test passes, but it doesn't reflect the # behavior of
    # the design under test, then why do it?
    not_gonna_happen(mutable_object)
    assert mutable_object == ['state changed']
```


