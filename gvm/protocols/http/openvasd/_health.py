# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
API wrapper for accessing the /health endpoints of the openvasd HTTP API.
"""

import httpx

from ._api import OpenvasdAPI


class HealthAPI(OpenvasdAPI):
    """
    Provides access to the openvasd /health endpoints, which expose the
    operational state of the scanner.

    All methods return the HTTP status code of the response and raise an exception
    if the server returns an error response (4xx or 5xx).
    """

    def get_alive(self) -> int:
        """
        Check if the scanner process is alive.

        Returns:
            HTTP status code (e.g., 200 if alive).

        Raises:
            httpx.HTTPStatusError: If the server response indicates failure and
                exceptions are not suppressed.

        See: GET /health/alive in the openvasd API documentation.
        """
        try:
            response = self._client.get("/health/alive")
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response.status_code
            raise

    def get_ready(self) -> int:
        """
        Check if the scanner is ready to accept requests (e.g., feed loaded).

        Returns:
            HTTP status code (e.g., 200 if ready).

        Raises:
            httpx.HTTPStatusError: If the server response indicates failure and
                exceptions are not suppressed.

        See: GET /health/ready in the openvasd API documentation.
        """
        try:
            response = self._client.get("/health/ready")
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response.status_code
            raise

    def get_started(self) -> int:
        """
        Check if the scanner has fully started.

        Returns:
            HTTP status code (e.g., 200 if started).

        Raises:
            httpx.HTTPStatusError: If the server response indicates failure and
                exceptions are not suppressed.

        See: GET /health/started in the openvasd API documentation.
        """
        try:
            response = self._client.get("/health/started")
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response.status_code
            raise
