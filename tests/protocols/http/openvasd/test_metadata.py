# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock

import httpx

from gvm.protocols.http.openvasd._metadata import (
    Metadata,
    MetadataAPI,
    MetadataError,
)


def _mock_head_response(status_code=200, headers=None):
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.headers = headers or {}
    response.raise_for_status = MagicMock()
    return response


class TestMetadataAPI(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=httpx.Client)

    def test_get_successful(self):
        headers = {
            "api-version": "1.0",
            "feed-version": "2025.01",
            "authentication": "API-KEY",
        }
        mock_response = _mock_head_response(200, headers)
        self.mock_client.head.return_value = mock_response

        api = MetadataAPI(self.mock_client)
        result = api.get()
        self.mock_client.head.assert_called_once_with("/")
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(
            result,
            Metadata(
                api_version="1.0",
                feed_version="2025.01",
                authentication="API-KEY",
            ),
        )

    def test_get_unauthorized_with_suppress_exceptions(self):
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 401

        self.mock_client.head.side_effect = httpx.HTTPStatusError(
            "Unauthorized", request=MagicMock(), response=mock_response
        )

        api = MetadataAPI(self.mock_client, suppress_exceptions=True)
        result = api.get()
        self.assertEqual(
            result, MetadataError(error="Unauthorized", status_code=401)
        )

    def test_get_failure_raises_httpx_error(self):
        mock_response = _mock_head_response(500, None)
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        self.mock_client.head.return_value = mock_response

        api = MetadataAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.get()

        self.mock_client.head.assert_called_once_with("/")

    def test_get_scans_successful(self):
        headers = {
            "api-version": "1.0",
            "feed-version": "2025.01",
            "authentication": "API-KEY",
        }
        mock_response = _mock_head_response(200, headers)
        self.mock_client.head.return_value = mock_response

        api = MetadataAPI(self.mock_client)
        result = api.get_scans()
        self.mock_client.head.assert_called_once_with("/scans")
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(
            result,
            Metadata(
                api_version="1.0",
                feed_version="2025.01",
                authentication="API-KEY",
            ),
        )

    def test_get_scans_unauthorized_with_suppress_exceptions(self):
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 401

        self.mock_client.head.side_effect = httpx.HTTPStatusError(
            "Unauthorized", request=MagicMock(), response=mock_response
        )

        api = MetadataAPI(self.mock_client, suppress_exceptions=True)
        result = api.get_scans()
        self.assertEqual(
            result, MetadataError(error="Unauthorized", status_code=401)
        )

    def test_get_scans_failure_raises_httpx_error(self):
        mock_response = _mock_head_response(500, None)
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        self.mock_client.head.return_value = mock_response

        api = MetadataAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.get_scans()

        self.mock_client.head.assert_called_once_with("/scans")
