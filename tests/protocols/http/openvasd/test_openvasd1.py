# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock, patch

from gvm.protocols.http.openvasd.openvasdv1 import OpenvasdHttpApiV1


class TestOpenvasdHttpApiV1(unittest.TestCase):

    @patch("gvm.protocols.http.openvasd.openvasdv1.OpenvasdClient")
    def test_initializes_all_sub_apis(self, mock_openvasd_client_class):
        mock_httpx_client = MagicMock()
        mock_openvasd_client_instance = MagicMock()
        mock_openvasd_client_instance.client = mock_httpx_client
        mock_openvasd_client_class.return_value = mock_openvasd_client_instance

        api = OpenvasdHttpApiV1(
            host_name="localhost",
            port=3000,
            api_key="test-key",
            server_ca_path="/path/to/ca.pem",
            client_cert_paths=("/path/to/client.pem", "/path/to/key.pem"),
        )

        mock_openvasd_client_class.assert_called_once_with(
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
