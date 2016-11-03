loghub
======

Build status
------------
|travis status| |appveyor status| |circleci status| |quantified code| |scrutinizer|

Project information
-------------------
|license| |pypi version| |gitter|

.. |travis status| image:: https://travis-ci.org/spyder-ide/loghub.svg?branch=master
   :target: https://travis-ci.org/spyder-ide/loghub
   :alt: Travis-CI build status
.. |appveyor status| image:: https://ci.appveyor.com/api/projects/status/8v5n191gy3c06dfc?svg=true
   :target: https://ci.appveyor.com/project/goanpeca/loghub
   :alt: Appveyor build status
.. |circleci status| image:: https://circleci.com/gh/spyder-ide/loghub/tree/master.svg?style=shield
   :target: https://circleci.com/gh/spyder-ide/loghub/tree/master
   :alt: Circle-CI build status
.. |quantified code| image:: https://www.quantifiedcode.com/api/v1/project/b5e47eec1e564a66a8c52c989880637b/badge.svg
   :target: https://www.quantifiedcode.com/app/project/b5e47eec1e564a66a8c52c989880637b
   :alt: Quantified Code issues
.. |scrutinizer| image:: https://scrutinizer-ci.com/g/spyder-ide/loghub/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/spyder-ide/loghub/?branch=master
   :alt: Scrutinizer Code Quality
.. |license| image:: https://img.shields.io/pypi/l/loghub.svg
   :target: LICENSE.txt
   :alt: License
.. |pypi version| image:: https://img.shields.io/pypi/v/loghub.svg
   :target: https://pypi.python.org/pypi/loghub/
   :alt: Latest PyPI version
.. |gitter| image:: https://badges.gitter.im/spyder-ide/public.svg
   :target: https://gitter.im/spyder-ide/public
   :alt: Join the chat at https://gitter.im/spyder-ide/public

Description
-----------
Changelog generator based on milestone or tags for github.

Installation
------------

Using pip

::

    pip install loghub

Using conda

::

    conda install loghub -c conda-forge

Usage
-----

loghub can be used to generate changelog based on milestones or on tags.

In projects where milestones are used to track a release we can use for example:

.. code-block:: python

    loghub spyder-ide/spyder -m v3.0


In projects where milestones are used to track chunks of work but not releases, we can use tags to get the changes after the latest release, for example:

.. code-block:: python

    loghub spyder-ide/spyder -st v3.0.0b7


Or if loghub is used to generate old changelogs (or update changelogs), we can also use tags to limit the range , for example:

.. code-block:: python

    loghub spyder-ide/spyder -st v3.0.0b7 -ut v3.0.0


For private repos, just add the username and password arguments, for example:

.. code-block:: python

    loghub spyder-ide/spyder -st v3.0.0b7 -ut v3.0.0 -u <username> -p <password>


Detailed CLI arguments
----------------------

.. code-block:: text

    usage: loghub [-h] [-m MILESTONE] [-st SINCE_TAG] [-ut UNTIL_TAG]
                  [-f OUTPUT_FORMAT] [-u USER] [-p PASSWORD]
                  repository

    Script to print the list of issues and pull requests closed in a given
    milestone

    positional arguments:
      repository            Repository name to generate the Changelog for, in the
                            form user/repo or org/repo (e.g. spyder-ide/spyder)

    optional arguments:
      -h, --help           
                            Show this help message and exit

      -m MILESTONE, --milestone MILESTONE
                            Github milestone to get issues and pull requests for

      -st SINCE_TAG, --since-tag SINCE_TAG
                            Github issues and pull requests since tag

      -ut UNTIL_TAG, --until-tag UNTIL_TAG
                            Github issues and pull requests until tag

      -f OUTPUT_FORMAT, --format OUTPUT_FORMAT
                            Format for print, either 'changelog' (for Changelog.md
                            file) or 'release' (for the Github Releases page).
                            Default is 'changelog'. The 'release' option doesn't
                            generate Markdown hyperlinks.

      -u USER, --user USER
                            Github user name

      -p PASSWORD, --password PASSWORD
                            Github user password

