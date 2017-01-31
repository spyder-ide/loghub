# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Build a list of issues and pull requests per Github milestone."""

# yapf: disable

from __future__ import print_function

# Standard library imports
import argparse
import sys

# Local imports
from loghub.cli.common import add_common_parser_args, parse_password_check_repo
from loghub.core.formatter import create_changelog

# yapf: enable

PY2 = sys.version[0] == '2'


def main():
    """Main script."""
    parse_arguments(skip=False)


def parse_arguments(skip=False):
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description='Script to print the list of issues and pull requests '
        'closed in a given milestone, tag including additional filtering '
        'options.')

    # Get common parser arguments
    parser = add_common_parser_args(parser)

    parser.add_argument(
        '-m',
        '--milestone',
        action="store",
        dest="milestone",
        default='',
        help="Github milestone to get issues and pull requests for")
    parser.add_argument(
        '-st',
        '--since-tag',
        action="store",
        dest="since_tag",
        default='',
        help="Github issues and pull requests since tag")
    parser.add_argument(
        '-ut',
        '--until-tag',
        action="store",
        dest="until_tag",
        default='',
        help="Github issues and pull requests until tag")
    parser.add_argument(
        '-b',
        '--branch',
        action="store",
        dest="branch",
        default='',
        help="Github base branch for merged PRs")
    parser.add_argument(
        '-ilg',
        '--issue-label-group',
        action="append",
        nargs='+',
        dest="issue_label_groups",
        help="Groups the generated issues by the specified label. This option"
        "Takes 1 or 2 arguments, where the first one is the label to "
        "match and the second one is the label to print on the final"
        "output")
    parser.add_argument(
        '-ilr',
        '--issue-label-regex',
        action="store",
        dest="issue_label_regex",
        default='',
        help="Label issue filter using a regular expression filter")
    parser.add_argument(
        '-plr',
        '--pr-label-regex',
        action="store",
        dest="pr_label_regex",
        default='',
        help="Label pull requets filter using a regular expression filter")
    parser.add_argument(
        '-f',
        '--format',
        action="store",
        dest="output_format",
        default='changelog',
        help="Format for print, either 'changelog' (for "
        "Changelog.md file) or 'release' (for the Github "
        "Releases page). Default is 'changelog'. The "
        "'release' option doesn't generate Markdown "
        "hyperlinks.")
    parser.add_argument(
        '--template',
        action="store",
        dest="template",
        default='',
        help="Use a custom Jinja2 template file ")
    parser.add_argument(
        '--batch',
        action="store",
        dest="batch",
        default=None,
        choices=['milestones', 'tags'],
        help="Run loghub for all milestones or all tags")
    parser.add_argument(
        '--no-prs',
        action="store_false",
        dest="show_prs",
        default=True,
        help="Run loghub without any pull requests output")

    options = parser.parse_args()

    milestone = options.milestone
    batch = options.batch

    # Check if milestone or tag given
    if not batch:
        if not milestone and not options.since_tag:
            print('\nLOGHUB: Querying all issues\n')
        elif milestone:
            print('\nLOGHUB: Querying issues for milestone {0}'
                  '\n'.format(milestone))
        elif options.since_tag and not options.until_tag:
            print('\nLOGHUB: Querying issues since tag {0}'
                  '\n'.format(options.since_tag))
        elif options.since_tag and options.until_tag:
            print('\nLOGHUB: Querying issues since tag {0} until tag {1}'
                  '\n'.format(options.since_tag, options.until_tag))
    elif batch and any([
            bool(options.since_tag), bool(options.until_tag),
            bool(options.milestone)
    ]):
        print('LOGHUB: When using batch mode no tags or milestone arguments '
              'are allowed.\n')
        sys.exit(1)

    # Ask for password once input is valid
    username = options.username
    password = parse_password_check_repo(options)
    issue_label_groups = options.issue_label_groups

    new_issue_label_groups = []
    if issue_label_groups:
        for item in issue_label_groups:
            dic = {}
            if len(item) == 1:
                dic['label'] = item[0]
                dic['name'] = item[0]
            elif len(item) == 2:
                dic['label'] = item[0]
                dic['name'] = item[1]
            else:
                print('LOGHUB: Issue label group takes 1 or 2 arguments\n')
                sys.exit(1)
            new_issue_label_groups.append(dic)

    if not skip:
        create_changelog(
            repo=options.repository,
            username=username,
            password=password,
            token=options.token,
            milestone=milestone,
            since_tag=options.since_tag,
            until_tag=options.until_tag,
            branch=options.branch,
            issue_label_regex=options.issue_label_regex,
            pr_label_regex=options.pr_label_regex,
            output_format=options.output_format,
            template_file=options.template,
            issue_label_groups=new_issue_label_groups,
            batch=batch,
            show_prs=options.show_prs)

    return options


if __name__ == '__main__':  # yapf: disable
    main()
