# Release process

## To release a new version of **loghub** on PyPI:

* Ensure you have the latest version from upstream and update your fork

  ```bash
  git pull upstream master
  git push origin master
  ```

* Clean the repo

  ```bash
  git clean -xfdi
  ```

* Update CHANGELOG.md using loghub itself:

    * if using Github Milestones:

      ```bash
      loghub spyder-ide/loghub -ilg type:feature "Features " -ilg type:enhancement "Enhancements" -ilg type:bug "Bugs fixed" -ilr "reso:completed" --no-prs -u <github-username> -m <github-milestone>
      ```

    * if using ZenHub Releases:

      ```bash
      loghub spyder-ide/loghub -ilg type:feature "Features " -ilg type:enhancement "Enhancements" -ilg type:bug "Bugs fixed" -ilr "reso:completed" --no-prs -u <github-username> -zr <zenhub-release> -zt <zenhub-token>
      ```

* Update version in `__init__.py` (set release version, remove 'dev0')

* Commit changes

  ```bash
  git add .
  git commit -m "Set release version"
  ```

* Create distributions

  ```bash
  python setup.py sdist bdist_wheel
  ```

* Upload distributions

  ```bash
  twine upload dist/* -u <username> -p <password>
  ```

* Add release tag

  ```bash
  git tag -a vX.X.X -m 'Release version'
  ```

* Update `__init__.py` (add 'dev0' and increment minor)

* Commint changes

  ```bash
  git add .
  git commit -m "Restore dev version"
  ```

* Push changes
    
  ```bash
  git push upstream master
  git push origin master
  git push --tags
  ```

## To release a new version of **loghub** on conda-forge:

* Update recipe on the loghub feedstock: https://github.com/conda-forge/loghub-feedstock
