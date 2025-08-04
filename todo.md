- Gitlab CICD

  - Runner level credential
  - registry service port != base service port

- model module design
- algorithm

  - b-tree
  - priority queue
  - minimum spanning tree
    - prim
    - kruskal
  - loop invariant

- how to find bind doc in bash and bindkey in zsh

  - obvi, `man bash`, `man zshzle` instead of `man bind`

- why can't c-q to be set as key bind in bash: https://unix.stackexchange.com/questions/72086/ctrl-s-hangs-the-terminal-emulator
- from wsl clipboard to windows clipboard

  - cat clip.txt | clip.exe
  - remember to do it in a wsl session, not in a ssh session to the wsl instance

- How does vscode have built-in json code completion: json schema
- Turn off windows terminal bell: defaults:{ "bell-style": none }

- Install python-dev with python<version>-dev
- `python -m pip install .` (with setup.py)

  ```sh
  running egg_info
  writing <packagge>.egg-info/PKG-INFO
  error: [Errno 13] Permission denied: '<package>.egg-info/PKG-INFO'
  ```

  grant permission with sudo of the working directory:
  `sudo chmod -R 777 <package folder>`

- test oversight: test not only parameter on certain range, but also
  the boundary, obviously.

  ```python
  # test on certain numeric ranges
  assert floor(3.4) == 3
  assert floor(3.6) == 3
  # but also the boundaries, even if it seems to be trivial
  assert floor(3.0) == 3
  ```

- In tests, assert statement in a function may not be run, this must be caught
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

- gitlab "remote: you are not allowed to upload code, fatal: unable to access <url>: The requested URL returned error: 403"
  when gitlab.credential.helper is set to store, user/passwd will be changed. I
  use something like `pip install https://<user>:<passwd>@<url>, and the credential
  is obscurely changed; specifically I was using a deploy token without write
  permission, thus the message

- connection broken by 'SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE VERIFY 9 Y_ FAILED] certificate verify failed: self signed certificate
  for the command `python -m pip install https://<repo url>`. So we know that for pip
  to directly install from a repo, add `git+` before the url, it's not a problem
  with SSL, the error message may lead to wrong debug direction

- for pip, in cli or in requirements.txt, specify user/passwd with the following
  syntax:
  `python -m pip install git+https://<user>:<passwd>@<repo url>.git@<commit/branch>`
- convert **iter** to **await**

- git show-ref,
  warning: refname 'HEAD' is ambiguous.warning: redirecting to https://192.168.1.139:10443/chip/gzsim.git/
  There is no tracking information for the current branch.
  Please specify which branch you want to merge with.
  See git-pull(1) for details.

        git pull <remote> <branch>

  If you wish to set tracking information for this branch you can do so with:
  git branch --set-upstream-to=origin/<branch> develop

- cicd install package hosted locally:
  setup deploy token from the project settings, and use it as a user password
  pair for authentication, then in requirements.txt

  ```txt
  git+https://deploy-token:${DEPLOY_TOKEN}@{repo host url}/{repo}
  ```

- Add local location as remote: local remote
  as simple as
  ```shell
  git remote add <NAME> <PATH>
  ```
- shift-I in vim
- git show file from commit: `git show branch:file`
- git rebase but keep the branch:
  just create a new branch from the branch and rebase it:
  ```
  # on A, to be rebase onto B
  git branch -b rebase/A
  git checkout rebase/A
  git rebase B
  ```
- Monad like application for callable:
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
- Find a way around explicitly creating all combinations
  Say we have a callable chain

  ```python
  class Chain:
      foo: callable
      bar: callable
      def __call__(self, data):
          return bar(foo(data))
  ```

  This is a product type, the number of combinations it can have
  = (# of foo) \* (# of bar)  
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

- check vpn split tunneling,
  On windows:

```shell
# check ip trace that doesn't go through the vpn
$tracert facebook.com
Tracing route to facebook.com [31.13.87.36]
over a maximum of 30 hops:

  1    <1 ms    <1 ms    <1 ms  192.168.1.1
  2     2 ms     2 ms     2 ms  192.168.0.1
  ...

# and then trace the ip that should go through the vpn
$tracert 192.168.0.128

Tracing route to <host name> [192.168.3.121]
over a maximum of 30 hops:

  1    18 ms    13 ms    12 ms  MY-PC [123.123.123.123]
  2    14 ms    15 ms    13 ms  <remote host> [192.168.0.128]

# And check vpn settings
# we can see that the second ip goes through the ip address of the VPN
# first
$ipconfig /all

Windows IP Configuration

   Host Name . . . . . . . . . . . . : MY-PC
   Primary Dns Suffix  . . . . . . . :
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No

Ethernet adapter 乙太網路 3:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : <VPN description>
   Physical Address. . . . . . . . . :
   DHCP Enabled. . . . . . . . . . . :
   Autoconfiguration Enabled . . . . :
   Link-local IPv6 Address . . . . . : ...
   IPv4 Address. . . . . . . . . . . : 123.123.123.123(Preferred)
   ...
```

- To use nerd font:
  Install the font on the host machine! Say I am ssh-ing from A windows machine,
  install the font on A machine, and change the setting of the A machine terminal.
  In my case, I am using windows terminal, then after installing the font,
  by just clicking on the ttf file, go `Settings > <Profile> > Appearance > Font Face`
  and it's all done, no need to install the font on the remote machine.

- Max/min rounds before face-off between two players

  - N players
  - Each round, for the left N/2 players, player i plays against player N-i (1-index)
    in other words, every players plays against the reflection of its position in the
    player array.
  - if N is odd, the middle player directly advances to the next round.
  - There are two players that always win, for other player pairs, we can choose either
    of the pair to advance into the next round
  - Compute the min/max rounds until the two winning players face each other.
    DP approach with three parameters:
  - N: number of players
  - A: index of the first winning player
  - B: index of the second winning player

    We need a DP array for each remaining player numbers N, N/2, N/4 ..., for each round
    if the remaining players is odd, we have to check (N+1)/2 instead.

  Each DP array is just a upper triangle matrix, where a(i,j) represents player a
  at position i and player b at position b (1-index). Also, j is always larger
  than i, so we only need a (N-1)x(N-1) upper triangle matrix for case N. This is
  also the number of combinations of picking two positions out of N positions.
  In practice, the upper triangle matrix should be stored in an array (though this doesn't seem particularly useful).

  Starting from the ground up, for each number of player N, each cell holds
  (max rounds, min round) until the two players meet. N=1 is not considered.
  For N=2, as mentioned, there is (2\*1)/2 = 1 combination, max/min rounds are 1.

  For each round, if A and B are in opposite positions in the player array,
  the max/min remaining rounds are 1.

  Now, for each iteration, starting from n = 1,
  for all the possible outcomes in the next round, the min rounds is min(all possible outcomes + 1)
  and the max rounds is max(all possible outcomes + 1).

  Now we just calculate the possible position of a in the next round (a), and the offset
  of b player from player A's position (ofs), the Cartesian product of the (a, a+ofs) gives the
  position combinations of the a,b players in the next round, combined with the number
  of players in the next round is n/2 or (n+1)/2, meaning that half of the players
  are eliminated this round, we can get the min/max round for all combinations of the
  current number of player n.

  Now the trickiest part, computing the possible outcomes. Divide into three cases:

  1. a,b all on left half of the array(a,b <= N/2)

  - The possible number of players survive to the left of player A determines player A's
    position on the next round.
  - remember to rule out the players eliminated by a, b
  - if n is odd, the middle player must be excluded.
  - b-a-1 is the # of players possible between a and b, this number happens
    to be the ofs

  2. a is in the left half array, b is in the right half

  - a position is the same as case 1
  - b-(n/2) or b-(n+1)/2 is the b position on the left half
  - This number is the ofs.
  - Remember to eliminate A's opponent if it is also on left half and has a smaller
    position than b

  3. A and B are both in the right half

  - Treat A and B like B in case 2.

* `:filter`, `:let g:`
* `man 1 bash`, `edit-and-execute-command`
* polars

  - join(on: Sequence)
  - arr.get(index)
  - str.slice
  - concat_arr

* bash redirection

  In bash manual:

  > 3.6.8 Duplicating File Descriptors
  >
  > `[n]>&word`
  >
  > is used similarly to duplicate output file descriptors

  ```shell
  # ffmpeg along returns 2, and output to stderr
  # redirrecting err to stdout we can then grep the output
  # "lib" are highlighted by grep
  ffmpeg 2>&1 | grep lib
  ```
