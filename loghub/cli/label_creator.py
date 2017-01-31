# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Create github labels from a text file."""

# yapf: disable

# Standard library imports
import argparse

# Local imports
from loghub.cli.common import add_common_parser_args, parse_password_check_repo
from loghub.core.labels import process_labels


# yapf: enable


def main():
    """Main script."""
    parse_arguments(skip=False)


def parse_arguments(skip=False):
    """Parse argument for label creator utility."""
    # Get command-line arguments
    parser = argparse.ArgumentParser()

    parser = add_common_parser_args(parser)
    parser.add_argument(
        '-a',
        '--action',
        help='Action to take',
        type=str,
        choices=['get', 'update'],
        default='get',
        nargs='?')
    parser.add_argument(
        '-f',
        '--filename',
        help='File for storing labels',
        type=str,
        default='labels.txt')

    options = parser.parse_args()

    username = options.username
    password = parse_password_check_repo(options)

    if not skip:
        process_labels(
            username,
            password,
            options.token,
            options.action,
            options.repository,
            options.filename, )

    return options


if __name__ == '__main__':
    main()
