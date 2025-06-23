# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
API wrapper for accessing vulnerability test (VT) metadata from the openvasd HTTP API.
"""

import urllib.parse

import httpx


class VtsAPI:
    """
    Provides access to the openvasd /vts endpoints.

    This includes retrieving the list of all available vulnerability tests
    as well as fetching detailed information for individual VTs by OID.
    """

    def __init__(self, client: httpx.Client):
        """
        Initialize a VtsAPI instance.

        Args:
            client: An `httpx.Client` instance configured to communicate with the openvasd server.
        """
        self._client = client

    def get_all(self, safe: bool = False) -> httpx.Response:
        """
        Retrieve the list of all available vulnerability tests (VTs).

        This corresponds to a GET request to `/vts`.

        Args:
            safe: If True, suppress exceptions and return structured error responses.

        Returns:
            The full `httpx.Response` containing a JSON list of VT entries.

        Raises:
            httpx.HTTPStatusError: If the server returns a non-success status and safe is False.

        See: GET /vts in the openvasd API documentation.
        """
        try:
            response = self._client.get("/vts")
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if safe:
                return e.response
            raise

    def get(self, oid: str, safe: bool = False) -> httpx.Response:
        """
        Retrieve detailed information about a specific VT by OID.

        This corresponds to a GET request to `/vts/{oid}`.

        Args:
            oid: The OID (object identifier) of the vulnerability test.
            safe: If True, suppress exceptions and return structured error responses.

        Returns:
            The full `httpx.Response` containing VT metadata for the given OID.

        Raises:
            httpx.HTTPStatusError: If the server returns a non-success status and safe is False.

        See: GET /vts/{id} in the openvasd API documentation.
        """
        quoted_oid = urllib.parse.quote(oid)
        try:
            response = self._client.get(f"/vts/{quoted_oid}")
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if safe:
                return e.response
            raise
