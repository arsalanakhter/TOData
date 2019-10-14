# TOData

## Workflow

0. Pull any changes from master
```
$ git checkout master
$ git pull origin master
```
1. Create an issue on Github that should be worked on.
2. On the local computer create a new branch with the issue name
```
$ git checkout -b issue#1
```
3. Work, commit. 

  - In the commit message, use the keywords `fixes #1` or `resolves #1`. This helps with automatically closing the issue that we worked on.

  - Once done, push to github.
```
$ git push origin issue#1
```
4. Create a pull request for merging into master
5. Review and merge, and delete the branch on github, if the work in finished
6. Once merged, then on your local computer, switch to master again
```
$ git checkout master
```
8. Now pull the changes from remote origin/master to local master
```
$ git pull origin master
```
7. Delete the local branch on your computer
```
$ git branch -D issue#1
```
