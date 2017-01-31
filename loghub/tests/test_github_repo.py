# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Tests github repo."""

# Standard library imports
import os

# Third party imports
import pytest

# Local imports
from loghub.core.repo import GitHubRepo
from loghub.external.github import ApiError

REPO = 'spyder-ide/loghub'
TEST_TOKEN = os.environ.get('TEST_TOKEN', '').replace('x', '')
TEST_USER = os.environ.get('TEST_USER', '').replace('x', '')
TEST_PASS = os.environ.get('TEST_CODE', '').replace('x', '')
TEST_MILESTONE = 'test-milestone'
TEST_TAG = 'v0.1.2'
NOT_ON_CI = os.environ.get('CIRCLECI') != 'true'


# --- Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def gh_repo():
    return GitHubRepo(token=TEST_TOKEN, repo=REPO)


# --- Tests
# -----------------------------------------------------------------------------
@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_valid_user_password():
    gh = GitHubRepo(username=TEST_USER, password=TEST_PASS, repo=REPO)
    assert bool(gh.milestone(TEST_MILESTONE))


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_invalid_user_password():
    with pytest.raises(SystemExit):
        gh = GitHubRepo(
            username='invalid-user',
            password='invalid-password',
            repo=REPO, )
        gh.milestone(TEST_MILESTONE)


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_valid_token():
    gh = GitHubRepo(token=TEST_TOKEN, repo=REPO)
    gh.milestone(TEST_MILESTONE)


def test_invalid_token():
    with pytest.raises(SystemExit):
        gh = GitHubRepo(token='this-is-an-invalid-token', repo=REPO)
        gh.milestone(TEST_MILESTONE)


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_tags(gh_repo):
    tags = gh_repo.tags()
    titles = [tag['ref'].replace('refs/tags/', '') for tag in tags]
    assert TEST_TAG in titles


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_valid_tag(gh_repo):
    tag = gh_repo.tag(TEST_TAG)
    assert bool(tag)


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_invalid_tag(gh_repo):
    with pytest.raises(SystemExit):
        gh_repo.tag('invalid-tag')


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_milestones(gh_repo):
    milestones = gh_repo.milestones()
    titles = [milestone['title'] for milestone in milestones]
    assert TEST_MILESTONE in titles


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_valid_milestone(gh_repo):
    assert bool(gh_repo.milestone(TEST_MILESTONE))


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_invalid_milestone(gh_repo):
    with pytest.raises(SystemExit):
        gh_repo.milestone('invalid-milestone')


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_issues(gh_repo):
    issues = gh_repo.issues(milestone=TEST_MILESTONE, state='closed')
    assert len(issues) == 4


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_pr_merged(gh_repo):
    assert gh_repo.is_merged(25)


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_pr_closed(gh_repo):
    assert not gh_repo.is_merged(22)


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_pr_valid(gh_repo):
    pr = gh_repo.pr(32)
    assert bool(pr)


@pytest.mark.skipif(NOT_ON_CI, reason='test on ci server only')
def test_pr_invalid(gh_repo):
    with pytest.raises(ApiError):
        gh_repo.pr(1000000)


def test_dates():
    date = GitHubRepo.str_to_date('2016-10-10T08:08:08Z')
    assert date.year == 2016
    assert date.month == 10
    assert date.day == 10
    assert date.hour == 8
    assert date.minute == 8
    assert date.second == 8
