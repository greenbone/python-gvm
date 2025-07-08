# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
API wrapper for retrieving metadata from the openvasd HTTP API using HEAD requests.
"""

from dataclasses import dataclass
from typing import Union

import httpx

from ._api import OpenvasdAPI


@dataclass
class Metadata:
    """
    Represents metadata returned by the openvasd API.

    Attributes:
        api_version: Comma separated list of available API versions
        feed_version: Version of the feed.
        authentication: Supported authentication methods
    """

    api_version: str
    feed_version: str
    authentication: str


@dataclass
class MetadataError:
    """
    Represents an error response from the metadata API.

    Attributes:
        error: Error message.
        status_code: HTTP status code of the error response.
    """

    error: str
    status_code: int


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

    def get(self) -> Union[Metadata, MetadataError]:
        """
        Perform a HEAD request to `/` to retrieve top-level API metadata.

        Returns:
            A Metadata instance or MetadataError if exceptions are suppressed and an error occurs.

        Raises:
            httpx.HTTPStatusError: For non-401 HTTP errors if exceptions are not suppressed.

        See: HEAD / in the openvasd API documentation.
        """
        try:
            response = self._client.head("/")
            response.raise_for_status()
            return Metadata(
                api_version=response.headers.get("api-version"),
                feed_version=response.headers.get("feed-version"),
                authentication=response.headers.get("authentication"),
            )
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return MetadataError(
                    error=str(e), status_code=e.response.status_code
                )
            raise

    def get_scans(self) -> Union[Metadata, MetadataError]:
        """
        Perform a HEAD request to `/scans` to retrieve scan endpoint metadata.

        Returns:
            A Metadata instance or MetadataError if exceptions are suppressed and an error occurs.

         Raises:
             httpx.HTTPStatusError: For non-401 HTTP errors if exceptions are not suppressed.

         See: HEAD /scans in the openvasd API documentation.
        """
        try:
            response = self._client.head("/scans")
            response.raise_for_status()
            return Metadata(
                api_version=response.headers.get("api-version"),
                feed_version=response.headers.get("feed-version"),
                authentication=response.headers.get("authentication"),
            )
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return MetadataError(
                    error=str(e), status_code=e.response.status_code
                )
            raise
