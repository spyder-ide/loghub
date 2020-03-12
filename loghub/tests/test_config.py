# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Tests changelog labels."""

# Standard library imports
import tempfile

# Third party imports
from mock import patch

# Local imports
from loghub.core.config import load_config


def test_load_config_empty():
    _, tempfilepath = tempfile.mkstemp()

    with patch('loghub.core.config.user_config_path',
                return_value=tempfilepath) as method:
        config = load_config()
        assert config.sections() == []


def test_load_config():
    _, tempfilepath = tempfile.mkstemp()
    with open(tempfilepath, 'w') as fh:
        fh.write('[github]\ntoken=1\n[zenhub]\ntoken=2')

    with patch('loghub.core.config.user_config_path',
                return_value=tempfilepath) as method:
        config = load_config()
        assert config.sections() == ['github', 'zenhub']
        assert config.get('github', 'token') == '1'
        assert config.get('zenhub', 'token') == '2'


def test_load_config_with_path():
    _, tempfilepath = tempfile.mkstemp()
    with open(tempfilepath, 'w') as fh:
        fh.write('[github]\ntoken=1\n[zenhub]\ntoken=2')

    config = load_config(tempfilepath)
    assert config.sections() == ['github', 'zenhub']
    assert config.get('github', 'token') == '1'
    assert config.get('zenhub', 'token') == '2'
