# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock, patch

from gvm.protocols.http.openvasd import OpenvasdHttpAPIv1


class TestOpenvasdHttpApiV1(unittest.TestCase):
    @patch("gvm.protocols.http.openvasd._openvasd1.create_openvasd_http_client")
    def test_initializes_all_sub_apis(self, mock_crate_openvasd_client):
        mock_httpx_client = MagicMock()
        mock_crate_openvasd_client.return_value = mock_httpx_client

        api = OpenvasdHttpAPIv1(
            host_name="localhost",
            port=3000,
            api_key="test-key",
            server_ca_path="/path/to/ca.pem",
            client_cert_paths=("/path/to/client.pem", "/path/to/key.pem"),
        )

        mock_crate_openvasd_client.assert_called_once_with(
            host_name="localhost",
            port=3000,
            api_key="test-key",
            server_ca_path="/path/to/ca.pem",
            client_cert_paths=("/path/to/client.pem", "/path/to/key.pem"),
        )

        self.assertEqual(api._client, mock_httpx_client)
        self.assertEqual(api.health._client, mock_httpx_client)
        self.assertEqual(api.metadata._client, mock_httpx_client)
        self.assertEqual(api.notus._client, mock_httpx_client)
        self.assertEqual(api.scans._client, mock_httpx_client)
        self.assertEqual(api.vts._client, mock_httpx_client)
