# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
API wrapper for interacting with the Notus component of the openvasd HTTP API.
"""

import urllib.parse
from typing import List

import httpx


class NotusAPI:
    """
    Provides access to the Notus-related endpoints of the openvasd HTTP API.

    This includes retrieving supported operating systems and triggering
    package-based vulnerability scans for a specific OS.
    """

    def __init__(self, client: httpx.Client):
        """
        Initialize a NotusAPI instance.

        Args:
            client: An `httpx.Client` configured to communicate with the openvasd server.
        """
        self._client = client

    def get_os_list(self, safe: bool = False) -> httpx.Response:
        """
        Retrieve the list of supported operating systems from the Notus service.

        Args:
            safe: If True, return error info on failure instead of raising.

        Returns:
            The full `httpx.Response` on success.

        See: GET /notus in the openvasd API documentation.
        """
        try:
            response = self._client.get("/notus")
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if safe:
                return e.response
            raise

    def run_scan(
        self, os: str, package_list: List[str], safe: bool = False
    ) -> httpx.Response:
        """
        Trigger a Notus scan for a given OS and list of packages.

        Args:
            os: Operating system name (e.g., "debian", "alpine").
            package_list: List of package names to evaluate for vulnerabilities.
            safe: If True, return error info on failure instead of raising.

        Returns:
            The full `httpx.Response` on success.

        See: POST /notus/{os} in the openvasd API documentation.
        """
        quoted_os = urllib.parse.quote(os)
        try:
            response = self._client.post(
                f"/notus/{quoted_os}", json=package_list
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if safe:
                return e.response
            raise
