# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Module for handling GVM HTTP API connections
"""

import urllib.parse
from typing import Any, MutableMapping, Optional, Tuple, Union

from httpx import Client

from gvm.protocols.http.core.response import HttpResponse


class HttpApiConnector:
    """
    Class for connecting to HTTP based API servers, sending requests and receiving the responses.
    """

    @classmethod
    def _new_client(
        cls,
        server_ca_path: Optional[str] = None,
        client_cert_paths: Optional[Union[str, Tuple[str, str]]] = None,
    ):
        """
        Creates a new httpx client
        """
        return Client(
            verify=server_ca_path if server_ca_path else False,
            cert=client_cert_paths,
        )

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
        client_cert_paths: Optional[Union[str, Tuple[str, str]]] = None,
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

        self._client: Client = self._new_client(
            server_ca_path, client_cert_paths
        )

    def update_headers(self, new_headers: MutableMapping[str, str]) -> None:
        """
        Updates the headers sent with each request, e.g. for passing an API key

        Args:
            new_headers: MutableMapping, e.g. dict, containing the new headers
        """
        self._client.headers.update(new_headers)

    def delete(
        self,
        rel_path: str,
        *,
        raise_for_status: bool = True,
        params: Optional[MutableMapping[str, str]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
    ) -> HttpResponse:
        """
        Sends a ``DELETE`` request and returns the response.

        Args:
            rel_path: The relative path for the request
            raise_for_status: Whether to raise an error if response has a
             non-success HTTP status code
            params: Optional MutableMapping, e.g. dict of URL-encoded parameters
            headers: Optional additional headers added to the request

        Return:
            The HTTP response.
        """
        url = self.url_join(self.base_url, rel_path)
        r = self._client.delete(url, params=params, headers=headers)
        if raise_for_status:
            r.raise_for_status()
        return HttpResponse.from_requests_lib(r)

    def get(
        self,
        rel_path: str,
        *,
        raise_for_status: bool = True,
        params: Optional[MutableMapping[str, str]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
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
        r = self._client.get(url, params=params, headers=headers)
        if raise_for_status:
            r.raise_for_status()
        return HttpResponse.from_requests_lib(r)

    def post_json(
        self,
        rel_path: str,
        json: Any,
        *,
        raise_for_status: bool = True,
        params: Optional[MutableMapping[str, str]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
    ) -> HttpResponse:
        """
        Sends a ``POST`` request, using the given JSON-compatible object as the
         request body, and returns the response.

        Args:
            rel_path: The relative path for the request
            json: The object to use as the request body.
            raise_for_status: Whether to raise an error if response has a
             non-success HTTP status code
            params: Optional MutableMapping, e.g. dict of URL-encoded parameters
            headers: Optional additional headers added to the request

        Return:
            The HTTP response.
        """
        url = self.url_join(self.base_url, rel_path)
        r = self._client.post(url, json=json, params=params, headers=headers)
        if raise_for_status:
            r.raise_for_status()
        return HttpResponse.from_requests_lib(r)
