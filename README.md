# Loghub

## Project details

[![license](https://img.shields.io/pypi/l/loghub.svg)](./LICENSE.txt)
[![pypi version](https://img.shields.io/pypi/v/loghub.svg)](https://pypi.org/project/loghub/)
[![conda version](https://img.shields.io/conda/vn/conda-forge/loghub.svg)](https://www.anaconda.com/download/)
[![OpenCollective Backers](https://opencollective.com/spyder/backers/badge.svg?color=blue)](#backers)
[![OpenCollective Sponsors](https://opencollective.com/spyder/sponsors/badge.svg?color=blue)](#sponsors)
[![Join the chat at https://gitter.im/spyder-ide/public](https://badges.gitter.im/spyder-ide/spyder.svg)](https://gitter.im/spyder-ide/public)
[![PyPI status](https://img.shields.io/pypi/status/loghub.svg)](https://github.com/spyder-ide/loghub)

## Build status

[![Build status](https://github.com/spyder-ide/loghub/workflows/Tests%20master/badge.svg)](https://github.com/spyder-ide/loghub/actions?query=workflow%3A%22Tests+master%22)
[![Codecov](https://codecov.io/gh/spyder-ide/loghub/branch/master/graph/badge.svg)](https://codecov.io/gh/spyder-ide/loghub/branch/master)
[![Scrutinizer](https://scrutinizer-ci.com/g/spyder-ide/loghub/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/spyder-ide/loghub/?branch=master)

## Description

Changelog generator based on milestone or tags for github.

## Example output

So how does this look in practice? It looks like this for 0.3 release of loghub:

```Markdown
## Version 0.3 (2017-10-10)

### Issues Closed

#### Enhancements

* [Issue 63](https://github.com/spyder-ide/loghub/issues/63) - Add PR link / commit link inside issue ([PR 69](https://github.com/spyder-ide/loghub/pull/69))

In this release 1 issue was closed.

### Pull Requests Merged

* [PR 69](https://github.com/spyder-ide/loghub/pull/69) - PR: Add extra links for related issues and prs ([63](https://github.com/spyder-ide/loghub/issues/63))

In this release 1 pull request was closed.
```

You can look at [loghub's CHANGELOG.md](https://github.com/spyder-ide/loghub/blob/master/CHANGELOG.md), or
[spyder's CHANGELOG.md](https://github.com/spyder-ide/spyder/blob/master/CHANGELOG.md) for a more complete example output.


## Installation

Using pip

```bash
pip install loghub
````

Using conda

```bash
conda install loghub -c conda-forge
````

or

```bash
conda install loghub -c spyder-ide
```

## Usage

loghub can be used to generate changelog based on milestones or on tags.

In projects where milestones are used to track a release we can use for example:

```bash
loghub spyder-ide/spyder --milestone v3.0
```

In projects where milestones are used to track chunks of work but not releases,
we can use tags to get the changes after the latest release, for example:

```bash
loghub spyder-ide/spyder --since-tag v3.0.0b7
```

Or if loghub is used to generate old changelogs (or update changelogs),
we can also use tags to limit the range , for example:

```bash
loghub spyder-ide/spyder --since-tag v3.0.0b7 --until-tag v3.0.0
```

For private repos, just add the username and password arguments, for example:

```bash
loghub spyder-ide/spyder --since-tag v3.0.0b7 --since-tag v3.0.0 --username <username> --password <password>
```

Or, just add the username and a password prompt will appear, for example:

```bash
loghub spyder-ide/spyder --since-tag v3.0.0b7 --since-tag v3.0.0 --username <username>
```

Or generate a Github access token and use that instead, for example:

```bash
loghub spyder-ide/spyder --since-tag v3.0.0b7 -until-tag v3.0.0 --token <token>
```

**Important**

Because of the Github API rate limitations it is advised to always use authentication
by either access token or user and password.

## ZenHub Integration

If your project is using [Zenhub](https://www.zenhub.com/) to manage the workflow, you can also
use Zenhub releases to create your changelog.

```bash
loghub spyder-ide/spyder --zenhub-release "spyder v4.1.0" --zenhub-token <zenhub-token>
```

**Important**

For Zenhub integration to work you need to always use a zenhub token. You can generate one by
going to your [dashboard](https://app.zenhub.com/dashboard/tokens). Same GitHub API rate limits apply here so it is advised to always
use authentication by either access token or user and password.

```bash
loghub spyder-ide/spyder --zenhub-release "spyder v4.1.0" --zenhub-token <zenhub-token> --token <github-token>
```

## Advanced Usage

### Filter PR base branch

Pull requests to display can be filtered depending on the branch they were
merged against (base branch):
              
```bash
loghub spyder-ide/spyder --branch 3.x
```

### Filter issues/PRs by labels

To filter issues to display, we can use a regular expression:

```bash
loghub spyder-ide/spyder --issue-label-regex "Type.*" --milestone v3.1
```

This will filter all the issues that start with *Type*

The same can be done with PRs

```bash
loghub spyder-ide/spyder --pr-label-regex "<some-regex>" --milestone v3.1
```

### Group issues by label

Issues displayed can be grouped by labels:

```bash
loghub spyder-ide/spyder --issue-label-group "Type-Bug" "Bugs Fixed" --issue-label-group "Type-Enhancement" "New Features" --milestone v3.1
```

This will result in issues being grouped in two sections with the headings
*Bugs Fixed* and *New Features* respectively.

### Output format

Loghub provides two formats:

* ***changelog***, which is the default and includes links to issues and PRs
* ***release***, which does not include links

```bash
loghub spyder-ide/spyder --milestone v3.1 --format release
```

### Custom templates

Loghub uses Jinja2 templates to format the output. If the current template
does not meet your needs, you can copy the default `templates <https://github.com/spyder-ide/loghub/tree/master/loghub/templates>`_ 
and create a new one and provide the path to it as:

```bash
loghub spyder-ide/spyder --milestone v3.1 --template <PATH_TO_TEMPLATE>
```

## Detailed CLI arguments

```text
usage: loghub [-h] [-u USERNAME] [-p PASSWORD] [-t TOKEN] [-zt ZENHUB_TOKEN]
            [-m MILESTONE] [-zr ZENHUB_RELEASE] [-st SINCE_TAG]
            [-ut UNTIL_TAG] [-b BRANCH]
            [-ilg ISSUE_LABEL_GROUPS [ISSUE_LABEL_GROUPS ...]]
            [-plg PR_LABEL_GROUPS [PR_LABEL_GROUPS ...]]
            [-lg LABEL_GROUPS [LABEL_GROUPS ...]] [-ilr ISSUE_LABEL_REGEX]
            [-plr PR_LABEL_REGEX] [-f OUTPUT_FORMAT] [--template TEMPLATE]
            [--batch {milestones,tags}] [--no-prs]
            repository

Script to print the list of issues and pull requests closed in a given
milestone, tag including additional filtering options.

positional arguments:
repository            Repository name to generate the Changelog for, in the
                        form user/repo or org/repo (e.g. spyder-ide/spyder)

optional arguments:
-h, --help            show this help message and exit
-u USERNAME, --username USERNAME
                        Github user name
-p PASSWORD, --password PASSWORD
                        Github user password
-t TOKEN, --token TOKEN
                        Github access token
-zt ZENHUB_TOKEN, --zenhub-token ZENHUB_TOKEN
                        Zenhub access token
-m MILESTONE, --milestone MILESTONE
                        Github milestone to get issues and pull requests for
-zr ZENHUB_RELEASE, --zenhub-release ZENHUB_RELEASE
                        Zenhub release to get issues and pull requests for
-st SINCE_TAG, --since-tag SINCE_TAG
                        Github issues and pull requests since tag
-ut UNTIL_TAG, --until-tag UNTIL_TAG
                        Github issues and pull requests until tag
-b BRANCH, --branch BRANCH
                        Github base branch for merged PRs
-ilg ISSUE_LABEL_GROUPS [ISSUE_LABEL_GROUPS ...], --issue-label-group ISSUE_LABEL_GROUPS [ISSUE_LABEL_GROUPS ...]
                        Groups the generated issues by the specified label.
                        This optiontakes 1 or 2 arguments, where the first one
                        is the label to match and the second one is the label
                        to print on the finaloutput
-plg PR_LABEL_GROUPS [PR_LABEL_GROUPS ...], --pr-label-group PR_LABEL_GROUPS [PR_LABEL_GROUPS ...]
                        Groups the generated PRs by the specified label. This
                        optiontakes 1 or 2 arguments, where the first one is
                        the label to match and the second one is the label to
                        print on the finaloutput
-lg LABEL_GROUPS [LABEL_GROUPS ...], --label-group LABEL_GROUPS [LABEL_GROUPS ...]
                        Groups the generated issues and PRs by the specified
                        label. This option takes 1 or 2 arguments, where the
                        first one is the label to match and the second one is
                        the label to print on the final output
-ilr ISSUE_LABEL_REGEX, --issue-label-regex ISSUE_LABEL_REGEX
                        Label issue filter using a regular expression filter
-plr PR_LABEL_REGEX, --pr-label-regex PR_LABEL_REGEX
                        Label pull request filter using a regular expression
                        filter
-f OUTPUT_FORMAT, --format OUTPUT_FORMAT
                        Format for print, either 'changelog' (for Changelog.md
                        file) or 'release' (for the Github Releases page).
                        Default is 'changelog'. The 'release' option doesn't
                        generate Markdown hyperlinks.
--template TEMPLATE   Use a custom Jinja2 template file
--batch {milestones,tags}
                        Run loghub for all milestones or all tags
--no-prs              Run loghub without any pull requests output
--no-related-prs      Do not display related prs on issues
--no-related-issues   Do not display related issues on prs
```

## Label utility CLI arguments

loghub includes an additional utility to get or update labels.

```text
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
```

## Contributing

Everyone is welcome to contribute!

### Backers

Support us with a monthly donation and help us continue our activities.

[![Backers](https://opencollective.com/spyder/backers.svg)](https://opencollective.com/spyder#support)

### Sponsors

Become a sponsor to get your logo on our README on Github.

[![Sponsors](https://opencollective.com/spyder/sponsors.svg)](https://opencollective.com/spyder#support)
