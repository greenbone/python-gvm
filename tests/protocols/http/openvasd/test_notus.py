# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock

import httpx

from gvm.protocols.http.openvasd._notus import NotusAPI


def _mock_response(status_code=200, json_data=None):
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.json.return_value = json_data or []
    response.raise_for_status = MagicMock()
    return response


class TestNotusAPI(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=httpx.Client)

    def test_get_os_list_success(self):
        mock_response = _mock_response(json_data=["debian", "alpine"])
        self.mock_client.get.return_value = mock_response

        api = NotusAPI(self.mock_client)
        result = api.get_os_list()
        self.mock_client.get.assert_called_once_with("/notus")
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, mock_response)

    def test_get_os_list_http_error_with_suppress_exceptions(self):
        mock_response = MagicMock()
        mock_response.status_code = 500

        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Internal Server Error", request=MagicMock(), response=mock_response
        )

        api = NotusAPI(self.mock_client, suppress_exceptions=True)
        result = api.get_os_list()

        self.assertEqual(result, mock_response)

    def test_get_os_list_http_error(self):
        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock(status_code=500)
        )

        api = NotusAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.get_os_list()

    def test_run_scan_success(self):
        mock_response = _mock_response(json_data={"vulnerabilities": []})
        self.mock_client.post.return_value = mock_response

        api = NotusAPI(self.mock_client)
        result = api.run_scan("debian", ["openssl", "bash"])
        self.mock_client.post.assert_called_once_with(
            "/notus/debian", json=["openssl", "bash"]
        )
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, mock_response)

    def test_run_scan_with_special_os_name(self):
        mock_response = _mock_response()
        self.mock_client.post.return_value = mock_response

        os_name = "alpine linux"
        encoded = "alpine%20linux"
        api = NotusAPI(self.mock_client)
        api.run_scan(os_name, ["musl"])
        self.mock_client.post.assert_called_once_with(
            f"/notus/{encoded}", json=["musl"]
        )

    def test_run_scan_http_error(self):
        self.mock_client.post.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock(status_code=400)
        )

        api = NotusAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.run_scan("ubuntu", ["curl"])

    def test_run_scan_http_error_with_suppress_exceptions(self):
        mock_response = MagicMock()
        mock_response.status_code = 500
        self.mock_client.post.side_effect = httpx.HTTPStatusError(
            "Internal Server Error", request=MagicMock(), response=mock_response
        )

        api = NotusAPI(self.mock_client, suppress_exceptions=True)
        response = api.run_scan("ubuntu", ["curl"])

        self.assertEqual(response, mock_response)
