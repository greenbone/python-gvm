#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later

import ssl
import unittest
from unittest.mock import MagicMock, patch

from gvm.protocols.http.openvasd._client import create_openvasd_http_client


class TestOpenvasdClient(unittest.TestCase):
    @patch("gvm.protocols.http.openvasd._client.Client")
    def test_init_without_tls_or_api_key(self, mock_httpx_client):
        create_openvasd_http_client("localhost")
        mock_httpx_client.assert_called_once()
        _, kwargs = mock_httpx_client.call_args
        self.assertEqual(kwargs["base_url"], "http://localhost:3000")
        self.assertFalse(kwargs["verify"])
        self.assertNotIn("X-API-KEY", kwargs["headers"])

    @patch("gvm.protocols.http.openvasd._client.Client")
    def test_init_with_api_key_only(self, mock_httpx_client):
        create_openvasd_http_client("localhost", api_key="secret")
        _, kwargs = mock_httpx_client.call_args
        self.assertEqual(kwargs["headers"]["X-API-KEY"], "secret")
        self.assertEqual(kwargs["base_url"], "http://localhost:3000")
        self.assertFalse(kwargs["verify"])

    @patch("gvm.protocols.http.openvasd._client.ssl.create_default_context")
    @patch("gvm.protocols.http.openvasd._client.Client")
    def test_init_with_mtls_tuple(
        self, mock_httpx_client, mock_ssl_ctx_factory
    ):
        mock_context = MagicMock(spec=ssl.SSLContext)
        mock_ssl_ctx_factory.return_value = mock_context

        create_openvasd_http_client(
            "localhost",
            server_ca_path="/path/ca.pem",
            client_cert_paths=("/path/cert.pem", "/path/key.pem"),
        )

        mock_ssl_ctx_factory.assert_called_once_with(
            ssl.Purpose.SERVER_AUTH, cafile="/path/ca.pem"
        )
        mock_context.load_cert_chain.assert_called_once_with(
            certfile="/path/cert.pem", keyfile="/path/key.pem"
        )
        mock_httpx_client.assert_called_once()
        _, kwargs = mock_httpx_client.call_args
        self.assertEqual(kwargs["base_url"], "https://localhost:3000")
        self.assertEqual(kwargs["verify"], mock_context)

    @patch("gvm.protocols.http.openvasd._client.ssl.create_default_context")
    @patch("gvm.protocols.http.openvasd._client.Client")
    def test_init_with_mtls_single_cert(
        self, mock_httpx_client, mock_ssl_ctx_factory
    ):
        mock_context = MagicMock(spec=ssl.SSLContext)
        mock_ssl_ctx_factory.return_value = mock_context

        create_openvasd_http_client(
            "localhost",
            server_ca_path="/path/ca.pem",
            client_cert_paths="/path/client.pem",
        )

        mock_context.load_cert_chain.assert_called_once_with(
            certfile="/path/client.pem"
        )
        _, kwargs = mock_httpx_client.call_args
        self.assertEqual(kwargs["base_url"], "https://localhost:3000")
        self.assertEqual(kwargs["verify"], mock_context)
