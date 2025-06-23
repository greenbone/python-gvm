# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock

import httpx

from gvm.protocols.http.openvasd.notus import NotusAPI


def _mock_response(status_code=200, json_data=None):
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.json.return_value = json_data or []
    response.raise_for_status = MagicMock()
    return response


class TestNotusAPI(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=httpx.Client)
        self.api = NotusAPI(self.mock_client)

    def test_get_os_list_success(self):
        mock_response = _mock_response(json_data=["debian", "alpine"])
        self.mock_client.get.return_value = mock_response

        result = self.api.get_os_list()
        self.mock_client.get.assert_called_once_with("/notus")
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, mock_response)

    def test_get_os_list_http_error_with_safe_true(self):
        mock_response = MagicMock()
        mock_response.status_code = 500

        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Internal Server Error", request=MagicMock(), response=mock_response
        )

        result = self.api.get_os_list(safe=True)

        self.assertEqual(result, mock_response)

    def test_get_os_list_http_error(self):
        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock(status_code=500)
        )

        with self.assertRaises(httpx.HTTPStatusError):
            self.api.get_os_list()

    def test_run_scan_success(self):
        mock_response = _mock_response(json_data={"vulnerabilities": []})
        self.mock_client.post.return_value = mock_response

        result = self.api.run_scan("debian", ["openssl", "bash"])
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
        self.api.run_scan(os_name, ["musl"])
        self.mock_client.post.assert_called_once_with(
            f"/notus/{encoded}", json=["musl"]
        )

    def test_run_scan_http_error(self):
        self.mock_client.post.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock(status_code=400)
        )

        with self.assertRaises(httpx.HTTPStatusError):
            self.api.run_scan("ubuntu", ["curl"])

    def test_run_scan_http_error_with_safe_true(self):
        mock_response = MagicMock()
        mock_response.status_code = 500
        self.mock_client.post.side_effect = httpx.HTTPStatusError(
            "Internal Server Error", request=MagicMock(), response=mock_response
        )

        response = self.api.run_scan("ubuntu", ["curl"], safe=True)

        self.assertEqual(response, mock_response)
