# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
API wrapper for accessing the /health endpoints of the openvasd HTTP API.
"""

import httpx


class HealthAPI:
    """
    Provides access to the openvasd /health endpoints, which expose the
    operational state of the scanner.

    All methods return the HTTP status code of the response and raise an exception
    if the server returns an error response (4xx or 5xx).
    """

    def __init__(self, client: httpx.Client):
        """
        Create a new HealthAPI instance.

        Args:
            client: An initialized `httpx.Client` configured for communicating
                    with the openvasd server.
        """
        self._client = client

    def get_alive(self, safe: bool = False) -> int:
        """
        Check if the scanner process is alive.

        Args:
            safe: If True, suppress exceptions and return structured error responses.

        Returns:
            HTTP status code (e.g., 200 if alive).

        Raises:
            httpx.HTTPStatusError: If the server response indicates failure and safe is False.

        See: GET /health/alive in the openvasd API documentation.
        """
        try:
            response = self._client.get("/health/alive")
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as e:
            if safe:
                return e.response.status_code
            raise

    def get_ready(self, safe: bool = False) -> int:
        """
        Check if the scanner is ready to accept requests (e.g., feed loaded).

        Args:
            safe: If True, suppress exceptions and return structured error responses.

        Returns:
            HTTP status code (e.g., 200 if ready).

        Raises:
            httpx.HTTPStatusError: If the server response indicates failure and safe is False.

        See: GET /health/ready in the openvasd API documentation.
        """
        try:
            response = self._client.get("/health/ready")
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as e:
            if safe:
                return e.response.status_code
            raise

    def get_started(self, safe: bool = False) -> int:
        """
        Check if the scanner has fully started.

        Args:
            safe: If True, suppress exceptions and return structured error responses.

        Returns:
            HTTP status code (e.g., 200 if started).

        Raises:
            httpx.HTTPStatusError: If the server response indicates failure and safe is False.

        See: GET /health/started in the openvasd API documentation.
        """
        try:
            response = self._client.get("/health/started")
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as e:
            if safe:
                return e.response.status_code
            raise
