<!--toc:start-->

- [Placement new for c calling cpp override function](#placement-new-for-c-calling-cpp-override-function)
<!--toc:end-->

## Placement new for c calling cpp override function

placement c:

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

```c
extern "C" void foo(){
  new (&d) Derived();
  d.run();
}
```
