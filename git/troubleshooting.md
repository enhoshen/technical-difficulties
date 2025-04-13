# Troubleshooting in git

<!--toc:start-->

- [Troubleshooting in git](#troubleshooting-in-git)
  - [Deleted remote branch keeps coming back when pushing](#deleted-remote-branch-keeps-coming-back-when-pushing)
  <!--toc:end-->

## Deleted remote branch keeps coming back when pushing

To rename a branch both locally and remotely, we run

```shell
# rename local branch
git branch -m <old branch> <new branch>
# delete remote branch
git branch <remote> -d <old branch>
# push new branch and set upstream to remote
git push -u origin <new branch>
```

It might end up like this:

```shell
 remote:
 To <remote url>
  * [new branch]      <new branch> -> <old branch>
```

One possible cause, and the one I encountered may be that the upstream is not reset. Simply reset the upstream then push.

```shell
# Possibily, if the upstream is already set, git push -u doesn't update it
# so we reset it first
branch --unset-upstream <new branch>
git push --set-upstream origin <new branch>
```
