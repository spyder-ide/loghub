loghub
======

Build status
------------
|travis status| |appveyor status| |circleci status| |coverage| |quantified code| |scrutinizer|

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
.. |coverage| image:: https://coveralls.io/repos/github/spyder-ide/loghub/badge.svg?branch=master
   :target: https://coveralls.io/github/spyder-ide/loghub?branch=master
   :alt: Code Coverage


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

.. code-block:: text

    loghub spyder-ide/spyder -m v3.0


In projects where milestones are used to track chunks of work but not releases,
we can use tags to get the changes after the latest release, for example:

.. code-block:: text

    loghub spyder-ide/spyder -st v3.0.0b7


Or if loghub is used to generate old changelogs (or update changelogs),
we can also use tags to limit the range , for example:

.. code-block:: text

    loghub spyder-ide/spyder -st v3.0.0b7 -ut v3.0.0


For private repos, just add the username and password arguments, for example:

.. code-block:: text

    loghub spyder-ide/spyder -st v3.0.0b7 -ut v3.0.0 -u <username> -p <password>


Or, just add the username and a password prompt will appear, for example:

.. code-block:: text

    loghub spyder-ide/spyder -st v3.0.0b7 -ut v3.0.0 -u <username>


Or generate a Github access token and use that instead, for example:

.. code-block:: text

    loghub spyder-ide/spyder -st v3.0.0b7 -ut v3.0.0 -t <token>


**Important**

Because of git api rate limitations it is advised to always use authentication
by either access token or user and password.

    
Advanced Usage
--------------

Filter PR base branch
~~~~~~~~~~~~~~~~~~~~~

Pull requests to display can be filtered depending on the branch they were
merge against (base branch):
              
.. code-block:: text

    loghub spyder-ide/spyder -b 3.x


Filter issues/PRs by labels
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To filter issues to display, we can use a regular expression:

.. code-block:: text

    loghub spyder-ide/spyder -ilr "Type.*" -m v3.1

This will filter all the issues that start with *Type*

The same can be done with PRs

.. code-block:: text

    loghub spyder-ide/spyder -ipr "<some-regex>" -m v3.1


Group issues by label
~~~~~~~~~~~~~~~~~~~~~

Issues displayed can be grouped by labels:

.. code-block:: text

    loghub spyder-ide/spyder -ilg "Type-Bug" "Bugs Fixed" "Type-Enhancement" "New Features" -m v3.1

This will result in issues being grouped in two sections with the headings
*Bugs Fixed* and *New Features* respectively.

Output format
~~~~~~~~~~~~~

Loghub provides two formats:

* 'changelog', which is the default and includes links to issues and PRs
* 'release', which does not include links

.. code-block:: text

    loghub spyder-ide/spyder -m v3.1 -f release

Custom templates
~~~~~~~~~~~~~~~~

Loghub uses Jinja2 templates to format the output. If the current template
does not  yur needs, you can copy the default `templates <https://github.com/spyder-ide/loghub/tree/master/loghub/templates>`_ 
and create a new one and provide the path to it as:

.. code-block:: text

    loghub spyder-ide/spyder -m v3.1 --template <PATH_TO_TEMPLATE>

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

      -ilg ISSUE_LABEL [TEXT TO PRINT], --issue-label-group ISSUE_LABEL [TEXT TO PRINT]
                            Groups the generated issues by the specified label.
                            This option takes 1 or 2 arguments, where the first one
                            is the label to match and the second one is the label
                            to print on the final output

      -ilr ISSUE_LABEL_REGEX, --issue-label-regex ISSUE_LABEL_REGEX
                            Label issue filter using a regular expression filter

      -plr PR_LABEL_REGEX, --pr-label-regex PR_LABEL_REGEX
                            Label pull requets filter using a regular expression
                            filter

      -b BRANCH, --branch BRANCH
                            Filter merged PRs on base branch

      -f OUTPUT_FORMAT, --format OUTPUT_FORMAT
                            Format for print, either 'changelog' (for Changelog.md
                            file) or 'release' (for the Github Releases page).
                            Default is 'changelog'. The 'release' option doesn't
                            generate Markdown hyperlinks.

      -te, --template TEMPLATE
                            Use a custom Jinja2 template file
  
      -u USER, --user USER
                            Github user name

      -p PASSWORD, --password PASSWORD
                            Github user password

      -t TOKEN, --token TOKEN
                            Github access token
