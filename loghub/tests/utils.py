# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Tests utils."""


class Issue:
    """Issue github mock."""

    def __init__(self, number, user='test-user', full_repo='foo/bar', body=None, is_pr=False):
        self.pull_request = is_pr
        self.number = number
        self.body = body or ''
        self.user = {'login': user, 'html_url': 'https://github.com/{}'.format(user)}

        if is_pr:
            self.html_url = 'https://github.com/{}/pull/{}'.format(full_repo, number)
        else:
            self.html_url = 'https://github.com/{}/issues/{}'.format(full_repo, number)

    def __repr__(self):
        return repr(self.__dict__)

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def get(self, name, default=None):
        if default is None:
            return self.__dict__.get(name)
        else:
            return self.__dict__.get(name, default)
