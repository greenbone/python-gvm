# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Module for handling GVM HTTP API connections
"""

import urllib.parse
from typing import Any, Dict, Optional, Tuple

from requests import Session

from gvm.http.core.response import HttpResponse


class HttpApiConnector:
    """
    Class for connecting to HTTP based API servers, sending requests and receiving the responses.
    """

    @classmethod
    def _new_session(cls):
        """
        Creates a new session
        """
        return Session()

    @classmethod
    def url_join(cls, base: str, rel_path: str) -> str:
        """
        Combines a base URL and a relative path into one URL.

        Unlike `urrlib.parse.urljoin` the base path will always be the parent of the
         relative path as if it ends with "/".
        """
        if base.endswith("/"):
            return urllib.parse.urljoin(base, rel_path)

        return urllib.parse.urljoin(base + "/", rel_path)

    def __init__(
        self,
        base_url: str,
        *,
        server_ca_path: Optional[str] = None,
        client_cert_paths: Optional[str | Tuple[str]] = None,
    ):
        """
        Create a new HTTP API Connector.

        Args:
            base_url: The base server URL to which request-specific paths will be appended
             for the requests
            server_ca_path: Optional path to a CA certificate for verifying the server.
                If none is given, server verification is disabled.
            client_cert_paths: Optional path to a client private key and certificate
             for authentication.
             Can be a combined key and certificate file or a tuple containing separate files.
             The key must not be encrypted.
        """

        self.base_url = base_url
        "The base server URL to which request-specific paths will be appended for the requests"

        self._session = self._new_session()
        "Internal session handling the HTTP requests"
        if server_ca_path:
            self._session.verify = server_ca_path
        if client_cert_paths:
            self._session.cert = client_cert_paths

    def update_headers(self, new_headers: Dict[str, str]) -> None:
        """
        Updates the headers sent with each request, e.g. for passing an API key

        Args:
            new_headers: Dict containing the new headers
        """
        self._session.headers.update(new_headers)

    def delete(
        self,
        rel_path: str,
        *,
        raise_for_status: bool = True,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> HttpResponse:
        """
        Sends a ``DELETE`` request and returns the response.

        Args:
            rel_path: The relative path for the request
            raise_for_status: Whether to raise an error if response has a
             non-success HTTP status code
            params: Optional dict of URL-encoded parameters
            headers: Optional additional headers added to the request

        Return:
            The HTTP response.
        """
        url = self.url_join(self.base_url, rel_path)
        r = self._session.delete(url, params=params, headers=headers)
        if raise_for_status:
            r.raise_for_status()
        return HttpResponse.from_requests_lib(r)

    def get(
        self,
        rel_path: str,
        *,
        raise_for_status: bool = True,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> HttpResponse:
        """
        Sends a ``GET`` request and returns the response.

        Args:
            rel_path: The relative path for the request
            raise_for_status: Whether to raise an error if response has a
             non-success HTTP status code
            params: Optional dict of URL-encoded parameters
            headers: Optional additional headers added to the request

        Return:
            The HTTP response.
        """
        url = self.url_join(self.base_url, rel_path)
        r = self._session.get(url, params=params, headers=headers)
        if raise_for_status:
            r.raise_for_status()
        return HttpResponse.from_requests_lib(r)

    def post_json(
        self,
        rel_path: str,
        json: Any,
        *,
        raise_for_status: bool = True,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> HttpResponse:
        """
        Sends a ``POST`` request, using the given JSON-compatible object as the
         request body, and returns the response.

        Args:
            rel_path: The relative path for the request
            json: The object to use as the request body.
            raise_for_status: Whether to raise an error if response has a
             non-success HTTP status code
            params: Optional dict of URL-encoded parameters
            headers: Optional additional headers added to the request

        Return:
            The HTTP response.
        """
        url = self.url_join(self.base_url, rel_path)
        r = self._session.post(url, json=json, params=params, headers=headers)
        if raise_for_status:
            r.raise_for_status()
        return HttpResponse.from_requests_lib(r)
