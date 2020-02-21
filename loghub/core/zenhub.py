# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""ZenHub API."""

from __future__ import print_function

# Third party imports
import requests


class ZenHubError(Exception):
    pass


class ZenHub(object):
    """ZenHub API wrapper."""
    _HEADERS = {
        'Content-type': 'application/json',
        'User-Agent': 'ZenHub Python Client',
    }

    def __init__(self, token):
        """ZenHub API wrapper."""
        self._token = token
        self._endpoint = 'https://api.zenhub.com/p1/'
        self._session = requests.Session()

        # Setup
        self._session.headers.update(self._HEADERS)
        self._session.headers.update({'X-Authentication-Token': token})

    # --- Helpers
    @staticmethod
    def _parse_response_contents(response):
        """Parse response and convert to json if possible."""
        contents = {}

        status_code = response.status_code
        if status_code == 200:
            try:
                contents = response.json()                
            except Exception as err:
                print(err)
        elif status_code == 401:
            raise ZenHubError('Invalid token!')
        elif status_code == 403:
            raise ZenHubError('Reached request limit to the API. See API Limits.')
        elif status_code == 404:
            raise ZenHubError('Not found!')
        else:
            raise ZenHubError('Unknown error!')

        return contents

    def _make_url(self, url):
        """Create full api url."""
        return '{}{}'.format(self._endpoint, url)

    def _get(self, url):
        """Send GET request with given url."""
        response = self._session.get(self._make_url(url))
        return self._parse_response_contents(response)

    def releases(self, repo_id):
        """Provide list of releases for a given `repo_id`."""
        url = 'repositories/{repo_id}/reports/releases'
        return self._get(url.format(repo_id=repo_id))

    def issues(self, release_id):
        """Return a list of issues found in given `release_id`."""
        url = 'reports/release/{release_id}/issues'
        return self._get(url.format(release_id=release_id))
