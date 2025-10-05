# Lua programming tips

<!--toc:start-->
- [Lua programming tips](#lua-programming-tips)
  - [lua synthetic sugar](#lua-synthetic-sugar)
<!--toc:end-->

## lua synthetic sugar

- single argument function call

```lua
-- Standard function calls
print("Hello, world!")
table.insert(my_table, "new value")

-- Syntactic sugar (parentheses omitted)
print "Hello, world!"  -- Equivalent to print("Hello, world!")
table.insert my_table, "new value" -- This won't work!  table.insert takes two arguments, so you can't use the sugar.
```
