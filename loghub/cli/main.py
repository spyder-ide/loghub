# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Build a list of issues and pull requests per Github milestone."""

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


def filter_prs_by_regex(issues, pr_label_regex):
    """Filter prs by issue regex."""
    filtered_prs = []
    pr_pattern = re.compile(pr_label_regex)

    for issue in issues:
        is_pr = bool(issue.get('pull_request'))
        labels = ' '.join(issue.get('loghub_label_names'))

        if is_pr and pr_label_regex:
            pr_valid = bool(pr_pattern.search(labels))
            if pr_valid:
                filtered_prs.append(issue)
        if is_pr and not pr_label_regex:
            filtered_prs.append(issue)

    return filtered_prs


def filter_issues_by_regex(issues, issue_label_regex):
    """Filter issues by issue regex."""
    filtered_issues = []
    issue_pattern = re.compile(issue_label_regex)

    for issue in issues:
        is_pr = bool(issue.get('pull_request'))
        is_issue = not is_pr
        labels = ' '.join(issue.get('loghub_label_names'))

        if is_issue and issue_label_regex:
            issue_valid = bool(issue_pattern.search(labels))
            if issue_valid:
                filtered_issues.append(issue)
        elif is_issue and not issue_label_regex:
            filtered_issues.append(issue)

    return filtered_issues


def filter_issue_label_groups(issues, issue_label_groups):
    """Filter issues by the label groups."""
    new_filtered_issues = []
    if issue_label_groups:
        for issue in issues:
            for label_group_dic in issue_label_groups:
                labels = issue.get('loghub_label_names')
                label = label_group_dic['label']
                if label in labels:
                    new_filtered_issues.append(issue)
    else:
        new_filtered_issues = issues

    return new_filtered_issues


def create_changelog(repo=None,
                     username=None,
                     password=None,
                     token=None,
                     milestone=None,
                     since_tag=None,
                     until_tag=None,
                     branch=None,
                     output_format='changelog',
                     issue_label_regex='',
                     pr_label_regex='',
                     template_file=None,
                     issue_label_groups=None):
    """Create changelog data."""
    # Instantiate Github API
    gh = GitHubRepo(
        username=username,
        password=password,
        token=token,
        repo=repo, )

    version = until_tag or None
    milestone_number = None
    closed_at = None
    since = None
    until = None

    # Set milestone or from tag
    if milestone and not since_tag:
        milestone_data = gh.milestone(milestone)
        milestone_number = milestone_data['number']
        closed_at = milestone_data['closed_at']
        version = milestone.replace('v', '')
    elif not milestone and since_tag:
        since = gh.tag(since_tag)['tagger']['date']
        if until_tag:
            until = gh.tag(until_tag)['tagger']['date']
            closed_at = until

    # This returns issues and pull requests
    issues = gh.issues(
        milestone=milestone_number,
        state='closed',
        since=since,
        until=until,
        branch=branch, )

    # Filter by regex if available
    filtered_prs = filter_prs_by_regex(issues, pr_label_regex)
    filtered_issues = filter_issues_by_regex(issues, issue_label_regex)

    # If issue label grouping, filter issues
    new_filtered_issues = filter_issue_label_groups(filtered_issues,
                                                    issue_label_groups)

    return format_changelog(
        repo,
        new_filtered_issues,
        filtered_prs,
        version,
        closed_at=closed_at,
        output_format=output_format,
        template_file=template_file,
        issue_label_groups=issue_label_groups)


def format_changelog(repo,
                     issues,
                     prs,
                     version,
                     closed_at=None,
                     output_format='changelog',
                     output_file='CHANGELOG.temp',
                     template_file=None,
                     issue_label_groups=None):
    """Create changelog data."""
    # Header
    if version and version[0] == 'v':
        version = version.replace('v', '')
    else:
        version = '<RELEASE_VERSION>'

    if closed_at:
        close_date = closed_at.split('T')[0]
    else:
        close_date = time.strftime("%Y/%m/%d")

    # Load template
    if template_file:
        filepath = template_file
    else:
        if issue_label_groups:
            if output_format == 'changelog':
                filepath = CHANGELOG_GROUPS_TEMPLATE_PATH
            else:
                filepath = RELEASE_GROUPS_TEMPLATE_PATH
        else:
            if output_format == 'changelog':
                filepath = CHANGELOG_TEMPLATE_PATH
            else:
                filepath = RELEASE_TEMPLATE_PATH

    with open(filepath) as f:
        data = f.read()

    repo_owner, repo_name = repo.split('/')
    template = Template(data)
    rendered = template.render(
        issues=issues,
        pull_requests=prs,
        version=version,
        close_date=close_date,
        repo_full_name=repo,
        repo_owner=repo_owner,
        repo_name=repo_name,
        issue_label_groups=issue_label_groups, )

    print('#' * 79)
    print(rendered)
    print('#' * 79)

    with open(output_file, 'w') as f:
        f.write(rendered)

    return rendered


if __name__ == '__main__':  # yapf: disable
    main()
