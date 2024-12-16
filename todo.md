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

* gitlab "remote: you are not allowed to upload code, fatal: unable to access <url>: The requested URL returned error: 403"
  when gitlab.credential.helper is set to store, user/passwd will be changed. I
  use something like `pip install https://<user>:<passwd>@<url>, and the credential
  is obscurely changed; specifically I was using a deploy token without write
  permission, thus the message


* connection broken by 'SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE VERIFY 9 Y_ FAILED] certificate verify failed: self signed certificate
  for the command `python -m pip install https://<repo url>`. So we know that for pip
  to directly install from a repo, add `git+` before the url, it's not a problem
  with SSL, the error message may lead to wrong debug direction

* for pip, in cli or in requirements.txt, specify user/passwd with the following
  syntax:
  `python -m pip install git+https://<user>:<passwd>@<repo url>.git@<commit/branch>`
  
* convert __iter__ to __await__

* git show-ref,
    warning: refname 'HEAD' is ambiguous.warning: redirecting to https://192.168.1.139:10443/chip/gzsim.git/
    There is no tracking information for the current branch.
    Please specify which branch you want to merge with.
    See git-pull(1) for details.

        git pull <remote> <branch>

    If you wish to set tracking information for this branch you can do so with:
    git branch --set-upstream-to=origin/<branch> develop
* cicd install package hosted locally:
    setup deploy token from the project settings, and use it as a user password
    pair for authentication, then in requirements.txt
    ```txt
    git+https://deploy-token:${DEPLOY_TOKEN}@{repo host url}/{repo}
    ```

* Add local location as remote: local remote
    as simple as
    ```shell
    git remote add <NAME> <PATH>
    ```
* shift-I in vim
* git show file from commit: `git show branch:file`
* git rebase but keep the branch:
    just create a new branch from the branch and rebase it:
    ```
    # on A, to be rebase onto B
    git branch -b rebase/A
    git checkout rebase/A
    git rebase B
    ```
* Monad like application for callable:
    # instead of nested calls
    ```
    a(
        b(
            c(
                d(
                    data
                )
            )
        )
    )
    # First wrap the data in a Chain object
    class Chain
        def call(self, func: Callable):
            return Chain(func(self.data))
    # then we can use builder pattern when calling
    # a chain of callables
    for t in transforms:
        result = Chain(data)
            .call(a)
            .call(b)
            .call(c)
            .call(d)
            .data
        .data
    ```
* Find a way around explicitly creating all combinations
    Say we have a callable chain
    ```python
    class Chain:
        foo: callable
        bar: callable
        def __call__(self, data):
            return bar(foo(data))
    ```
    This is a product type, the number of combinations it can have
    = (# of foo) * (# of bar)  
    In this case, `Chain` wouldn't be a great design if all combinations
    will be used.
    ```python
    # You have to create the instances for all combinations
    for f in foos:
        for b in bars:
            chains.append(chain(f,b))
    # But when you use them, you still have to locate the combination you
    # need, this will be the same loop used for Chain creation

    # two loops that cannot be combined
    for f in foos:
        # previously created chain really not make things any easier
        chain = chains.locate(f,BAR)
        iterate_over_foo.append(chain(data))
    for b in bars:
        chain = chains.locate(FOO,b)
        iterate_over_bar.append(chain(data))

    # so instead just use the components explicitly, separately
    for f in foos:
        iterate_over_foo.append(BAR(f(data)))
    for b in bars:
        iterate_over_bar.append(b(FOO(data))
    ```
