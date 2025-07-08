# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock

import httpx

from gvm.protocols.http.openvasd._vts import VtsAPI


def _mock_response(status_code=200):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = status_code
    mock_response.raise_for_status = MagicMock()
    return mock_response


class TestVtsAPI(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=httpx.Client)

    def test_get_all_returns_response(self):
        mock_response = _mock_response(200)
        self.mock_client.get.return_value = mock_response

        api = VtsAPI(self.mock_client)
        response = api.get_all()
        self.mock_client.get.assert_called_once_with("/vts")
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(response, mock_response)

    def test_get_all_raises_httpx_error(self):
        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock(status_code=500)
        )
        api = VtsAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.get_all()

    def test_get_all_returns_response_on_httpx_error_with_suppress_exceptions(
        self,
    ):
        mock_response = _mock_response()
        mock_http_error = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        mock_response.raise_for_status.side_effect = mock_http_error
        self.mock_client.get.return_value = mock_response

        api = VtsAPI(self.mock_client, suppress_exceptions=True)
        result = api.get_all()

        self.mock_client.get.assert_called_once_with("/vts")
        self.assertEqual(result, mock_http_error.response)

    def test_get_by_oid_returns_response(self):
        mock_response = _mock_response(200)
        self.mock_client.get.return_value = mock_response

        oid = "1.3.6.1.4.1.25623.1.0.123456"
        api = VtsAPI(self.mock_client)
        response = api.get(oid)
        self.mock_client.get.assert_called_once_with(f"/vts/{oid}")
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(response, mock_response)

    def test_get_by_oid_raises_httpx_error(self):
        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404),
        )

        api = VtsAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.get("nonexistent-oid")

    def test_get_by_oid_response_on_httpx_error_with_suppress_exceptions(self):
        mock_response = _mock_response()
        mock_http_error = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404),
        )
        mock_response.raise_for_status.side_effect = mock_http_error
        self.mock_client.get.return_value = mock_response

        api = VtsAPI(self.mock_client, suppress_exceptions=True)
        response = api.get("nonexistent-oid")

        self.assertEqual(response, mock_http_error.response)
