# Setting up linux environment

<!--toc:start-->

- [Setting up linux environment](#setting-up-linux-environment)
  - [Upgrade glibc](#upgrade-glibc)
    - [First:](#first)
    - [Second:](#second)
    - [Third:](#third)
  - [Upgrade ubuntu](#upgrade-ubuntu)
  <!--toc:end-->

## Upgrade glibc

Newer version of `Lazyvim` asks for newer `neovim`, and newer `neovim`
requires newer `glibc`... In the unusual case of having to

- build from from source
- as non-root

Such as working on a ancient `centos` EDA server, I followed [this article](https://xbmlz.github.io/centos7-upgrade-glibc/)

The three steps of upgrading `gcc` -> `make` -> `glibc` all involve
`wget` the tarball, extract, create build directory, **configure**, `make -jN`
, make install.

I encountered three problems.

### First:

I use the following configure command to install under `~/usr/`

```shell
../configure --prefix=/home/user/usr ...
```

This will not immediately work unless `export PATH=/home/user/usr:$PATH`
makes `/home/user/usr` takes priority. If this is put under `*shrc` then
remember to re-source them.

### Second:

```shell
checking for gnumake... no
checking for gmake... gmake
...
configure: error:
*** These critical programs are missing or too old: make
*** Check the INSTALL file for required versions.
```

After successfully upgrade `make` and check with `make --version`. This is kind
of dumb because `gmake` is exactly `make`. But we only just set up the `make`
binary under `/home/user/usr/bin`. Configure tool will try to version check the
default `/usr/bin/gmake`.
Solve this by `ln -vsf /home/user/usr/bin/make /home/user/usr/gmake`, making
`gmake` binary by soft link ourself.

### Third:

When configuring `glibc`, the article instruct us to install under `/usr/`

```shell
../configure  --prefix=/usr --disable-profile --enable-add-ons --with-headers=/usr/include --with-binutils=/usr/bin --disable-sanity-checks --disable-werror
```

I use `/home/user/usr` as prefix and got

```shell
checking installed Linux kernel header files... missing or too old!
configure: error: GNU libc requires kernel header files from
Linux 3.2.0 or later to be installed before configuring.
```

Because there is literally no linux kernal header under `/home/user/usr`, not
because we have the too-old version. Remove the `--with-headers=/home/user/usr/include`
so it falls back to searching header under `/usr/include`. Thankfully I had
those headers under `/usr/include`

## Upgrade ubuntu

Annoyingly many software requires newer glibc and I may be using `centos7` or
`ubuntu 20.02`. In my case I need to upgrade `ubuntu` to `22.04`.

I follow this [guide](https://askubuntu.com/a/1428481)

```shell
sudo apt update && sudo apt full-upgrade
# restart wsl
# in power shell
wsl --terminate Ubuntu
# in wsl
sudo do-release-upgrade
```

and encountered following problems:

- "No module named `apt_pkg`" when running `do-release-upgrade`
  - Solved this by linking the proper `apt_pkg` shared libary
  ```shell
  sudo ln -s /usr/lib/python3/dist-packages/apt_pkg.cpython-38-x86_64-linux-gnu.so apt_pkg.so
  ```
- And while running `do-release-upgrade` it complained the python is corrupted:

  ```shell
  Can not upgrade

  Your python3 install is corrupted. Please fix the '/usr/bin/python3'
  symlink.
  ```

  - this is because I dynamic link my preferred version of python directly
    to `/usr/bin/python3`, now you learn again and again not to do this..
  - to fix this, link the correct system python binary back, for `Ubuntu 20.04`
    it's `3.8`

  ```shell
  sudo ln -sf /usr/bin/python3.8 /usr/bin/python3
  ```
