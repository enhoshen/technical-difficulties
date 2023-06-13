# All about Bash

## What are these `&&, ||, ;, &`?
When you try to learn about these "operator" you might have a hard time picking the best keyword when searching. They are operators seperating lists of command

see: [3.2.4 Lists of Command](https://www.gnu.org/software/bash/manual/html_node/Lists.html)

## Pattern matching
Pattern matching is used for filename expansion, or wherever in the documentation the word *PATTERN* comes up (I believe). Let's see a couple of example first.
```shell
# in a folder container about-tests/
ls [[:lower:]]bout-tests # list files under about-tests/
# matches pattern in conditional construct
[[ a == [a-z] ]] && echo "match found"
[[ abc == * ]] && echo "match found"
[[ a == ? ]] && echo "match found"
[[ abc == *([a-z]) ]] && echo "match found"
```
The document is actually very clear, but there are some nuance you may very likely overlook and cause your pattern to not work.  
see [3.5.8.1 Pattern Matching](https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html)

### mixed with glob
When in combination of glob pattern we are very familiar with, things may not work as expected, if the documentation is not read thoroughly.
Let's read the document first:  
> Composite patterns may be formed using one or more of the following sub-patterns:  
> ?(*pattern-list*) ...  

This looks and works very much like regex. But watch carefully that the patter-list **must** be enclosed in parentheses.
```shell
# This is actually a glob in combination with `[]` pattern matching
# because the [a-z] is not enclosed in parentheses `()`
[[ 12c == *[a-z] ]] && echo "match found"
# This matches [a-z] whatever times, then glob matches whatever characters
# after the dot
ls *([a-z]).* # matches abc.sh cde.txt etc.
```

### Pattern matching with character classes
Read carefully for the *character classes* section
|> Within ‘[’ and ‘]’, character classes can be specified using the syntax [:class:]
```shell
# match fails
[[ a == [:lower:] ]] && echo "mathces"
# it works enclosed in brackets
[[ a == [[:lower:]] ]] && echo "mathces"
```
However, for whatever reason, the character class `word` doesn't work in zsh (v5.8.1)
```shell
# match fails, :word: equals [A-Za-z0-9_]
[[ a == [:lower:] ]] && echo "mathces"
```
