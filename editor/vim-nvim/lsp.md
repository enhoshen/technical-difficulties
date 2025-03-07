# Language server protocol in vim/nvim
<!--toc:start-->
- [Language server protocol in vim/nvim](#language-server-protocol-in-vimnvim)
  - [Server specifics](#server-specifics)
    - [marksman](#marksman)
      - [Code action](#code-action)
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
