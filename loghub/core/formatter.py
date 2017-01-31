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
                              CHANGELOG_TEMPLATE_PATH,
                              RELEASE_GROUPS_TEMPLATE_PATH,
                              RELEASE_TEMPLATE_PATH)


# yapf: enable


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
    grouped_filtered_issues = OrderedDict()
    print(issue_label_groups)
    if issue_label_groups:
        new_filtered_issues = []
        for label_group_dic in issue_label_groups:
            grouped_filtered_issues[label_group_dic['name']] = []

        for issue in issues:
            for label_group_dic in issue_label_groups:
                labels = issue.get('loghub_label_names')
                label = label_group_dic['label']
                name = label_group_dic['name']
                if label in labels:
                    grouped_filtered_issues[name].append(issue)
                    new_filtered_issues.append(issue)

        # Remove any empty groups
        for group, grouped_issues in grouped_filtered_issues.copy().items():
            if not grouped_issues:
                grouped_filtered_issues.pop(group)
    else:
        new_filtered_issues = issues

    return new_filtered_issues, grouped_filtered_issues


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
                     batch=None,
                     show_prs=True):
    """Create changelog data for single and batched mode."""
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
            items = zip(*(milestones, empty_items, empty_items))
        elif batch == 'tags':
            tags = [
                i.get('ref', '').replace('refs/tags/', '') for i in gh.tags()
            ]
            since_tags = [None] + tags
            until_tags = tags + [None]
            empty_items = [None] * len(since_tags)
            items = zip(*(empty_items, since_tags, until_tags))
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
        new_filtered_issues, issue_label_groups = filter_issue_label_groups(
            filtered_issues, issue_label_groups)

        ch = render_changelog(
            repo,
            new_filtered_issues,
            filtered_prs,
            version,
            closed_at=closed_at,
            output_format=output_format,
            template_file=template_file,
            issue_label_groups=issue_label_groups,
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
        issue_label_groups=issue_label_groups,
        show_prs=show_prs, )

    return rendered


def write_changelog(changelog, output_file='CHANGELOG.temp'):
    """Output rendered result to prompt and file."""
    print('#' * 79)
    print(changelog)
    print('#' * 79)

    with codecs.open(output_file, "w", "utf-8") as f:
        f.write(changelog)
