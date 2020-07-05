# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Changelog generator based on github milestones or tags."""

__version__ = '0.5.1'


def _to_version_info(version):
    """Convert a version string to a number and string tuple."""
    parts = []
    for part in version.split('.'):
        try:
            part = int(part)
        except ValueError:
            pass

        parts.append(part)

    return tuple(parts)


VERSION_INFO = _to_version_info(__version__)
