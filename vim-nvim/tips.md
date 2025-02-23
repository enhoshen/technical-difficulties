# Vim/Neovim tips

<!--toc:start-->
- [Vim/Neovim tips](#vimneovim-tips)
  - [Trying to do some action but in a new tab](#trying-to-do-some-action-but-in-a-new-tab)
  - [Check startup error messages](#check-startup-error-messages)
<!--toc:end-->

## Trying to do some action but in a new tab
Try search for command that start with CTRL-W. For example to open file under
cursor it is `gf` or `gF`, to open it in a new tab, goes `<Ctrl-W>gF`. See
`:help CTRL-W_gf`.


## Check startup error messages
With lazyvim installed, those startup messages seems to be handled by Snack.notifier,
so do `:lua Snacks.notifier.show_chistory()`
[ref](https://github.com/LazyVim/LazyVim/discussions/1963#discussioncomment-11274166)
