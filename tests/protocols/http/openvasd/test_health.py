#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock

import httpx

from gvm.protocols.http.openvasd._health import HealthAPI


def _mock_response(status_code=200):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = status_code
    mock_response.raise_for_status = MagicMock()
    return mock_response


class TestHealthAPI(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=httpx.Client)

    def test_alive_returns_status_code(self):
        mock_response = _mock_response(200)
        self.mock_client.get.return_value = mock_response

        health_api = HealthAPI(self.mock_client)
        result = health_api.get_alive()
        self.mock_client.get.assert_called_once_with("/health/alive")
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, 200)

    def test_alive_raises_httpx_error_returns_503_with_suppress_exceptions(
        self,
    ):
        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Not OK", request=MagicMock(), response=MagicMock(status_code=503)
        )

        health_api = HealthAPI(self.mock_client, suppress_exceptions=True)
        result = health_api.get_alive()
        self.assertEqual(result, 503)

    def test_alive_raises_httpx_error(self):
        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Not OK", request=MagicMock(), response=MagicMock(status_code=503)
        )
        health_api = HealthAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            health_api.get_alive()

    def test_ready_returns_status_code(self):
        mock_response = _mock_response(204)
        self.mock_client.get.return_value = mock_response

        health_api = HealthAPI(self.mock_client)
        result = health_api.get_ready()
        self.mock_client.get.assert_called_once_with("/health/ready")
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, 204)

    def test_ready_raises_httpx_error_returns_503_with_suppress_exceptions(
        self,
    ):
        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Not OK", request=MagicMock(), response=MagicMock(status_code=503)
        )

        health_api = HealthAPI(self.mock_client, suppress_exceptions=True)
        result = health_api.get_ready()
        self.assertEqual(result, 503)

    def test_ready_raises_httpx_error(self):
        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Not OK", request=MagicMock(), response=MagicMock(status_code=503)
        )
        health_api = HealthAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            health_api.get_ready()

    def test_started_returns_status_code(self):
        mock_response = _mock_response(202)
        self.mock_client.get.return_value = mock_response

        health_api = HealthAPI(self.mock_client)
        result = health_api.get_started()
        self.mock_client.get.assert_called_once_with("/health/started")
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, 202)

    def test_started_raises_httpx_error_returns_503_with_suppress_exceptions(
        self,
    ):
        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Not OK", request=MagicMock(), response=MagicMock(status_code=503)
        )

        health_api = HealthAPI(self.mock_client, suppress_exceptions=True)
        result = health_api.get_started()
        self.assertEqual(result, 503)

    def test_started_raises_httpx_error(self):
        self.mock_client.get.side_effect = httpx.HTTPStatusError(
            "Not OK", request=MagicMock(), response=MagicMock(status_code=503)
        )

        health_api = HealthAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            health_api.get_started()
