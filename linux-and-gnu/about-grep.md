# All about grep

<!--toc:start-->
- [All about grep](#all-about-grep)
  - [Exclude pattern using grep negative lookahead/lookbehind](#exclude-pattern-using-grep-negative-lookaheadlookbehind)
<!--toc:end-->

## Exclude pattern using grep negative lookahead/lookbehind

When doing file operations like `ls`, one may need to exclude some pattern, an option is to pipe the output to `grep`. In order to do this, negative lookahead is needed. The syntax is availale with option `-P` meaning perl compatiable regex pattern.

```shell
# match files ending with .sh, but not install.sh
# ! in double quote in bash is history expansion, so we have to escape it,
# or use single-quote instead
ls *.sh | grep -P "(?<\!install)\.sh"
ls *.sh | grep -P '(?<!install)\.sh'
```

Better avoid double quote when using negative lookahead/lookbehind all together, it works weirdly,

```shell
# this may work
ls *.sh | grep -P "(?<\!install)\.sh"
# but not in command expansion $()
# (This command should copies files ending in .sh but not install.sh
# to ~/)
cp $(ls *.sh | grep -P "(?<\!install)\.sh") ~/
# And single quote should work
cp $(ls *.sh | grep -P '(?<\!install)\.sh') ~/
```
