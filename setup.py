#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Setup script for loghub."""

# Standard library imports
import os

# Third party imports
from setuptools import find_packages, setup
import versioneer


HERE = os.path.abspath(os.path.dirname(__file__))


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.rst'), 'r') as f:
        data = f.read()
    return data


REQUIREMENTS = ['jinja2']


setup(
    name='loghub',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    keywords=["github changelog milestone"],
    url='https://github.com/spyder-ide/loghub',
    license='MIT',
    author='Carlos Cordoba',
    author_email='ccordoba12@gmail.com',
    maintainer='Carlos Cordoba',
    maintainer_email='ccordoba12@gmail.com',
    description='Generate changelogs based on Github milestones or tags',
    long_description=get_description(),
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=REQUIREMENTS,
    entry_points={'console_scripts': ['loghub = loghub.main:main']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ])
