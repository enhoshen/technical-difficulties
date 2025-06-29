# Vim/Neovim tips

<!--toc:start-->
- [Vim/Neovim tips](#vimneovim-tips)
  - [Trying to do some action but in a new tab](#trying-to-do-some-action-but-in-a-new-tab)
  - [Check startup error messages](#check-startup-error-messages)
  - [cmdline-special and expand](#cmdline-special-and-expand)
  - [Lua](#lua)
    - [quick lua table debug](#quick-lua-table-debug)
    - [run vim function in lua code](#run-vim-function-in-lua-code)
<!--toc:end-->

## Trying to do some action but in a new tab

Try search for command that start with CTRL-W. For example to open file under
cursor it is `gf` or `gF`, to open it in a new tab, goes `<Ctrl-W>gF`. See
`:help CTRL-W_gf`.

## Check startup error messages

With lazyvim installed, those startup messages seems to be handled by
`Snacks.notifier`, so do `:lua Snacks.notifier.show_history()`, or with keybind
`<Leader>n` to open a notification window, setup by `Snacks.picker` by default
[ref](https://github.com/LazyVim/LazyVim/discussions/1963#discussioncomment-11274166)

## cmdline-special and expand

Looking at `:help gx` we find that file name under cursor has something to do with `<cfile>`.
These special character will be expanded

- when file name are to be expected in ex command
- when used in function `expand`, like `expand("<cfile>")`
  let's put cursor under a URL like https://www.google.com and type:

```vimscript
:echo expand("<cfile")
```

and the URL will be printed.

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

### run vim function in lua code

`vim.fn`. Straight to the example:

```lua
function ()
  -- :let path=expand("<cfile>")
  path = vim.fn.expand("<cfile>")
  vim.print(path)
end
```
