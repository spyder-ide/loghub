# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Tests changelog labels."""

# Standard library imports
import os
import tempfile

# Third party imports
from mock import patch
import pytest

# Local imports
from loghub.core.labels import process_labels


# --- Mocks
# ----------------------------------------------------------------------------
class Label:

    def __init__(self, name, color):
        self.name = name
        self.color = color


class GHRepo:

    def __init__(self, *args, **kwargs):
        pass

    def labels(self):
        return [Label('foo', '#ff00ff'), Label('bar', '#0000ff')]

    def set_labels(self, labels):
        GHRepo._labels = labels


# --- Tests
# ----------------------------------------------------------------------------
def test_invalid_action_labels():
    _, tempfilepath = tempfile.mkstemp()

    with patch('loghub.core.labels.GitHubRepo', new=GHRepo) as ghrepo:
        with pytest.raises(ValueError):
            process_labels('', '', '', 'BOOM', 'monty-repo', tempfilepath)

        with open(tempfilepath, 'r') as fh:
            data = fh.read()

        assert data == ''


def test_get_labels():
    _, tempfilepath = tempfile.mkstemp()

    with patch('loghub.core.labels.GitHubRepo', new=GHRepo) as gh_repo:
        process_labels('', '', '', 'get', 'monty-repo', tempfilepath)

        with open(tempfilepath, 'r') as fh:
            data = fh.read()

        assert data == 'bar;#0000ff\nfoo;#ff00ff'


def test_set_labels_2_parts():
    _, tempfilepath = tempfile.mkstemp()

    with open(tempfilepath, 'w') as fh:
        data = fh.write('bar;#0000ff\nfoo;#ff00ff')

    with patch('loghub.core.labels.GitHubRepo', new=GHRepo) as gh_repo:
        process_labels('', '', '', 'update', 'monty-repo', tempfilepath)
        assert gh_repo._labels == [
            {'new_name': 'bar', 'old_name': 'bar', 'color': '#0000ff'},
            {'new_name': 'foo', 'old_name': 'foo', 'color': '#ff00ff'},
        ]


def test_set_labels_3_parts():
    _, tempfilepath = tempfile.mkstemp()

    with open(tempfilepath, 'w') as fh:
        data = fh.write('old_bar;bar;#0000ff\nold_foo;foo;#ff00ff')

    with patch('loghub.core.labels.GitHubRepo', new=GHRepo) as gh_repo:
        process_labels('', '', '', 'update', 'monty-repo', tempfilepath)
        assert gh_repo._labels == [
            {'new_name': 'bar', 'old_name': 'old_bar', 'color': '#0000ff'},
            {'new_name': 'foo', 'old_name': 'old_foo', 'color': '#ff00ff'},
        ]
