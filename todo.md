* Gitlab CICD
    * Runner level credential
    * registry service port != base service port

* model module design 
* algorithm
    * b-tree
    * priority queue
    * minimum spanning tree
        * prim
        * kruskal
    * loop invariant

* how to find bind doc in bash and bindkey in zsh
    * obvi, `man bash`, `man zshzle` instead of `man bind`

* why can't c-q to be set as key bind in bash: https://unix.stackexchange.com/questions/72086/ctrl-s-hangs-the-terminal-emulator
* from wsl clipboard to windows clipboard
    * cat clip.txt | clip.exe
    * remember to do it in a wsl session, not in a ssh session to the wsl instance

* How does vscode have built-in json code completion: json schema
* Turn off windows terminal bell: defaults:{ "bell-style": none }

* Install python-dev with python<version>-dev
* `python -m pip install .` (with setup.py)
    ```sh
    running egg_info
    writing <packagge>.egg-info/PKG-INFO
    error: [Errno 13] Permission denied: '<package>.egg-info/PKG-INFO'
    ```
    grant permission with sudo of the working directory:
    `sudo chmod -R 777 <package folder>`

* test oversight: test not only parameter on certain range, but also
 the boundary, obviously.
    ```python
    # test on certain numeric ranges
    assert floor(3.4) == 3
    assert floor(3.6) == 3
    # but also the boundaries, even if it seems to be trivial
    assert floor(3.0) == 3
    ```

* In tests, assert statement in a function may not be run, this must be caught
  if the function one way or another, a simple way:
    ```python
    # Pass a mutable object to the function that may not finish
    async def not_run(result: List):
        assert result == [1234]
        result.append(5678)
    asyncio.run(not_run())
    # check OUTSIDE of the function it mutate the result
    assert result == [1234, 5678]
    ```
