# All about man

## What does <command>(#) mean in the title of a man page?

Let's see the output of `man man`, the manual page of command `man`:

```
MAN(1)     Manual pager utils   MAN(1)

NAME
       man - an interface to the system reference manuals
```

What does the `(1)` mean after "MAN"? Let's read the OVERVIEW section of `man man`:

>       The table below shows the section numbers of the manual followed by the types of pages they contain.
>
>       1   Executable programs or shell commands
>       2   System calls (functions provided by the kernel) ...

and the command synopsis:

> man [man options] [[section] page ...] ...

We know that you can add section number before the command!

```shell
# Read the 5th section about file formats and conventions for command passwd
man 5 passwd
```

## Where does man search for pages?

I came across a weird and rarely documented behavior where `man` is able to locate the man page of an executable just added to `PATH`.

```shell
# No manual entry for cmake
man cmake
# Add cmake to PATH, the file hierarchy of the package is
# - cmake_base/
#   - bin/
#     - cmake # cmake binary
#   - man/
#   - doc/
#   - share/
export PATH=${PATH}:cmake_base
# The man can magically locate the man pages under cmake_base/man now!
man cmake
```

First we read man pages of `man`

```shell
man man
```

Under the `OVERVIEW` section, it reads

> Manual pages are normally stored in nroff(1) format under a directory such as /usr/share/man. In some installations, there may also be preformatted cat pages to improve performance. See manpath(5) for details of where these files are stored.

So we know we can read about manual of `manpath`. First we look at the first section of `manpath`

```shell
man manpath
```

In the `ENVIRONMENT` section, it reads

> See the SEARCH PATH section of manpath(5) for the default behaviour and details of how this environment variable is handled.

So we have to look for the 5th section of `manpath`, marked by `manpath(5)`.

```shell
man 5 manpath
```

> If there is no MANPATH_MAP line in the configuration file for a given path_element, then it adds all of path_element/../man, path_element/man, path_ele‐ ment/../share/man, and path_element/share/man that exist as directories to the search path.
