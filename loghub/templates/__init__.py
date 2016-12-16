# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Templates for output formatting."""

# Standard library imports
import os

HERE = os.path.dirname(os.path.realpath(__file__))
CHANGELOG_TEMPLATE_PATH = os.path.join(HERE, 'changelog.txt')
CHANGELOG_GROUPS_TEMPLATE_PATH = os.path.join(HERE, 'changelog_groups.txt')
RELEASE_TEMPLATE_PATH = os.path.join(HERE, 'release.txt')
RELEASE_GROUPS_TEMPLATE_PATH = os.path.join(HERE, 'release_groups.txt')
