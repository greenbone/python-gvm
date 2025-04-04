#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from http import HTTPStatus
from typing import Optional
from unittest.mock import Mock, patch

from gvm.errors import InvalidArgumentType

from gvm.http.core.headers import ContentType
from gvm.http.core.response import HttpResponse
from gvm.http.openvasd.openvasd1 import OpenvasdHttpApiV1


def new_mock_empty_response(
    status: Optional[int | HTTPStatus] = None,
    headers: Optional[dict[str, str]] = None,
):
    if status is None:
        status = int(HTTPStatus.NO_CONTENT)
    if headers is None:
        headers = []
    content_type = ContentType.from_string(None)
    return HttpResponse(
        body=None, status=status, headers=headers, content_type=content_type
    )


class OpenvasdHttpApiV1TestCase(unittest.TestCase):

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_init(self, mock_connector: Mock):
        api = OpenvasdHttpApiV1(mock_connector)
        mock_connector.update_headers.assert_not_called()
        self.assertIsNotNone(api)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_init_with_api_key(self, mock_connector: Mock):
        api = OpenvasdHttpApiV1(mock_connector, api_key="my-API-key")
        mock_connector.update_headers.assert_called_once_with(
            {"X-API-KEY": "my-API-key"}
        )
        self.assertIsNotNone(api)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_health_alive(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_health_alive()
        mock_connector.get.assert_called_once_with(
            "/health/alive", raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_health_ready(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_health_ready()
        mock_connector.get.assert_called_once_with(
            "/health/ready", raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_health_started(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_health_started()
        mock_connector.get.assert_called_once_with(
            "/health/started", raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_notus_os_list(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_notus_os_list()
        mock_connector.get.assert_called_once_with(
            "/notus", raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_run_notus_scan(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.post_json.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.run_notus_scan("Debian 11", ["foo-1.0", "bar-0.23"])
        mock_connector.post_json.assert_called_once_with(
            "/notus/Debian%2011",
            ["foo-1.0", "bar-0.23"],
            raise_for_status=False,
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_scan_preferences(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_scan_preferences()
        mock_connector.get.assert_called_once_with(
            "/scans/preferences", raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_create_scan(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.post_json.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        # minimal scan
        response = api.create_scan(
            {"hosts": "somehost"},
            ["some_vt", "another_vt"],
        )
        mock_connector.post_json.assert_called_once_with(
            "/scans",
            {
                "target": {"hosts": "somehost"},
                "vts": ["some_vt", "another_vt"],
            },
            raise_for_status=False,
        )

        # scan with all options
        mock_connector.post_json.reset_mock()
        response = api.create_scan(
            {"hosts": "somehost"},
            ["some_vt", "another_vt"],
            {"my_scanner_param": "abc"},
        )
        mock_connector.post_json.assert_called_once_with(
            "/scans",
            {
                "target": {"hosts": "somehost"},
                "vts": ["some_vt", "another_vt"],
                "scan_preferences": {"my_scanner_param": "abc"},
            },
            raise_for_status=False,
        )
        self.assertEqual(expected_response, response)
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_delete_scan(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.delete.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.delete_scan("foo bar")
        mock_connector.delete.assert_called_once_with(
            "/scans/foo%20bar", raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_scans(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_scans()
        mock_connector.get.assert_called_once_with(
            "/scans", raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_scan(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_scan("foo bar")
        mock_connector.get.assert_called_once_with(
            "/scans/foo%20bar", raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_scan_results(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_scan_results("foo bar")
        mock_connector.get.assert_called_once_with(
            "/scans/foo%20bar/results", params={}, raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_scan_results_with_ranges(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        # range start only
        response = api.get_scan_results("foo bar", 12)
        mock_connector.get.assert_called_once_with(
            "/scans/foo%20bar/results",
            params={"range": "12"},
            raise_for_status=False,
        )
        self.assertEqual(expected_response, response)

        # range start and end
        mock_connector.get.reset_mock()
        response = api.get_scan_results("foo bar", 12, 34)
        mock_connector.get.assert_called_once_with(
            "/scans/foo%20bar/results",
            params={"range": "12-34"},
            raise_for_status=False,
        )
        self.assertEqual(expected_response, response)

        # range end only
        mock_connector.get.reset_mock()
        response = api.get_scan_results("foo bar", range_end=23)
        mock_connector.get.assert_called_once_with(
            "/scans/foo%20bar/results",
            params={"range": "0-23"},
            raise_for_status=False,
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_scan_results_with_invalid_ranges(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        # range start
        self.assertRaises(
            InvalidArgumentType, api.get_scan_results, "foo bar", "invalid"
        )

        # range start and end
        self.assertRaises(
            InvalidArgumentType, api.get_scan_results, "foo bar", 12, "invalid"
        )

        # range end only
        self.assertRaises(
            InvalidArgumentType,
            api.get_scan_results,
            "foo bar",
            range_end="invalid",
        )

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_scan_result(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_scan_result("foo bar", "baz qux")
        mock_connector.get.assert_called_once_with(
            "/scans/foo%20bar/results/baz%20qux", raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_scan_status(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_scan_status("foo bar")
        mock_connector.get.assert_called_once_with(
            "/scans/foo%20bar/status", raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_run_scan_action(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.post_json.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.run_scan_action("foo bar", "do-something")
        mock_connector.post_json.assert_called_once_with(
            "/scans/foo%20bar",
            {"action": "do-something"},
            raise_for_status=False,
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_start_scan(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.post_json.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.start_scan("foo bar")
        mock_connector.post_json.assert_called_once_with(
            "/scans/foo%20bar", {"action": "start"}, raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_stop_scan(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.post_json.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.stop_scan("foo bar")
        mock_connector.post_json.assert_called_once_with(
            "/scans/foo%20bar", {"action": "stop"}, raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_vts(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_vts()
        mock_connector.get.assert_called_once_with(
            "/vts", raise_for_status=False
        )
        self.assertEqual(expected_response, response)

    @patch("gvm.http.core.connector.HttpApiConnector", autospec=True)
    def test_get_vt(self, mock_connector: Mock):
        expected_response = new_mock_empty_response()
        mock_connector.get.return_value = expected_response
        api = OpenvasdHttpApiV1(mock_connector)

        response = api.get_vt("foo bar")
        mock_connector.get.assert_called_once_with(
            "/vts/foo%20bar", raise_for_status=False
        )
        self.assertEqual(expected_response, response)
