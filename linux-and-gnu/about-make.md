# About GNU make

<!--toc:start-->
- [About GNU make](#about-gnu-make)
  - [shell command substitution used in recipe](#shell-command-substitution-used-in-recipe)
<!--toc:end-->

## shell command substitution used in recipe

- Makefile variable, cannot be changed in a recipe

  ```makefile
  D=$$(date)

  test:
    @# program is fast so the output string will be the same
    @echo $(D)
  ```

- Same line, same shell

  ```makefile
    @d=$$(date); \
    echo $${d}
  ```

- Make `eval` funciton

  ```makefile
  .PNONY: abc
  abc:

  test2: abc
    @# first prerequisite
    @echo $<
    @# eval is a make function, define new construct dynamically
    @# notice this is not ' single quote
    @# backtick is one way to do command substitution
    @$(eval d=`date`)
    @echo $d
    @# insane amount of escape to make shell command substitution work
    @# 	first expansion: the eval, so each $$ pair becomes $
    @# 	second expansion: d=$$(date) the usual make variable assignment to
    @#   shell command substitution
    @$(eval d=$$$$(date))
    @echo $d
  ```

- `ONESHELL`
  ```makefile
  # every rule will be in oneshell, defeat the fundamental design of
  # enviorment seperation per recipe lines
  # .ONESHELL:
  # test3:
  # 	@export d=$$(date)
  # 	@D=$$(ls)
  #
  # 	@echo $${d} $(D)
  ```
