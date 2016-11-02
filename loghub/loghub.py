# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2016 The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Build a list of issues and pull requests per Github milestone."""

# Standard library imports
import argparse
import sys

# Local imports
from .external import github

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
                    'closed in a given milestone',
        )
    parser.add_argument(
        '-m',
        '--milestone',
        action="store",
        dest="milestone",
        default='',
        help="Github milestone to get issues and pull requests for",
        )
    parser.add_argument(
        '-f',
        '--format',
        action="store",
        dest="format",
        default='changelog',
        help="Format for print, either 'changelog' (for "
             "Changelog.md file) or 'release' (for the Github "
             "Releases page). Default is 'changelog'. The "
             "'release' option doesn't generate Markdown "
             "hyperlinks.",
        )
    parser.add_argument(
        '-r',
        '--repo',
        action="store",
        dest="repo",
        default='',
        help="Repo name to generate the Changelog for, in the form "
             "user/repo or org/repo (e.g. spyder-ide/spyder) ",
        )
    parser.add_argument(
        '-u',
        '--user',
        action="store",
        dest="user",
        default='',
        help="Github user name",
        )
    parser.add_argument(
        '-p',
        '--password',
        action="store",
        dest="password",
        default='',
        help="Github user password",
        )
    parser.add_argument(
        '--page',
        action="store",
        dest="page",
        default='1',
        help="What page to select when asking Github for issues "
             "and pull requests of a given milestone. Default is "
             "1, and it contains 100 results",
        )
    options = parser.parse_args()

    # Instantiate Github API
    gh = github.GitHub(username=options.user, password=options.password)

    # Set repo
    if not options.repo:
        print('Please define a repository name to this script. See its help')
        sys.exit(1)
    else:
        repo_name = options.repo.split('/')
        repo = gh.repos(repo_name[0])(repo_name[1])

    # Set milestone
    if not options.milestone:
        print('Please pass a milestone to this script. See its help')
        sys.exit(1)

    milestones = repo.milestones.get(state='all')
    milestone_number = -1
    for ms in milestones:
        if ms['title'] == options.milestone:
            milestone_number = ms['number']
            closed_at = ms['closed_at']

    if milestone_number == -1:
        print("You didn't pass a valid milestone name!")
        sys.exit(1)

    # This returns issues and pull requests
    issues = repo.issues.get(milestone=milestone_number, state='closed',
                             per_page='100', page=options.page)

    # Print header
    version = options.milestone.replace('v', '')
    if closed_at:
        close_date = closed_at.split('T')[0]
        print('\n## Version {version} ({date})\n'.format(version=version,
              date=close_date))
    else:
        print('\n## Version {version} \n'.format(version=version))
    print('### Issues closed\n')

    # Printing issues
    print('**Issues**\n')
    number_of_issues = 0
    for i in issues:
        pr = i.get('pull_request', '')
        if not pr:
            number_of_issues += 1
            number = i['number']
            if options.format == 'changelog':
                issue_link = ISSUE_LONG.format(number=number,
                                               repo=options.repo)
            else:
                issue_link = ISSUE_SHORT.format(number=number)
            print(issue_link + ' - ' + i['title'])
    print('\nIn this release {number} issues were closed'.format(
          number=number_of_issues))

    # Printing pull requests
    print('\n**Pull requests**\n')
    number_of_prs = 0
    for i in issues:
        pr = i.get('pull_request', '')
        if pr:
            number_of_prs += 1
            number = i['number']
            if options.format == 'changelog':
                pr_link = PR_LONG.format(number=number, repo=options.repo)
            else:
                pr_link = PR_SHORT.format(number)
            print(pr_link + ' - ' + i['title'])
    print('\nIn this release {number} pull requests were merged '.format(
          number=number_of_prs))


if __name__ == '__main__':
    main()
