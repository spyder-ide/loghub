# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Changelog generator based on github milestones or tags."""

# Standard library imports
# Standar library imports
import os

HERE = os.path.dirname(os.path.realpath(__file__))
CHANGELOG_TEMPLATE_PATH = os.path.join(HERE, 'changelog.txt')
RELEASE_TEMPLATE_PATH = os.path.join(HERE, 'release.txt')
