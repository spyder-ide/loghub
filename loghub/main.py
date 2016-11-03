# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Build a list of issues and pull requests per Github milestone."""

# Standard library imports
import argparse
import datetime
import sys
import time

# Local imports
from loghub.external.github import GitHub

# TEMPLATES
ISSUE_LONG = "* [Issue {number}](https://github.com/{repo}/issues/{number})"
ISSUE_SHORT = "* Issue #{number}"
PR_LONG = "* [PR {number}](https://github.com/{repo}/pull/{number})"
PR_SHORT = "* PR #{number}"


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
    options = parser.parse_args()

    # Check if repo given
    if not options.repository:
        print('Please define a repository name to this script. See its help')
        sys.exit(1)

    # Check if milestone or tag given
    if not options.milestone and not options.since_tag:
        print('Please pass a milestone or a tag to this script. See its help')
        sys.exit(1)

    create_changelog(
        repo=options.repository,
        username=options.user,
        password=options.password,
        milestone=options.milestone,
        since_tag=options.since_tag,
        until_tag=options.until_tag,
        output_format=options.output_format, )


def create_changelog(repo, username, password, milestone, since_tag, until_tag,
                     output_format):
    """Create changelog data."""
    # Instantiate Github API
    gh = GitHubRepo(username=username, password=password, repo=repo)

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

    format_changelog(
        repo,
        issues,
        version,
        closed_at=closed_at,
        output_format=output_format)


def format_changelog(repo,
                     issues,
                     version,
                     closed_at=None,
                     output_format='changelog',
                     output_file='CHANGELOG.temp'):
    """Create changelog data."""
    lines = []

    # Header
    if version and version[0] == 'v':
        version = version.replace('v', '')
    else:
        '<RELEASE_VERSION>'

    if closed_at:
        close_date = closed_at.split('T')[0]
    else:
        close_date = time.strftime("%Y/%m/%d")

    quotes = '"' if version and ' ' in version else ''
    header = '## Version {q}{version}{q} ({date})\n'.format(
        version=version, date=close_date, q=quotes)

    lines.append(header)
    lines.append('\n### Issues closed\n')

    # Issues
    lines.append('\n**Issues**\n\n')
    number_of_issues = 0
    for i in issues:
        pr = i.get('pull_request', '')
        if not pr:
            number_of_issues += 1
            number = i['number']
            if output_format == 'changelog':
                issue_link = ISSUE_LONG.format(number=number, repo=repo)
            else:
                issue_link = ISSUE_SHORT.format(number=number)
            lines.append(issue_link + ' - ' + i['title'] + '\n')

    tense = 'was' if number_of_issues == 1 else 'were'
    plural = '' if number_of_issues == 1 else 's'
    lines.append('\nIn this release {number} issue{plural} {tense} closed\n'
                 ''.format(
                     number=number_of_issues, tense=tense, plural=plural))

    # Pull requests
    lines.append('\n**Pull requests**\n\n')
    number_of_prs = 0
    for i in issues:
        pr = i.get('pull_request', '')
        if pr:
            number_of_prs += 1
            number = i['number']
            if output_format == 'changelog':
                pr_link = PR_LONG.format(number=number, repo=repo)
            else:
                pr_link = PR_SHORT.format(number)
            lines.append(pr_link + ' - ' + i['title'] + '\n')
    tense = 'was' if number_of_prs == 1 else 'were'
    plural = '' if number_of_prs == 1 else 's'
    lines.append('\nIn this release {number} pull request{plural} {tense} '
                 'merged\n'.format(
                     number=number_of_prs, tense=tense, plural=plural))

    # Print everything
    for line in lines:
        print(line)

    # Write to file
    with open(output_file, 'w') as f:
        f.write(''.join(lines))


class GitHubRepo(object):
    """Github repository wrapper."""

    def __init__(self, username=None, password=None, repo=None):
        """Github repository wrapper."""
        self.gh = GitHub(username=username, password=password)
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
                                          firection=direction,
                                          since=since)
            if len(result) > 0:
                issues += result
                page = page + 1
            else:
                break

        # If until was provided, fix it!
        if until:
            until_date = self.str_to_date(until)
            for issue in issues[:]:
                close_date = self.str_to_date(issue['closed_at'])
                if close_date > until_date:
                    issues.remove(issue)

        return issues

    @staticmethod
    def str_to_date(string):
        """Convert ISO date string to datetime object."""
        parts = string.split('T')
        date_parts = parts[0]
        time_parts = parts[1][:-1]
        year, month, day = [int(i) for i in date_parts.split('-')]
        hour, minutes, seconds = [int(i) for i in time_parts.split(':')]
        return datetime.datetime(year, month, day, hour, minutes, seconds)


if __name__ == '__main__':
    main()
