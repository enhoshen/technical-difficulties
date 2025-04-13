# Vim/Neovim tips

<!--toc:start-->

- [Vim/Neovim tips](#vimneovim-tips)
  - [Trying to do some action but in a new tab](#trying-to-do-some-action-but-in-a-new-tab)
  - [Check startup error messages](#check-startup-error-messages)
  - [Lua](#lua) - [quick lua table debug](#quick-lua-table-debug)
  <!--toc:end-->

## Trying to do some action but in a new tab

Try search for command that start with CTRL-W. For example to open file under
cursor it is `gf` or `gF`, to open it in a new tab, goes `<Ctrl-W>gF`. See
`:help CTRL-W_gf`.

## Check startup error messages

With lazyvim installed, those startup messages seems to be handled by Snack.notifier,
so do `:lua Snacks.notifier.show_chistory()`
[ref](https://github.com/LazyVim/LazyVim/discussions/1963#discussioncomment-11274166)

## Lua

### quick lua table debug

`:lua =<table>`. Say while checking `conform` plugin's configuration of formattors  
, do `:lua =require("conform").formattorrs`. see `:help lua=`, it shows you
that it equals to `vim.print(<expr>)`. We also learn from this that `:lua print()`
and `:lua vim.print` is different.

For example, when trying to debug an plugin table

```lua
local blink = require("blink.cmp")
-- output:
-- table: 0x... (some address)
print(blink)
-- output:
--{
--  accept = <function 1>,
--  accept_and_enter = <function 2>,
--  ...
--}
vim.print(blink)
```
