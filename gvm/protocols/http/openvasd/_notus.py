# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
API wrapper for interacting with the Notus component of the openvasd HTTP API.
"""

import urllib

import httpx

from ._api import OpenvasdAPI


class NotusAPI(OpenvasdAPI):
    """
    Provides access to the Notus-related endpoints of the openvasd HTTP API.

    This includes retrieving supported operating systems and triggering
    package-based vulnerability scans for a specific OS.
    """

    def get_os_list(self) -> httpx.Response:
        """
        Retrieve the list of supported operating systems from the Notus service.

        Returns:
            The full `httpx.Response` on success.

        See: GET /notus in the openvasd API documentation.
        """
        try:
            response = self._client.get("/notus")
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response
            raise

    def run_scan(
        self,
        os: str,
        package_list: list[str],
    ) -> httpx.Response:
        """
        Trigger a Notus scan for a given OS and list of packages.

        Args:
            os: Operating system name (e.g., "debian", "alpine").
            package_list: List of package names to evaluate for vulnerabilities.

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
            if self._suppress_exceptions:
                return e.response
            raise
