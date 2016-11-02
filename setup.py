#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2016 The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Setup script for loghub."""

# Standard library imports
from setuptools import setup, find_packages
import ast
import os


HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='loghub'):
    """Get version."""
    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()
    lines = data.split('\n')
    for line in lines:
        if line.startswith('VERSION_INFO'):
            version_tuple = ast.literal_eval(line.split('=')[-1].strip())
            version = '.'.join(map(str, version_tuple))
            break
    return version


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.md'), 'r') as f:
        data = f.read()
    return data


setup(
    name='loghub',
    version=get_version(),
    keywords=["github changelog milestone"],
    url='https://github.com/spyder-ide/qtpy',
    license='MIT',
    author='Carlos Cordoba',
    author_email='ccordoba12@gmail.com',
    maintainer='Gonzalo Peña-Castellanos',
    maintainer_email='goanpeca@gmail.com',
    description='Generate changelog based on github milestones',
    long_description=get_description(),
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    dependencies=['six'],
    entry_points={
        'console_scripts': [
            'loghub = loghub.loghub:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5']
)
