# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.http.core.connector import HttpApiConnector


class GvmHttpApi:
    """
    Base class for HTTP-based GVM APIs.
    """

    def __init__(self, connector: HttpApiConnector, *, api_key: Optional[str] = None):
        """
        Create a new generic GVM HTTP API instance.

        Args:
            connector: The connector handling the HTTP(S) connection
            api_key: Optional API key for authentication
        """

        "The connector handling the HTTP(S) connection"
        self._connector: HttpApiConnector = connector

        "Optional API key for authentication"
        self._api_key: Optional[str] = api_key
