# Language server protocol in vim/nvim

<!--toc:start-->
- [Language server protocol in vim/nvim](#language-server-protocol-in-vimnvim)
  - [Server specifics](#server-specifics)
    - [marksman](#marksman)
      - [Code action](#code-action)
    - [pyright](#pyright)
      - [package cannot be resolved with pip editable install](#package-cannot-be-resolved-with-pip-editable-install)
<!--toc:end-->

## Server specifics

### marksman

[project page](//https://github.com/artempyanykh/marksman), for markdown

#### Code action

`marksman` supports a lsp code action to generate tabel of contents. However I like to have sub-sections of the same names, which results in ambiguous links that all point to the first appearance of the tag. In the example below, every h2 heading in the toc points to the `## example` sub-section under `# Foo`.

```markdown
# Foo

## example

...

# Bar

## example
```

`marksman` provides diagonistics for ambiguous links in location list, we can simply delete all of them:

```vim
" call code action when marksman is attached
:lua vim.lsp.buf.code_action()
" delete all the lines in the location list
:ldo :delete
```

### pyright

#### package cannot be resolved with pip editable install

When developing, I use `python -m pip install -e .`, and it is stated that
`pyright` cannot resolve package path properly as a static analyzer.

My python project looks like this, pretty standard

```shell
project (root)
├── project
├── submodule
    └── foo
        └── foo
    └── bar
        └── bar
```

```python
# one of this package can be resolved? WTF?
import foo
import bar
```

I found out under `.local/lib/python*/site-packages`, the not working project
installed by `python -m pip install -e .` creates `.pth` and `.finder.py` files
, and instead the working one has a `.egg-link` file simply contains the
project absolute path in it. The difference is probably caused by newer `pip` or python
version.

So maybe manually creating the `.egg-link` file would work, but I just add a
symbolic link to fool `pyright` into thinking the submodule project is also
a regular project under the project root:

```shell
# under project root
ln -s submodule/foo/foo foo
ln -s submodule/bar/bar bar
ls -a
# ... foo -> submodule/foo/foo/
```

This is mainly for `find definition`, the most important feature
of a LSP in my opinion, to work properly.
