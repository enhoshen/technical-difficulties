# Trouble shooting in vim/nvim
<!--toc:start-->
- [Trouble shooting in vim/nvim](#trouble-shooting-in-vimnvim)
  - [`:help` cannot locate document for plugin](#help-cannot-locate-document-for-plugin)
<!--toc:end-->

## `:help` cannot locate document for plugin
### case study
Not sure if intended, `:help` cannot locate documentation for `packer` plugin.

### solution
It seems that what's following `:help` command are help tags (see `:help :helptags`), so we should run `:helptags <document path>` to update the help tags file.
```vim
" document for packer is located at ~/.local/share/nvim/site/pack/packer/start/packer.nvim/doc/
:helptags ~/.local/share/nvim/site/pack/packer/start/packer.nvim/doc/
```
