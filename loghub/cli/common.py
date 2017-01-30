# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Common CLI utilities."""

# yapf: disable

from __future__ import print_function

# Standard library imports
import getpass
import sys


# yapf: enable


def add_common_parser_args(parser):
    """Parse CLI common login and repo arguments."""
    parser.add_argument(
        'repository',
        help="Repository name to generate the Changelog for, in the form "
        "user/repo or org/repo (e.g. spyder-ide/spyder)")
    parser.add_argument(
        '-u',
        '--username',
        action="store",
        dest="username",
        default='',
        help="Github user name")
    parser.add_argument(
        '-p',
        '--password',
        action="store",
        dest="password",
        default='',
        help="Github user password")
    parser.add_argument(
        '-t',
        '--token',
        action="store",
        dest="token",
        default='',
        help="Github access token")

    return parser


def parse_password_check_repo(options):
    """Check password and prompt if missing and check repo is provided."""
    if options.username and not options.password:
        password = getpass.getpass()
    else:
        password = options.password

    # Check if repo given
    if not options.repository:
        print('LOGHUB: Please define a repository name to this script. '
              'See its help')
        sys.exit(1)
    return password
