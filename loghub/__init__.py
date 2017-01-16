# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Changelog generator based on github milestones or tags."""

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions
