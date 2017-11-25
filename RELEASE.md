# Release process

## To release a new version of **loghub** on PyPI:

**1.)** Ensure you have the latest version from upstream and update your fork

    git pull upstream master
    git push origin master

**2.)** Update [CHANGELOG.md](https://github.com/spyder-ide/loghub/blob/master/CHANGELOG.md), using loghub itself

    loghub spyder-ide/loghub -ilg type:feature "Features " -ilg type:enhancement "Enhancements" -ilg type:bug "Bugs fixed" -ilr "reso:completed" -u <user> -m <milestone>

**3.)** Update [`loghub/__init__.py`](https://github.com/spyder-ide/loghub/blob/master/loghub/__init__.py) (set release version, remove 'dev0')

**4.)** Commit changes

    git add .
    git commit -m "Set release version"

**5.)** Create distributions

    python setup.py sdist bdist_wheel

**6.)** Upload distributions

    twine upload dist/* -u <username> -p <password>

**7.)** Add release tag

    git tag -a vX.X.X -m 'Release version'

**8.)** Update `__init__.py` (add 'dev0' and increment minor)

**9.)** Commint changes

    git add . 
    git commit -m "Restore dev version"

**10.)** Push changes
    
    git push upstream master
    git push origin master
    git push --tags

## To release a new version of **loghub** on conda-forge:

**1.)** Ensure you have the latest version from upstream and update your fork

    git pull upstream master
    git push origin master

**2.)** Update [meta.yaml](https://github.com/spyder-ide/loghub/blob/master/conda.recipe/meta.yaml) version and hash

**3.)** Commit changes

    git add .
    git commit -m "Update conda recipe"

**4.)** Update recipe on [conda-forge/loghub-feedstock](https://github.com/conda-forge/loghub-feedstock)

**5.)** Push changes

    git push upstream master
    git push origin master
