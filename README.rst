loghub
======

Project details
---------------
|license| |pypi version| |gitter| |backers| |sponsors|

Build status
------------
|travis status| |appveyor status| |circleci status| |coverage| |scrutinizer|

.. |travis status| image:: https://travis-ci.org/spyder-ide/loghub.svg?branch=master
   :target: https://travis-ci.org/spyder-ide/loghub
   :alt: Travis-CI build status
.. |appveyor status| image:: https://ci.appveyor.com/api/projects/status/vlvwisroqjaf6jvl?svg=true
   :target: https://ci.appveyor.com/project/spyder-ide/loghub
   :alt: Appveyor build status
.. |circleci status| image:: https://circleci.com/gh/spyder-ide/loghub/tree/master.svg?style=shield
   :target: https://circleci.com/gh/spyder-ide/loghub/tree/master
   :alt: Circle-CI build status
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
.. |coverage| image:: https://coveralls.io/repos/github/spyder-ide/loghub/badge.svg
   :target: https://coveralls.io/github/spyder-ide/loghub?branch=master
   :alt: Code Coverage
.. |backers| image:: https://opencollective.com/spyder/backers/badge.svg?color=blue
   :target: #backers
   :alt: OpenCollective Backers
.. |sponsors| image:: https://opencollective.com/spyder/sponsors/badge.svg?color=blue
   :target: #sponsors
   :alt: OpenCollective Sponsors

Important Announcement: Spyder is unfunded!
-------------------------------------------

Since mid November/2017, `Anaconda, Inc`_ has
stopped funding Spyder development, after doing it for the past 18
months. Because of that, development will focus from now on maintaining
Spyder 3 at a much slower pace than before.

If you want to contribute to maintain Spyder, please consider donating at

https://opencollective.com/spyder

We appreciate all the help you can provide us and can't thank you enough for
supporting the work of Spyder devs and Spyder development.

If you want to know more about this, please read this
`page`_.


.. _Anaconda, Inc: https://www.anaconda.com/
.. _page: https://github.com/spyder-ide/spyder/wiki/Anaconda-stopped-funding-Spyder


Description
-----------

Changelog generator based on milestone or tags for github.


Example output
--------------

So how does this look in practice? It looks like this for 0.3 release of loghub:


::

    ## Version 0.3 (2017-10-10)

    ### Issues Closed

    #### Enhancements

    * [Issue 63](https://github.com/spyder-ide/loghub/issues/63) - Add PR link / commit link inside issue ([PR 69](https://github.com/spyder-ide/loghub/pull/69))

    In this release 1 issue was closed.

    ### Pull Requests Merged

    * [PR 69](https://github.com/spyder-ide/loghub/pull/69) - PR: Add extra links for related issues and prs ([63](https://github.com/spyder-ide/loghub/issues/63))

    In this release 1 pull request was closed.


You can look at `loghub's CHANGELOG.md`_, or `spyder's CHANGELOG.md`_ for
a more complete example output

.. _loghub's CHANGELOG.md: https://github.com/spyder-ide/loghub/blob/master/CHANGELOG.md
.. _spyder's CHANGELOG.md: https://github.com/spyder-ide/spyder/blob/master/CHANGELOG.md


Installation
------------

Using pip

::

    pip install loghub

Using conda

::

    conda install loghub -c conda-forge

or

::

    conda install loghub -c spyder-ide


Usage
-----

loghub can be used to generate changelog based on milestones or on tags.

In projects where milestones are used to track a release we can use for example:

.. code-block:: text

    loghub spyder-ide/spyder --milestone v3.0


In projects where milestones are used to track chunks of work but not releases,
we can use tags to get the changes after the latest release, for example:

.. code-block:: text

    loghub spyder-ide/spyder --since-tag v3.0.0b7


Or if loghub is used to generate old changelogs (or update changelogs),
we can also use tags to limit the range , for example:

.. code-block:: text

    loghub spyder-ide/spyder --since-tag v3.0.0b7 --until-tag v3.0.0


For private repos, just add the username and password arguments, for example:

.. code-block:: text

    loghub spyder-ide/spyder --since-tag v3.0.0b7 --since-tag v3.0.0 --username <username> --password <password>


Or, just add the username and a password prompt will appear, for example:

.. code-block:: text

    loghub spyder-ide/spyder --since-tag v3.0.0b7 --since-tag v3.0.0 --username <username>


Or generate a Github access token and use that instead, for example:

.. code-block:: text

    loghub spyder-ide/spyder --since-tag v3.0.0b7 -until-tag v3.0.0 --token <token>


**Important**

Because of the Github API rate limitations it is advised to always use authentication
by either access token or user and password.

    
Advanced Usage
--------------

Filter PR base branch
~~~~~~~~~~~~~~~~~~~~~

Pull requests to display can be filtered depending on the branch they were
merge against (base branch):
              
.. code-block:: text

    loghub spyder-ide/spyder --branch 3.x


Filter issues/PRs by labels
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To filter issues to display, we can use a regular expression:

.. code-block:: text

    loghub spyder-ide/spyder --issue-label-regex "Type.*" --milestone v3.1

This will filter all the issues that start with *Type*

The same can be done with PRs

.. code-block:: text

    loghub spyder-ide/spyder --pr-label-regex "<some-regex>" --milestone v3.1


Group issues by label
~~~~~~~~~~~~~~~~~~~~~

Issues displayed can be grouped by labels:

.. code-block:: text

    loghub spyder-ide/spyder --issue-label-group "Type-Bug" "Bugs Fixed" --issue-label-group "Type-Enhancement" "New Features" --milestone v3.1

This will result in issues being grouped in two sections with the headings
*Bugs Fixed* and *New Features* respectively.

Output format
~~~~~~~~~~~~~

Loghub provides two formats:

* ***changelog***, which is the default and includes links to issues and PRs
* ***release***, which does not include links

.. code-block:: text

    loghub spyder-ide/spyder --milestone v3.1 --format release

Custom templates
~~~~~~~~~~~~~~~~

Loghub uses Jinja2 templates to format the output. If the current template
does not your needs, you can copy the default `templates <https://github.com/spyder-ide/loghub/tree/master/loghub/templates>`_ 
and create a new one and provide the path to it as:

.. code-block:: text

    loghub spyder-ide/spyder --milestone v3.1 --template <PATH_TO_TEMPLATE>

Detailed CLI arguments
----------------------

.. code-block:: text

    usage: loghub [-h] [-m MILESTONE]
                  [-ilg ISSUE_LABEL_GROUPS [ISSUE_LABEL_GROUPS ...]]
                  [-ilr ISSUE_LABEL_REGEX] [-plr PR_LABEL_REGEX] [-st SINCE_TAG]
                  [-ut UNTIL_TAG] [-b BRANCH] [-f OUTPUT_FORMAT]
                  [--template TEMPLATE] [-u USERNAME] [-p PASSWORD] [-t TOKEN]
                  repository

    Script to print the list of issues and pull requests closed in a given
    milestone, tag including additional filtering options.

    positional arguments:
      repository            Repository name to generate the Changelog for, in the
                            form user/repo or org/repo (e.g. spyder-ide/spyder)

    optional arguments:
      -h, --help
                            Show this help message and exit

      -u USERNAME, --username USERNAME
                            Github user name

      -p PASSWORD, --password PASSWORD
                            Github user password

      -t TOKEN, --token TOKEN
                            Github access token

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

      --batch {milestones,tags}
                            Run loghub for all milestones or all tags
 
      --no-prs              Run loghub without any pull requests output

Label utility CLI arguments
---------------------------
loghub includes an additional utility to get or update labels.

.. code-block:: text

    usage: loghub-labels [-h] [-u USERNAME] [-p PASSWORD] [-t TOKEN]
                         [-a [{get,update}]] [-f FILENAME]
                         repository
    
    positional arguments:
      repository            Repository name to generate the Changelog for, in the
                            form user/repo or org/repo (e.g. spyder-ide/spyder)
    
    optional arguments:
      -h, --help            
                            show this help message and exit

      -u USERNAME, --username USERNAME
                            Github user name

      -p PASSWORD, --password PASSWORD
                            Github user password

      -t TOKEN, --token TOKEN
                            Github access token

      -a [{get,update}], --action [{get,update}]
                            Action to take

      -f FILENAME, --filename FILENAME
                            File for storing labels

Contributing
------------

Everyone is welcome to contribute!

Backers
~~~~~~~

Support us with a monthly donation and help us continue our activities.

.. image:: https://opencollective.com/spyder/backers.svg
   :target: https://opencollective.com/spyder#support
   :alt: Backers

Sponsors
~~~~~~~~

Become a sponsor to get your logo on our README on Github.

.. image:: https://opencollective.com/spyder/sponsors.svg
   :target: https://opencollective.com/spyder#support
   :alt: Sponsors

