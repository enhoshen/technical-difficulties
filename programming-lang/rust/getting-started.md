# Getting started with rust

<!--toc:start-->
- [Getting started with rust](#getting-started-with-rust)
  - [Mutate non-overlapping part of a struct member](#mutate-non-overlapping-part-of-a-struct-member)
<!--toc:end-->


## Mutate non-overlapping part of a struct member
1. `cargo new toy`: create a new rust project
2. paste this in `toy/main.rs`
```rust
struct LargeStruct {
    data1: [i32; 1000],
    data2: [f64; 500],
}

fn observer1(data: &mut [i32; 1000]) {
    // Modify data1
    for i in 0..data.len() {
        data[i] += 1;
    }
}

fn observer2(data: &mut [f64; 500]) {
    // Modify data2
    for i in 0..data.len() {
        data[i] *= 2.0;
    }
}

// to hold a reference member, lifetime has to be specific
// >> https://doc.rust-lang.org/book/ch05-01-defining-structs.html
// >> https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html
struct Monitor<'a> {
    name: String,
    target: &'a LargeStruct
}

impl <'a>Monitor<'a> {
    fn monitor(& self) {
        // Access the entire struct immutably
        println!("{}", self.name);
        println!("data1: {}", self.target.data1[0]);
        println!("data2: {}", self.target.data2[0]);
    }
}

fn main() {
    let mut large_struct = LargeStruct {
        data1: [1; 1000],
        data2: [1.0; 500],
    };

    // Mutably borrow disjoint parts
    observer1(&mut large_struct.data1);
    observer2(&mut large_struct.data2);

    // multiple immutable references to the same object
    let m0 = Monitor{name: "m0".to_string(), target: &large_struct};
    let m1 = Monitor{name: "m1".to_string(), target: &large_struct};
    m0.monitor();
    m1.monitor();
}
```
3. `cargo run`: run the code under `toy/`

We can see that we can have multiple immutable reference to the shared, mutable
object, whose mutable data members are modified non-overlapping by different
borrower (observer*).
