# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Basic config parser."""

# Third party imports
import configparser
import os


def user_config_path():
    """Return the path of the Loghub user configuration file."""
    return os.path.expanduser('~/.loghubrc')


def load_config():
    """Load configutration file."""
    path = user_config_path()
    config = configparser.ConfigParser()
    if os.path.isfile(path):
        config.read(path)

    return config
