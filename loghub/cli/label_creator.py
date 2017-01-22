# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Create github labels from a text file."""

from __future__ import print_function

# Standard library imports
import argparse
import getpass
import re
import sys
import time

# Third party imports
from jinja2 import Template

# Local imports
# yapf: disable
from loghub.repo import GitHubRepo
from loghub.templates import (CHANGELOG_GROUPS_TEMPLATE_PATH,
                              CHANGELOG_TEMPLATE_PATH,
                              RELEASE_GROUPS_TEMPLATE_PATH,
                              RELEASE_TEMPLATE_PATH)

# yapf: enable

PY2 = sys.version[0] == '2'


def main():
    """Main script."""
    parse_arguments(skip=False)


def parse_arguments(skip=False):
    """Parse CLI arguments."""
    # Cli options
    parser = argparse.ArgumentParser(
        description='Script to print the list of issues and pull requests '
        'closed in a given milestone, tag including additional filtering '
        'options.')
    parser.add_argument(
        'repository',
        help="Repository name to generate the Changelog for, in the form "
        "user/repo or org/repo (e.g. spyder-ide/spyder)")
    parser.add_argument(
        '-m',
        '--milestone',
        action="store",
        dest="milestone",
        default='',
        help="Github milestone to get issues and pull requests for")
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
        '-u',
        '--user',
        action="store",
        dest="user",
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
    options = parser.parse_args()

    username = options.user
    password = options.password
    milestone = options.milestone
    issue_label_groups = options.issue_label_groups

    if username and not password:
        password = getpass.getpass()

    # Check if repo given
    if not options.repository:
        print('LOGHUB: Please define a repository name to this script. '
              'See its help')
        sys.exit(1)

    # Check if milestone or tag given
    if not milestone and not options.since_tag:
        print('\nLOGHUB: Querying all issues\n')
    elif milestone:
        print('\nLOGHUB: Querying issues for milestone {0}'
              '\n'.format(milestone))

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
            issue_label_groups=new_issue_label_groups)

    return options


def get_token():
    r"""
    Get the API token to use for talking to GitHub
    """
    try:
        with open('token', 'rt') as token_file:
            return token_file.readline()[:-1]
    except IOError:
        import os
        return os.environ['GITHUB_TOKEN']


if __name__ == '__main__':
    import argparse

    # Get command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('repository', help='Repository', type=str)
    parser.add_argument('-o', '--org', help='Organization', type=str, default='Unidata')
    parser.add_argument('action', help='Action to take', type=str, choices=['get', 'update'],
                        default='get', nargs='?')
    parser.add_argument('-f', '--filename', help='File for storing labels', type=str,
                        default='labels.txt')
    args = parser.parse_args()

    # Get the github API entry
    token = get_token()
    g = github.Github(token)

    # Get the organization
    org = g.get_organization(args.org)

    # Get the object for this repository
    repo = org.get_repo(args.repository)

    #
    if args.action == 'get':
        print('Getting labels from {0}'.format(args.repository))
        with open(args.filename, 'wt') as outfile:
            labels = sorted((l.name, l.color) for l in repo.get_labels())
            outfile.write(''.join('{0}|{1}\n'.format(*l) for l in labels))
    elif args.action == 'update':
        if token is None:
            raise RuntimeError('Updating labels requires a personal access token!')
        print('Updating labels on {0}'.format(args.repository))
        with open(args.filename, 'rt') as infile:
            for line in infile:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    old_name, new_name, color = parts
                else:
                    new_name, color = parts
                    old_name = new_name

                try:
                    label = repo.get_label(old_name)
                    label.edit(new_name, color)
                    print('Updated label: {0.name}->{1} (#{2})'.format(label, new_name, color))
                except github.GithubException:
                    label = repo.create_label(new_name, color)
                    print('Created label: {0.name} (#{0.color})'.format(label))

                    
if __name__ == '__main__':  # yapf: disable
    main()
