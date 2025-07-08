# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later


import httpx


class OpenvasdAPI:
    def __init__(
        self, client: httpx.Client, *, suppress_exceptions: bool = False
    ):
        """
        Initialize the OpenvasdAPI entry point.

        Args:
            client: An initialized `httpx.Client` configured for communicating
                    with the openvasd server.
            suppress_exceptions: If True, suppress exceptions and return structured error responses.
                Default is False, which means exceptions will be raised.
        """
        self._client = client
        self._suppress_exceptions = suppress_exceptions
