# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Tests changelog output."""

# Standard library imports
import os
import sys
import tempfile

# Third party imports
from mock import patch
import pytest

# Local imports
from loghub.cli.main import create_changelog, parse_arguments

REPO = 'spyder-ide/loghub'
TEST_TOKEN = os.environ.get('TEST_TOKEN', '').replace('x', '')
TEST_USER = os.environ.get('TEST_USER', '').replace('x', '')
TEST_PASS = os.environ.get('TEST_CODE', '').replace('x', '')
TEST_MILESTONE = 'test-milestone'
TEST_MILESTONE_REAL = 'v0.2'
TEST_TAG = 'v0.1.2'
NOT_ON_CI = os.environ.get('CIRCLECI') != 'true'


# --- Tests
# -----------------------------------------------------------------------------
@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_changelog_loghub_real_milestone():
    log = create_changelog(
        repo=REPO,
        token=TEST_TOKEN,
        milestone=TEST_MILESTONE_REAL,
        branch='master',
        output_format='changelog')
    expected = '''## Version 0.2 (2017-02-01)

### Issues Closed

* [Issue 64](https://github.com/spyder-ide/loghub/issues/64) - Create release for v0.2
* [Issue 57](https://github.com/spyder-ide/loghub/issues/57) - Allow Enable/Disable of PR output ([PR 65](https://github.com/spyder-ide/loghub/pull/65))
* [Issue 56](https://github.com/spyder-ide/loghub/issues/56) - Fix output for grouped labels if no items on that group ([PR 58](https://github.com/spyder-ide/loghub/pull/58))
* [Issue 55](https://github.com/spyder-ide/loghub/issues/55) - Fix date on generation based on milestone ([PR 58](https://github.com/spyder-ide/loghub/pull/58))
* [Issue 53](https://github.com/spyder-ide/loghub/issues/53) - Normalize CI files using requirements.txt ([PR 60](https://github.com/spyder-ide/loghub/pull/60))
* [Issue 52](https://github.com/spyder-ide/loghub/issues/52) - Update README to use full commands ([PR 58](https://github.com/spyder-ide/loghub/pull/58))
* [Issue 47](https://github.com/spyder-ide/loghub/issues/47) - Update Appveyor Badge for new username spyder-ide ([PR 48](https://github.com/spyder-ide/loghub/pull/48))
* [Issue 46](https://github.com/spyder-ide/loghub/issues/46) - Create labels automagically on github based on template ([PR 59](https://github.com/spyder-ide/loghub/pull/59))
* [Issue 42](https://github.com/spyder-ide/loghub/issues/42) - Generate all changelog based on milestones
* [Issue 41](https://github.com/spyder-ide/loghub/issues/41) - Add default template for release with issue label grouping ([PR 43](https://github.com/spyder-ide/loghub/pull/43))
* [Issue 40](https://github.com/spyder-ide/loghub/issues/40) - Provide available milestones to user when provided not found ([PR 44](https://github.com/spyder-ide/loghub/pull/44))
* [Issue 39](https://github.com/spyder-ide/loghub/issues/39) - Add checkignore to quantified code
* [Issue 30](https://github.com/spyder-ide/loghub/issues/30) - Add label groupings ([PR 34](https://github.com/spyder-ide/loghub/pull/34))
* [Issue 28](https://github.com/spyder-ide/loghub/issues/28) - Generate all changelog based on tags ([PR 61](https://github.com/spyder-ide/loghub/pull/61))
* [Issue 27](https://github.com/spyder-ide/loghub/issues/27) - Generate all changelog based on milestones ([PR 61](https://github.com/spyder-ide/loghub/pull/61))
* [Issue 23](https://github.com/spyder-ide/loghub/issues/23) - Update Readme with new CLI parameters ([PR 36](https://github.com/spyder-ide/loghub/pull/36))
* [Issue 21](https://github.com/spyder-ide/loghub/issues/21) - Add branch parameter to select PRs to display based on the merging branch ([PR 32](https://github.com/spyder-ide/loghub/pull/32))
* [Issue 16](https://github.com/spyder-ide/loghub/issues/16) - Better authorization handling  ([PR 44](https://github.com/spyder-ide/loghub/pull/44))
* [Issue 15](https://github.com/spyder-ide/loghub/issues/15) - Since tag not working properly ([PR 13](https://github.com/spyder-ide/loghub/pull/13))
* [Issue 11](https://github.com/spyder-ide/loghub/issues/11) - Support hidden password ([PR 14](https://github.com/spyder-ide/loghub/pull/14))
* [Issue 10](https://github.com/spyder-ide/loghub/issues/10) - Support custom line formats [templates] ([PR 20](https://github.com/spyder-ide/loghub/pull/20))
* [Issue 8](https://github.com/spyder-ide/loghub/issues/8) - Support "all issues"  ([PR 19](https://github.com/spyder-ide/loghub/pull/19))
* [Issue 4](https://github.com/spyder-ide/loghub/issues/4) - Expose labels for additional filtering ([PR 17](https://github.com/spyder-ide/loghub/pull/17))
* [Issue 3](https://github.com/spyder-ide/loghub/issues/3) - Add access token interface ([PR 18](https://github.com/spyder-ide/loghub/pull/18))
* [Issue 2](https://github.com/spyder-ide/loghub/issues/2) - Add some basic tests ([PR 29](https://github.com/spyder-ide/loghub/pull/29))

In this release 25 issues were closed.

### Pull Requests Merged

* [PR 65](https://github.com/spyder-ide/loghub/pull/65) - PR: Add support for no-prs on output ([57](https://github.com/spyder-ide/loghub/issues/57))
* [PR 61](https://github.com/spyder-ide/loghub/pull/61) - PR: Add batch mode for all tags for all milestones ([28](https://github.com/spyder-ide/loghub/issues/28), [27](https://github.com/spyder-ide/loghub/issues/27))
* [PR 60](https://github.com/spyder-ide/loghub/pull/60) - PR: Add requirements file and update CI process ([53](https://github.com/spyder-ide/loghub/issues/53))
* [PR 59](https://github.com/spyder-ide/loghub/pull/59) - PR: Add a label creator utility ([46](https://github.com/spyder-ide/loghub/issues/46))
* [PR 58](https://github.com/spyder-ide/loghub/pull/58) - PR: Refactor code and simplify group handling ([56](https://github.com/spyder-ide/loghub/issues/56), [55](https://github.com/spyder-ide/loghub/issues/55), [52](https://github.com/spyder-ide/loghub/issues/52))
* [PR 54](https://github.com/spyder-ide/loghub/pull/54) - PR: Remove versioneer
* [PR 51](https://github.com/spyder-ide/loghub/pull/51) - PR: Update ignore file to ignore versioneer files
* [PR 50](https://github.com/spyder-ide/loghub/pull/50) - PR: Add versioneer for version string control based on git tags not on manual editing ([49](https://github.com/spyder-ide/loghub/issues/49))
* [PR 48](https://github.com/spyder-ide/loghub/pull/48) - PR: Update AppVeyor badge because of move to org account ([47](https://github.com/spyder-ide/loghub/issues/47))
* [PR 45](https://github.com/spyder-ide/loghub/pull/45) - PR: Break into smaller funcs
* [PR 44](https://github.com/spyder-ide/loghub/pull/44) - PR: Improve error handling ([40](https://github.com/spyder-ide/loghub/issues/40), [16](https://github.com/spyder-ide/loghub/issues/16))
* [PR 43](https://github.com/spyder-ide/loghub/pull/43) - PR: Add template for release grouped issue labels ([41](https://github.com/spyder-ide/loghub/issues/41))
* [PR 36](https://github.com/spyder-ide/loghub/pull/36) - PR: Update readme with latest CLI commands ([23](https://github.com/spyder-ide/loghub/issues/23))
* [PR 34](https://github.com/spyder-ide/loghub/pull/34) - PR: Add label grouping for issues  ([30](https://github.com/spyder-ide/loghub/issues/30))
* [PR 32](https://github.com/spyder-ide/loghub/pull/32) - PR: Feature/branch ([21](https://github.com/spyder-ide/loghub/issues/21))
* [PR 31](https://github.com/spyder-ide/loghub/pull/31) - PR: Refactor code
* [PR 29](https://github.com/spyder-ide/loghub/pull/29) - PR: Maintenance/tests ([2](https://github.com/spyder-ide/loghub/issues/2))
* [PR 20](https://github.com/spyder-ide/loghub/pull/20) - PR: Feature/templates ([10](https://github.com/spyder-ide/loghub/issues/10))
* [PR 19](https://github.com/spyder-ide/loghub/pull/19) - PR: Add support for all issues when no tag or no milestone is provided ([8](https://github.com/spyder-ide/loghub/issues/8))
* [PR 18](https://github.com/spyder-ide/loghub/pull/18) - PR: Add support for github tokens ([3](https://github.com/spyder-ide/loghub/issues/3))
* [PR 17](https://github.com/spyder-ide/loghub/pull/17) - PR: Add regex label filtering for issues and prs ([4](https://github.com/spyder-ide/loghub/issues/4))
* [PR 14](https://github.com/spyder-ide/loghub/pull/14) - add password prompt when user is specified and password is blank ([11](https://github.com/spyder-ide/loghub/issues/11))
* [PR 13](https://github.com/spyder-ide/loghub/pull/13) - PR: Fix bug on since keyword returning incorrect issues ([15](https://github.com/spyder-ide/loghub/issues/15))
* [PR 12](https://github.com/spyder-ide/loghub/pull/12) - Don't test macOS in Travis
* [PR 9](https://github.com/spyder-ide/loghub/pull/9) - Don't show "Issues" or "Pull requests" sections if there are no issues or PRs to show
* [PR 7](https://github.com/spyder-ide/loghub/pull/7) - Fix contents of temporary file
* [PR 6](https://github.com/spyder-ide/loghub/pull/6) - Remove extra empty lines
* [PR 5](https://github.com/spyder-ide/loghub/pull/5) - Fix PR_SHORT formatting.
* [PR 1](https://github.com/spyder-ide/loghub/pull/1) - Several fixes

In this release 29 pull requests were closed.
'''
    print([log])
    print([expected])
    assert log == expected


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_changelog():
    log = create_changelog(
        repo=REPO,
        token=TEST_TOKEN,
        milestone=TEST_MILESTONE,
        branch='master',
        output_format='changelog')
    expected = '''## Version test-milestone (2016-12-05)

### Issues Closed

* [Issue 77](https://github.com/spyder-ide/loghub/issues/77) - Test empty body
* [Issue 26](https://github.com/spyder-ide/loghub/issues/26) - Test number 2
* [Issue 24](https://github.com/spyder-ide/loghub/issues/24) - Issue test

In this release 3 issues were closed.

### Pull Requests Merged

* [PR 25](https://github.com/spyder-ide/loghub/pull/25) - PR: Add tests folder

In this release 1 pull request was closed.
'''
    print([log])
    print([expected])
    assert log == expected


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_changelog_release():
    log = create_changelog(
        repo=REPO,
        token=TEST_TOKEN,
        milestone=TEST_MILESTONE,
        branch='master',
        output_format='release')
    expected = '''## Version test-milestone (2016-12-05)

### Issues Closed

* Issue #77 - Test empty body
* Issue #26 - Test number 2
* Issue #24 - Issue test

In this release 3 issues were closed.

### Pull Requests Merged

* PR #25 - PR: Add tests folder

In this release 1 pull request was closed.
'''
    print([log])
    print([expected])
    assert log == expected


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_changelog_release_branch():
    log = create_changelog(
        repo=REPO,
        token=TEST_TOKEN,
        milestone=TEST_MILESTONE,
        branch='test-branch',
        output_format='release')
    expected = '''## Version test-milestone (2016-12-05)

### Issues Closed

* Issue #77 - Test empty body
* Issue #26 - Test number 2
* Issue #24 - Issue test

In this release 3 issues were closed.

### Pull Requests Merged

* PR #84 - Test no issue number in PR's body
* PR #33 - PR: Test change

In this release 2 pull requests were closed.
'''
    print([log])
    print([expected])
    assert log == expected


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_changelog_groups():
    issue_label_groups = [{'label': 'type:bug', 'name': 'Bugs fixed'}]
    log = create_changelog(
        repo=REPO,
        token=TEST_TOKEN,
        milestone=TEST_MILESTONE,
        branch='test-branch',
        issue_label_groups=issue_label_groups)
    expected = '''## Version test-milestone (2016-12-05)

### Issues Closed

#### Bugs fixed

* [Issue 26](https://github.com/spyder-ide/loghub/issues/26) - Test number 2

In this release 1 issue was closed.

### Pull Requests Merged

* [PR 84](https://github.com/spyder-ide/loghub/pull/84) - Test no issue number in PR's body
* [PR 33](https://github.com/spyder-ide/loghub/pull/33) - PR: Test change

In this release 2 pull requests were closed.
'''
    print([log])
    print([expected])
    assert log == expected


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_changelog_template():
    template = '''{%   for i in issues -%}
* Issue #{{ i['number'] }} - {{ i['title'] }}
{%   endfor %}'''
    desc, path = tempfile.mkstemp()
    with open(path, 'w') as f:
        f.write(template)

    log = create_changelog(
        repo=REPO,
        token=TEST_TOKEN,
        milestone=TEST_MILESTONE,
        template_file=path)
    expected = '* Issue #77 - Test empty body\n* Issue #26 - Test number 2\n* Issue #24 - Issue test\n'
    print([log])
    print([expected])
    assert log == expected


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_argument_parser_invalid():
    args = ['prog']
    with pytest.raises(SystemExit):
        with patch.object(sys, 'argv', args):
            parse_arguments(skip=True)


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_argument_parser_valid():
    args = [
        'prog', 'spyder-ide/loghub', '-ilg', 'type:bug', 'Bugs fixed', '-t',
        TEST_TOKEN
    ]
    with patch.object(sys, 'argv', args):
        options = parse_arguments()
    assert options.issue_label_groups == [['type:bug', 'Bugs fixed']]
