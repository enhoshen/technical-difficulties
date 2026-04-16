# Command line tools

<!--toc:start-->
- [Command line tools](#command-line-tools)
  - [Use `fzf` by Junegunn as grep](#use-fzf-by-junegunn-as-grep)
  <!--toc:end-->

## Use `fzf` by Junegunn as grep

- feed input list via STDIN
- `-f` filter argument

This returns a list of result like grep non-interactively
EX: `ls | fzf -fabc`: query with `abc` the list returned by `ls`
