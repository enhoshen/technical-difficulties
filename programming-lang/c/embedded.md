<!--toc:start-->

- [Placement new for c calling cpp override function](#placement-new-for-c-calling-cpp-override-function)
<!--toc:end-->

## Placement new for c calling cpp override function

Static derived class override function is not recognized (supposedly points to
zero) by cpp-calling c code.

```c
#include <new>
 // this doesn't initialized the Vtable of d. Unless the startup code specifically invokes them
static Derived d = Derived();
void Derived::run(){
  // this will crash if Vtable is not initialized
  this->derived_method();
}
extern "C" void foo(){
  d.run()
}
```

Use placement new

> Gemini: constructs an object at a pre-allocated memory address

```c
extern "C" void foo(){
  new (&d) Derived();
  d.run();
}
```

Clean up placement new object:

```cpp
// `delete obj` will be undefined behavior
obj->~Derived(); // manual memory deallocation
```
