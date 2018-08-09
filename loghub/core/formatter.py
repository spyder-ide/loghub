# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Loghub filter and formatter."""

# yapf: disable

# Standard library imports
from collections import OrderedDict
import codecs
import re
import time

# Third party imports
from jinja2 import Template

# Local imports
from loghub.core.repo import GitHubRepo
from loghub.templates import (CHANGELOG_GROUPS_TEMPLATE_PATH,
                              CHANGELOG_ISSUE_GROUPS_TEMPLATE_PATH,
                              CHANGELOG_PR_GROUPS_TEMPLATE_PATH,
                              CHANGELOG_TEMPLATE_PATH,
                              RELEASE_GROUPS_TEMPLATE_PATH,
                              RELEASE_ISSUE_GROUPS_TEMPLATE_PATH,
                              RELEASE_PR_GROUPS_TEMPLATE_PATH,
                              RELEASE_TEMPLATE_PATH)

# yapf: enable


def filter_issues_fixed_by_prs(issues, prs):
    """
    Find related issues to prs and prs to issues that are fixed.

    This adds extra information to the issues and prs listings.
    """
    words = [
        'close', 'closes', 'fix', 'fixes', 'fixed', 'resolve', 'resolves',
        'resolved'
    ]
    pattern = re.compile(
        r'(?P<word>' + r'|'.join(words) + r') '
        r'((?P<repo>.*?)#(?P<number>\d*)|(?P<full_repo>.*)/(?P<number_2>\d*))',
        re.IGNORECASE, )
    issue_pr_map = {}
    pr_issue_map = {}
    for pr in prs:
        is_pr = bool(pr.get('pull_request'))
        if is_pr:
            pr_url = pr.html_url
            pr_number = pr.number
            repo_url = pr_url.split('/pull/')[0] + '/issues/'
            pr_issue_map[pr_url] = []
            body = pr.body or ''
            # Remove blanks and markdown comments
            if body:
                lines = body.splitlines()
                no_comments = [l for l in lines
                               if (l and not l.startswith("<!---"))]
                body = '\n'.join(no_comments)
            for matches in pattern.finditer(body):
                dic = matches.groupdict()
                issue_number = dic['number'] or dic['number_2'] or ''
                repo = dic['full_repo'] or dic['repo'] or repo_url

                # Repo name can't have spaces.
                if ' ' not in repo:
                    # In case spyder-ide/loghub#45 was for example used
                    if 'http' not in repo:
                        repo = 'https://github.com/' + repo

                    if '/issues' not in repo:
                        issue_url = repo + '/issues/' + issue_number
                    elif repo.endswith('/') and issue_number:
                        issue_url = repo + issue_number
                    elif issue_number:
                        issue_url = repo + '/' + issue_number
                    else:
                        issue_url = None
                else:
                    issue_url = None

                # Set the issue data
                issue_data = {'url': pr_url, 'text': pr_number}
                if issue_url is not None:
                    if issue_number in issue_pr_map:
                        issue_pr_map[issue_url].append(issue_data)
                    else:
                        issue_pr_map[issue_url] = [issue_data]

                    pr_data = {'url': issue_url, 'text': issue_number}
                    pr_issue_map[pr_url].append(pr_data)

            pr['loghub_related_issues'] = pr_issue_map[pr_url]

    for issue in issues:
        issue_url = issue.html_url
        if issue_url in issue_pr_map:
            issue['loghub_related_pulls'] = issue_pr_map[issue_url]

    # Now sort the numbers in descending order
    for issue in issues:
        related_pulls = issue.get('loghub_related_pulls', [])
        related_pulls = sorted(
            related_pulls, key=lambda p: p['url'], reverse=True)
        issue['loghub_related_pulls'] = related_pulls

    for pr in prs:
        related_issues = pr.get('loghub_related_issues', [])
        related_issues = sorted(
            related_issues, key=lambda i: i['url'], reverse=True)
        pr['loghub_related_issues'] = related_issues

    return issues, prs


def filter_prs_by_regex(issues, pr_label_regex):
    """Filter prs by issue regex."""
    filtered_prs = []
    pr_pattern = re.compile(pr_label_regex)

    for issue in issues:
        is_pr = bool(issue.get('pull_request'))
        labels = ' '.join(issue.get('loghub_label_names'))

        if is_pr:
            if pr_label_regex:
                pr_valid = bool(pr_pattern.search(labels))
                if pr_valid:
                    filtered_prs.append(issue)
            else:
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
    grouped_filtered_issues = OrderedDict()
    if issue_label_groups:
        new_filtered_issues = []
        for label_group_dic in issue_label_groups:
            grouped_filtered_issues[label_group_dic['name']] = []

        for issue in issues:
            labels = issue.get('loghub_label_names')
            for label_group_dic in issue_label_groups:
                label = label_group_dic['label']
                name = label_group_dic['name']
                if label in labels:
                    grouped_filtered_issues[name].append(issue)
                    new_filtered_issues.append(issue)
    else:
        new_filtered_issues = issues

    return new_filtered_issues, grouped_filtered_issues


def join_label_groups(grouped_issues, grouped_prs, issue_label_groups,
                      pr_label_groups):
    """Combine issue and PR groups in to one dictionary.

    PR-only groups are added after all issue groups. Any groups that are
    shared between issues and PRs are added according to the order in the
    issues list of groups. This results in "label-groups" remaining in the
    same order originally specified even if a group does not have issues
    in it. Otherwise, a shared group may end up at the end of the combined
    dictionary and not in the order originally specified by the user.

    """
    issue_group_names = [x['name'] for x in issue_label_groups]
    pr_group_names = [x['name'] for x in pr_label_groups]
    shared_groups = []
    for idx, group_name in enumerate(issue_group_names):
        if len(pr_group_names) > idx and group_name == pr_group_names[idx]:
            shared_groups.append(group_name)
        else:
            break

    label_groups = OrderedDict()
    # add shared groups first
    for group_name in shared_groups:
        # make sure to copy the issue group in case it is added to
        label_groups[group_name] = grouped_issues.get(group_name, [])[:]
    # add any remaining issue groups
    for group_name, group in grouped_issues.items():
        if group_name in shared_groups:
            continue
        label_groups[group_name] = group[:]
    # add any remaining PR groups (extending any existing groups)
    for group_name, group in grouped_prs.items():
        label_groups.setdefault(group_name, []).extend(group)
    return label_groups


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
                     issue_label_groups=None,
                     pr_label_groups=None,
                     batch=None,
                     show_prs=True):
    """Create changelog data for single and batched mode."""
    if issue_label_groups is None:
        issue_label_groups = []
    if pr_label_groups is None:
        pr_label_groups = []

    gh = GitHubRepo(
        username=username,
        password=password,
        token=token,
        repo=repo, )

    all_changelogs = []
    version_tag_prefix = 'v'

    if batch:
        # This will get all the issues, might eat up the api rate limit!
        base_issues = issues = gh.issues(state='closed', branch=branch)
        if batch == 'milestones':
            milestones = [i.get('title') for i in gh.milestones()]
            empty_items = [None] * len(milestones)
            items = list(zip(milestones, empty_items, empty_items))
        elif batch == 'tags':
            tags = [
                i.get('ref', '').replace('refs/tags/', '') for i in gh.tags()
            ]
            since_tags = [None] + tags
            until_tags = tags + [None]
            empty_items = [None] * len(since_tags)
            items = list(zip(empty_items, since_tags, until_tags))
    else:
        base_issues = None
        if milestone:
            items = [(milestone, None, None)]
        else:
            items = [(None, since_tag, until_tag)]

    for (milestone, since_tag, until_tag) in reversed(items):
        version = until_tag or None
        closed_at = None
        since = None
        until = None

        # Set milestone or from tag
        if milestone and not since_tag:
            milestone_data = gh.milestone(milestone)
            closed_at = milestone_data['closed_at']
            version = milestone

            if version.startswith(version_tag_prefix):
                version = version[len(version_tag_prefix):]

        elif not milestone and since_tag:
            since = gh.tag(since_tag)['tagger']['date']
            if until_tag:
                until = gh.tag(until_tag)['tagger']['date']
                closed_at = until

        # This returns issues and pull requests
        issues = gh.issues(
            milestone=milestone,
            state='closed',
            since=since,
            until=until,
            branch=branch,
            base_issues=base_issues, )

        # Filter by regex if available
        filtered_prs = filter_prs_by_regex(issues, pr_label_regex)
        filtered_issues = filter_issues_by_regex(issues, issue_label_regex)

        # If issue label grouping, filter issues
        new_filtered_issues, grouped_issues = filter_issue_label_groups(
            filtered_issues, issue_label_groups)
        new_filtered_prs, grouped_prs = filter_issue_label_groups(
            filtered_prs, pr_label_groups)
        label_groups = join_label_groups(grouped_issues, grouped_prs,
                                         issue_label_groups, pr_label_groups)

        filter_issues_fixed_by_prs(filtered_issues, filtered_prs)

        ch = render_changelog(
            repo,
            new_filtered_issues,
            new_filtered_prs,
            version,
            closed_at=closed_at,
            output_format=output_format,
            template_file=template_file,
            label_groups=label_groups,
            issue_label_groups=grouped_issues,
            pr_label_groups=grouped_prs,
            show_prs=show_prs)

        all_changelogs.append(ch)

    changelog = '\n'.join(all_changelogs)
    write_changelog(changelog=changelog)

    return changelog


def render_changelog(repo,
                     issues,
                     prs,
                     version=None,
                     closed_at=None,
                     output_format='changelog',
                     template_file=None,
                     issue_label_groups=None,
                     pr_label_groups=None,
                     label_groups=None,
                     show_prs=True):
    """Render changelog data on a jinja template."""
    # Header
    if not version:
        version = '<RELEASE_VERSION>'

    if closed_at:
        close_date = closed_at.split('T')[0]
    else:
        close_date = time.strftime("%Y/%m/%d")

    # Load template
    if template_file:
        filepath = template_file
    else:
        if issue_label_groups and pr_label_groups:
            if output_format == 'changelog':
                filepath = CHANGELOG_GROUPS_TEMPLATE_PATH
            else:
                filepath = RELEASE_GROUPS_TEMPLATE_PATH
        elif issue_label_groups:
            if output_format == 'changelog':
                filepath = CHANGELOG_ISSUE_GROUPS_TEMPLATE_PATH
            else:
                filepath = RELEASE_ISSUE_GROUPS_TEMPLATE_PATH
        elif pr_label_groups:
            if output_format == 'changelog':
                filepath = CHANGELOG_PR_GROUPS_TEMPLATE_PATH
            else:
                filepath = RELEASE_PR_GROUPS_TEMPLATE_PATH
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
        label_groups=label_groups,
        issue_label_groups=issue_label_groups,
        pr_label_groups=pr_label_groups,
        show_prs=show_prs)

    return rendered


def write_changelog(changelog, output_file='CHANGELOG.temp'):
    """Output rendered result to prompt and file."""
    print('#' * 79)
    print(changelog)
    print('#' * 79)

    with codecs.open(output_file, "w", "utf-8") as f:
        f.write(changelog)
