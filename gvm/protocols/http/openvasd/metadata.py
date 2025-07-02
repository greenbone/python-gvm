# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
API wrapper for retrieving metadata from the openvasd HTTP API using HEAD requests.
"""

import httpx


class MetadataAPI:
    """
    Provides access to metadata endpoints exposed by the openvasd server
    using lightweight HTTP HEAD requests.

    These endpoints return useful information in HTTP headers such as:
    - API version
    - Feed version
    - Authentication type

    If the scanner is protected and the request is unauthorized, a 401 response
    is handled gracefully.
    """

    def __init__(self, client: httpx.Client):
        """
        Initialize a MetadataAPI instance.

        Args:
            client: An `httpx.Client` configured to communicate with the openvasd server.
        """
        self._client = client

    def get(self, safe: bool = False) -> dict:
        """
        Perform a HEAD request to `/` to retrieve top-level API metadata.

        Args:
            safe: If True, suppress exceptions and return structured error responses.

        Returns:
            A dictionary containing:

              - "api-version"
              - "feed-version"
              - "authentication"

            Or if safe=True and error occurs:

              - {"error": str, "status_code": int}

        Raises:
            httpx.HTTPStatusError: For non-401 HTTP errors if safe=False.

        See: HEAD / in the openvasd API documentation.
        """
        try:
            response = self._client.head("/")
            response.raise_for_status()
            return {
                "api-version": response.headers.get("api-version"),
                "feed-version": response.headers.get("feed-version"),
                "authentication": response.headers.get("authentication"),
            }
        except httpx.HTTPStatusError as e:
            if safe:
                return {"error": str(e), "status_code": e.response.status_code}
            raise

    def get_scans(self, safe: bool = False) -> dict:
        """
         Perform a HEAD request to `/scans` to retrieve scan endpoint metadata.

         Args:
             safe: If True, suppress exceptions and return structured error responses.

        Returns:
             A dictionary containing:

               - "api-version"
               - "feed-version"
               - "authentication"

             Or if safe=True and error occurs:

               - {"error": str, "status_code": int}

         Raises:
             httpx.HTTPStatusError: For non-401 HTTP errors if safe=False.

         See: HEAD /scans in the openvasd API documentation.
        """
        try:
            response = self._client.head("/scans")
            response.raise_for_status()
            return {
                "api-version": response.headers.get("api-version"),
                "feed-version": response.headers.get("feed-version"),
                "authentication": response.headers.get("authentication"),
            }
        except httpx.HTTPStatusError as e:
            if safe:
                return {"error": str(e), "status_code": e.response.status_code}
            raise
