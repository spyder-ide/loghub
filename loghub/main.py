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
import datetime
import getpass
import re
import sys
import time

# Third party imports
from jinja2 import Template

# Local imports
from loghub.external.github import GitHub
from loghub.templates import CHANGELOG_TEMPLATE_PATH, RELEASE_TEMPLATE_PATH

PY2 = sys.version[0] == '2'


def main():
    """Main script."""
    # Cli options
    parser = argparse.ArgumentParser(
        description='Script to print the list of issues and pull requests '
        'closed in a given milestone')
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
        '-il',
        '--issue-label-regex',
        action="store",
        dest="issue_label_regex",
        default='',
        help="Label issue filter using a regular expression filter")
    parser.add_argument(
        '-pl',
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

    create_changelog(
        repo=options.repository,
        username=username,
        password=password,
        token=options.token,
        milestone=milestone,
        since_tag=options.since_tag,
        until_tag=options.until_tag,
        output_format=options.output_format,
        issue_label_regex=options.issue_label_regex,
        pr_label_regex=options.pr_label_regex,
        template_file=options.template)


def create_changelog(repo=None,
                     username=None,
                     password=None,
                     token=None,
                     milestone=None,
                     since_tag=None,
                     until_tag=None,
                     output_format='changelog',
                     issue_label_regex='',
                     pr_label_regex='',
                     template_file=None):
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
        milestone=milestone_number, state='closed', since=since, until=until)

    # Filter by regex if available
    filtered_issues, filtered_prs = [], []
    issue_pattern = re.compile(issue_label_regex)
    pr_pattern = re.compile(pr_label_regex)
    for issue in issues:
        is_pr = bool(issue.get('pull_request'))
        is_issue = not is_pr
        labels = ' '.join(issue.get('_label_names'))

        if is_issue and issue_label_regex:
            issue_valid = bool(issue_pattern.search(labels))
            if issue_valid:
                filtered_issues.append(issue)
        elif is_pr and pr_label_regex:
            pr_valid = bool(pr_pattern.search(labels))
            if pr_valid:
                filtered_prs.append(issue)
        elif is_issue and not issue_label_regex:
            filtered_issues.append(issue)
        elif is_pr and not pr_label_regex:
            filtered_prs.append(issue)

    return format_changelog(
        repo,
        filtered_issues,
        filtered_prs,
        version,
        closed_at=closed_at,
        output_format=output_format,
        template_file=template_file)


def format_changelog(repo,
                     issues,
                     prs,
                     version,
                     closed_at=None,
                     output_format='changelog',
                     output_file='CHANGELOG.temp',
                     template_file=None):
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
        repo_name=repo_name, )

    print('#' * 79)
    print(rendered)
    print('#' * 79)

    with open(output_file, 'w') as f:
        f.write(rendered)

    return rendered


class GitHubRepo(object):
    """Github repository wrapper."""

    def __init__(self, username=None, password=None, token=None, repo=None):
        """Github repository wrapper."""
        self.gh = GitHub(
            username=username,
            password=password,
            access_token=token, )
        repo_organization, repo_name = repo.split('/')
        self.repo = self.gh.repos(repo_organization)(repo_name)

    def tags(self):
        """Return all tags."""
        return self.repo('git')('refs')('tags').get()

    def tag(self, tag_name):
        """Get tag information."""
        refs = self.repo('git')('refs')('tags').get()
        sha = -1
        for ref in refs:
            ref_name = 'refs/tags/{tag}'.format(tag=tag_name)
            if 'object' in ref and ref['ref'] == ref_name:
                sha = ref['object']['sha']
                break

        if sha == -1:
            print("You didn't pass a valid tag name!")
            sys.exit(1)

        return self.repo('git')('tags')(sha).get()

    def milestones(self):
        """Return all milestones."""
        return self.repo.milestones.get(state='all')

    def milestone(self, milestone_title):
        """Return milestone with given title."""
        milestones = self.milestones()
        milestone_number = -1
        for milestone in milestones:
            if milestone['title'] == milestone_title:
                milestone_number = milestone['number']
                break

        if milestone_number == -1:
            print("You didn't pass a valid milestone name!")
            sys.exit(1)

        return milestone

    def issues(self,
               milestone=None,
               state=None,
               assignee=None,
               creator=None,
               mentioned=None,
               labels=None,
               sort=None,
               direction=None,
               since=None,
               until=None):
        """Return Issues and Pull Requests."""
        page = 1
        issues = []
        while True:
            result = self.repo.issues.get(page=page,
                                          per_page=100,
                                          milestone=milestone,
                                          state=state,
                                          assignee=assignee,
                                          creator=creator,
                                          mentioned=mentioned,
                                          labels=labels,
                                          sort=sort,
                                          direction=direction,
                                          since=since)
            if len(result) > 0:
                issues += result
                page = page + 1
            else:
                break

        # If since was provided, filter the issue
        if since:
            since_date = self.str_to_date(since)
            for issue in issues[:]:
                close_date = self.str_to_date(issue['closed_at'])
                if close_date < since_date:
                    issues.remove(issue)

        # If until was provided, filter the issue
        if until:
            until_date = self.str_to_date(until)
            for issue in issues[:]:
                close_date = self.str_to_date(issue['closed_at'])
                if close_date > until_date:
                    issues.remove(issue)

        # If it is a pr check if it is merged or closed, removed closed ones
        for issue in issues[:]:
            pr = issue.get('pull_request', '')

            # Add label names inside additional key
            issue['_label_names'] = [l['name'] for l in issue.get('labels')]

            if pr:
                number = issue['number']
                if not self.is_merged(number):
                    issues.remove(issue)

        return issues

    def is_merged(self, pr):
        """
        Return wether a PR was merged, or if it was closed and discarded.

        https://developer.github.com/v3/pulls/#get-if-a-pull-request-has-been-merged
        """
        merged = True
        try:
            self.repo('pulls')(str(pr))('merge').get()
        except Exception:
            merged = False
        return merged

    @staticmethod
    def str_to_date(string):
        """Convert ISO date string to datetime object."""
        parts = string.split('T')
        date_parts = parts[0]
        time_parts = parts[1][:-1]
        year, month, day = [int(i) for i in date_parts.split('-')]
        hour, minutes, seconds = [int(i) for i in time_parts.split(':')]
        return datetime.datetime(year, month, day, hour, minutes, seconds)


if __name__ == '__main__':  # yapf: disable
    main()
