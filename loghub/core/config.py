# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Basic config parser."""

# Third party imports
import os
import sys

# Constants
PY2 = sys.version[0] == '2'
if PY2:
    import ConfigParser as configparser
else:
    import configparser


def user_config_path():
    """Return the path of the Loghub user configuration file."""
    return os.path.expanduser('~/.loghubrc')


def load_config(path=None):
    """Load configutration file."""
    config_path = path or user_config_path()
    config = configparser.ConfigParser()
    if os.path.isfile(config_path):
        config.read(config_path)

    return config
