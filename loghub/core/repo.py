# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Github repo wrapper."""

from __future__ import print_function

# Standard library imports
import datetime
import sys
import time

# Local imports
from loghub.external.github import ApiError, ApiNotFoundError, GitHub


class GitHubRepo(object):
    """Github repository wrapper."""

    def __init__(self, username=None, password=None, token=None, repo=None):
        """Github repository wrapper."""
        self._username = username
        self._password = password
        self._token = token

        self.gh = GitHub(
            username=username,
            password=password,
            access_token=token, )
        repo_organization, repo_name = repo.split('/')
        self._repo_organization = repo_organization
        self._repo_name = repo_name
        self.repo = self.gh.repos(repo_organization)(repo_name)

        # Check username and repo name
        self._check_user()
        self._check_repo_name()

    def _check_user(self):
        """Check if the supplied username is valid."""
        try:
            self.gh.users(self._repo_organization).get()
        except ApiNotFoundError:
            print('LOGHUB: Organization/user `{}` seems to be '
                  'invalid.\n'.format(self._repo_organization))
            sys.exit(1)
        except ApiError:
            self._check_rate()
            print('LOGHUB: The credentials seems to be invalid!\n')
            sys.exit(1)

    def _check_repo_name(self):
        """Check if the supplied repository exists."""
        try:
            self.repo.get()
        except ApiNotFoundError:
            print('LOGHUB: Repository `{0}` for organization/username `{1}` '
                  'seems to be invalid.\n'.format(self._repo_name,
                                                  self._repo_organization))
            sys.exit(1)
        except ApiError:
            self._check_rate()

    def _check_rate(self):
        """Check and handle if api rate limit has been exceeded."""
        if self.gh.x_ratelimit_remaining == 0:
            reset_struct = time.gmtime(self.gh.x_ratelimit_reset)
            reset_format = time.strftime('%Y/%m/%d %H:%M', reset_struct)
            print('LOGHUB: GitHub API rate limit exceeded!')
            print('LOGHUB: GitHub API rate limit resets on '
                  '{}'.format(reset_format))
            if not self._username and not self._password or not self._token:
                print('LOGHUB: Try running loghub with user/password or '
                      'a valid token.\n')
            sys.exit(1)

    def _filter_milestone(self, issues, milestone):
        """Filter out all issues in milestone."""
        if milestone:
            for issue in issues[:]:
                milestone_data = issue.get('milestone', {})
                if milestone_data:
                    issue_milestone_title = milestone_data.get('title')
                else:
                    issue_milestone_title = ''

                if issue_milestone_title != milestone:
                    issues.remove(issue)
        return issues

    def _filter_since(self, issues, since):
        """Filter out all issues before `since` date."""
        if since:
            since_date = self.str_to_date(since)
            for issue in issues[:]:
                close_date = self.str_to_date(issue['closed_at'])
                if close_date < since_date and issue in issues:
                    issues.remove(issue)
        return issues

    def _filter_until(self, issues, until):
        """Filter out all issues after `until` date."""
        if until:
            until_date = self.str_to_date(until)
            for issue in issues[:]:
                close_date = self.str_to_date(issue['closed_at'])
                if close_date > until_date and issue in issues:
                    issues.remove(issue)
        return issues

    def _filter_by_branch(self, issues, issue, branch):
        """Filter prs by the branch they were merged into."""
        number = issue['number']

        if not self.is_merged(number) and issue in issues:
            issues.remove(issue)

        if branch:
            # Get PR info and get base branch
            pr_data = self.pr(number)
            base_ref = pr_data['base']['ref']

            if base_ref != branch and issue in issues:
                issues.remove(issue)

        return issues

    def _filer_closed_prs(self, issues, branch):
        """Filter out closed PRs."""
        for issue in issues[:]:
            pr = issue.get('pull_request', '')

            # Add label names inside additional key
            issue['loghub_label_names'] = [
                l['name'] for l in issue.get('labels')
            ]

            if pr:
                issues = self._filter_by_branch(issues, issue, branch)

        return issues

    def tags(self):
        """Return all tags."""
        self._check_rate()
        return self.repo('git')('refs')('tags').get()

    def tag(self, tag_name):
        """Get tag information."""
        self._check_rate()
        refs = self.repo('git')('refs')('tags').get()
        sha = -1

        tags = []
        for ref in refs:
            ref_name = 'refs/tags/{tag}'.format(tag=tag_name)
            if 'object' in ref and ref['ref'] == ref_name:
                sha = ref['object']['sha']
            tags.append(ref['ref'].split('/')[-1])

        if sha == -1:
            print("LOGHUB: You didn't pass a valid tag name!")
            print('LOGHUB: The available tags are: {0}\n'.format(tags))
            sys.exit(1)

        return self.repo('git')('tags')(sha).get()

    def labels(self):
        """Return labels for the repo."""
        self._check_rate()
        return self.repo.labels.get()

    def set_labels(self, labels):
        """Return labels for the repo."""
        self._check_rate()
        for label in labels:
            new_name = label['new_name']
            old_name = label['old_name']
            color = label['color']
            try:
                self.repo.labels(old_name).patch(name=new_name, color=color)
                print('Updated label: "{0}" -> "{1}" (#{2})'.format(
                    old_name, new_name, color))
            except ApiError:
                try:
                    self.repo.labels.post(name=new_name, color=color)
                    print('Created label: "{0}" (#{1})'.format(new_name,
                                                               color))
                except ApiError:
                    print('\nLabel "{0}" already exists!'.format(new_name))

    def milestones(self):
        """Return all milestones."""
        self._check_rate()
        return self.repo.milestones.get(state='all')

    def milestone(self, milestone_title):
        """Return milestone with given title."""
        self._check_rate()
        milestones = self.milestones()
        milestone_number = -1

        milestone_titles = [milestone['title'] for milestone in milestones]
        for milestone in milestones:
            if milestone['title'] == milestone_title:
                milestone_number = milestone['number']
                break

        if milestone_number == -1:
            print("LOGHUB: You didn't pass a valid milestone name!")
            print('LOGHUB: The available milestones are: {0}\n'
                  ''.format(milestone_titles))
            sys.exit(1)

        return milestone

    def pr(self, pr_number):
        """Get PR information."""
        self._check_rate()
        return self.repo('pulls')(str(pr_number)).get()

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
               until=None,
               branch=None,
               cache=False,
               base_issues=None):
        """Return Issues and Pull Requests."""
        self._check_rate()
        page = 1

        if not base_issues:
            milestone_number = None
            if milestone:
                milestone_data = self.milestone(milestone)
                milestone_number = milestone_data.get('number')
            issues = []
            while True:
                result = self.repo.issues.get(page=page,
                                              per_page=100,
                                              milestone=milestone_number,
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
        else:
            issues = base_issues

        # If since was provided, filter the issue
        issues = self._filter_since(issues, since)

        # If until was provided, filter the issue
        issues = self._filter_until(issues, until)

        # If milestone was provided, filter the issue
        issues = self._filter_milestone(issues, milestone)

        # If it is a pr check if it is merged or closed, removed closed ones
        issues = self._filer_closed_prs(issues, branch)

        return issues

    def is_merged(self, pr):
        """
        Return wether a PR was merged, or if it was closed and discarded.

        https://developer.github.com/v3/pulls/#get-if-a-pull-request-has-been-merged
        """
        self._check_rate()
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
