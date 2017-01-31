# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Get/Create github labels from a text file."""

# yapf: disable

# Local imports
from loghub.core.repo import GitHubRepo


# yapf: enable


def process_labels(username, password, token, action, repo, filename):
    """Get or update labels on a given repository."""
    # Separator
    s = ';'

    # Instantiate Github API
    gh = GitHubRepo(
        username=username,
        password=password,
        token=token,
        repo=repo, )

    labels = gh.labels()

    if action == 'get':
        print('Getting labels from {0}\n'.format(repo))
        labels = sorted((l.name, l.color) for l in labels)
        data = ''.join('{0}{1}{2}\n'.format(l, s, c) for (l, c) in labels)

        with open(filename, 'wt') as f:
            f.write(data[:-1])

    elif action == 'update':
        print('Updating labels on {0}\n'.format(repo))
        with open(filename, 'r') as f:
            data = f.read()

        lines = [line for line in data.split('\n') if line]
        labels = []
        for line in lines:
            parts = [p for p in line.strip().split(s)]
            if len(parts) == 3:
                old_name, new_name, color = parts
            else:
                new_name, color = parts
                old_name = new_name

            label_dict = {
                'new_name': new_name,
                'old_name': old_name,
                'color': color
            }
            labels.append(label_dict)

        gh.set_labels(labels)
