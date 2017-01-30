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
TEST_TAG = 'v0.1.2'
NOT_ON_CI = os.environ.get('CIRCLECI') != 'true'


# --- Tests
# -----------------------------------------------------------------------------
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

* [Issue 26](https://github.com/spyder-ide/loghub/issues/26) - Test number 2
* [Issue 24](https://github.com/spyder-ide/loghub/issues/24) - Issue test

In this release 2 issues were closed.

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

* Issue #26 - Test number 2
* Issue #24 - Issue test

In this release 2 issues were closed.

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

* Issue #26 - Test number 2
* Issue #24 - Issue test

In this release 2 issues were closed.

### Pull Requests Merged

* PR #33 - PR: Test change

In this release 1 pull request was closed.
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

* [PR 33](https://github.com/spyder-ide/loghub/pull/33) - PR: Test change

In this release 1 pull request was closed.
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
    expected = '* Issue #26 - Test number 2\n* Issue #24 - Issue test\n'
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
