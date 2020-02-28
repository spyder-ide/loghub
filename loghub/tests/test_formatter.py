# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Tests formatter."""

# Standard library imports
import os

# Third party imports
import pytest

# Local imports
from loghub.core.formatter import filter_issues_fixed_by_prs
from loghub.tests.utils import Issue


# --- Tests
# -----------------------------------------------------------------------------
def test_filter_issues_fixed_by_prs_no_show():
    issues = [
        Issue(number=34),
        Issue(number=35),
    ]
    prs = [
        Issue(body='Fixes #34', is_pr=True, number=45),
        Issue(body='Closes #35', is_pr=True, number=46),
    ]

    new_issues, new_prs = filter_issues_fixed_by_prs(
        issues, prs, show_related_prs=False, show_related_issues=False
    )
    assert not all(bool(issue['loghub_related_pulls']) for issue in new_issues)
    assert not all(bool(pr['loghub_related_issues']) for pr in new_prs)


def test_filter_issues_fixed_by_prs_no_show_issues():
    issues = [
        Issue(number=34),
        Issue(number=35),
    ]
    prs = [
        Issue(body='Fixes #34', is_pr=True, number=45),
        Issue(body='Closes #35', is_pr=True, number=46),
    ]

    new_issues, new_prs = filter_issues_fixed_by_prs(
        issues, prs, show_related_prs=True, show_related_issues=False
    )
    assert all(bool(issue['loghub_related_pulls']) for issue in new_issues)
    assert not all(bool(pr['loghub_related_issues']) for pr in new_prs)


def test_filter_issues_fixed_by_prs_no_show_pulls():
    issues = [
        Issue(number=34),
        Issue(number=35),
    ]
    prs = [
        Issue(body='Fixes #34', is_pr=True, number=45),
        Issue(body='Closes #35', is_pr=True, number=46),
    ]

    new_issues, new_prs = filter_issues_fixed_by_prs(
        issues, prs, show_related_prs=False, show_related_issues=True
    )
    assert not all(bool(issue['loghub_related_pulls']) for issue in new_issues)
    assert all(bool(pr['loghub_related_issues']) for pr in new_prs)


def test_filter_issues_fixed_by_prs_show():
    issues = [
        Issue(number=34),
        Issue(number=35),
    ]
    prs = [
        Issue(body='Fixes #34', is_pr=True, number=45),
        Issue(body='Closes #35', is_pr=True, number=46),
    ]

    new_issues, new_prs = filter_issues_fixed_by_prs(
        issues, prs, show_related_prs=True, show_related_issues=True
    )
    assert all(bool(issue['loghub_related_pulls']) for issue in new_issues)
    assert all(bool(pr['loghub_related_issues']) for pr in new_prs)
