# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
API wrapper for retrieving metadata from the openvasd HTTP API using HEAD requests.
"""

from typing import Union

import httpx

from ._api import OpenvasdAPI


class MetadataAPI(OpenvasdAPI):
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

    def get(self) -> dict[str, Union[str, int]]:
        """
        Perform a HEAD request to `/` to retrieve top-level API metadata.

        Returns:
            A dictionary containing:

              - "api-version"
              - "feed-version"
              - "authentication"

            Or if exceptions are suppressed and error occurs:

              - {"error": str, "status_code": int}

        Raises:
            httpx.HTTPStatusError: For non-401 HTTP errors if exceptions are not suppressed.

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
            if self._suppress_exceptions:
                return {"error": str(e), "status_code": e.response.status_code}
            raise

    def get_scans(self) -> dict[str, Union[str, int]]:
        """
         Perform a HEAD request to `/scans` to retrieve scan endpoint metadata.

        Returns:
             A dictionary containing:

               - "api-version"
               - "feed-version"
               - "authentication"

             Or if safe=True and error occurs:

               - {"error": str, "status_code": int}

         Raises:
             httpx.HTTPStatusError: For non-401 HTTP errors if exceptions are not suppressed.

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
            if self._suppress_exceptions:
                return {"error": str(e), "status_code": e.response.status_code}
            raise
