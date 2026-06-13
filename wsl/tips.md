# Tips

<!--toc:start-->
- [Tips](#tips)
  - [Open file in windows host](#open-file-in-windows-host)
    - [Open with default app](#open-with-default-app)
    - [Open explorer](#open-explorer)
    - [Update `xdg-open` to work with vim `gx`](#update-xdg-open-to-work-with-vim-gx)
<!--toc:end-->

## Open file in windows host

### Open with default app

```sh
cmd.exe /C start <file>`
```

Often this gives the following error

```sh
'\\wsl.localhost\Ubuntu\root\technical-difficulties'
CMD.EXE was started with the above path as the current directory.
UNC paths are not supported.  Defaulting to Windows directory.
The system cannot find the file wsl/tips.md.
```

Alternatively use `wslview`

```sh
# if the distro is old, install manually
sudo apt install wslu
# open the file in the windows default app
wslview <file>
```

### Open explorer

Open the folder in explorer can be quite useful than opening the file
directly sometimes.

```sh
explorer.exe .
```

### Update `xdg-open` to work with vim `gx`

Create a file `xdg-open`

```sh
#!/bin/bash
if grep -q WSL /proc/version; then
  wslview $1
else
  /usr/bin/xdg-open "$1"
fi
```

Make sure the `$PATH` can locate this pseudo binary.
When we use `gx` in normal mode in vim/nvim, it will try to
open the path with "the system default handler", evidently
in wsl this is `xdg-open` by default (see `:help gx`).
Surprisingly joyful, in an `oil.nvim` buffer, `gx` works
perfectly and can directly open the file under the cursor.
