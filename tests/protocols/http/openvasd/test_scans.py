# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock

import httpx

from gvm.errors import InvalidArgumentType
from gvm.protocols.http.openvasd._scans import (
    Credential,
    CredentialUP,
    ScanAction,
    ScanPreference,
    ScansAPI,
    Target,
    VTParameter,
    VTSelection,
)


def _mock_response(status_code=200, json_data=None):
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    resp.raise_for_status = MagicMock()
    return resp


class TestScansAPI(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=httpx.Client)

    def test_create_scan_success(self):
        mock_resp = _mock_response()
        self.mock_client.post.return_value = mock_resp

        api = ScansAPI(self.mock_client)

        target = Target(
            hosts=["localhost"],
            credentials=[
                Credential(
                    service="ssh",
                    port=22,
                    up=CredentialUP(username="user", password="pass"),
                )
            ],
        )
        vt_selection = [
            VTSelection(
                oid="1.3.6.1.4.1.25623.1.0.100001",
                parameters=[VTParameter(id=1, value="true")],
            )
        ]
        preferences = [
            ScanPreference(id="auto_enable_dependencies", value="True")
        ]

        api.create(target, vt_selection, scan_preferences=preferences)

        self.mock_client.post.assert_called_once_with(
            "/scans",
            json={
                "target": {
                    "hosts": ["localhost"],
                    "excluded_hosts": [],
                    "ports": [],
                    "credentials": [
                        {
                            "service": "ssh",
                            "port": 22,
                            "up": {
                                "username": "user",
                                "password": "pass",
                                "privilege_username": None,
                                "privilege_password": None,
                            },
                            "krb5": None,
                            "usk": None,
                            "snmp": None,
                        }
                    ],
                    "alive_test_ports": [],
                    "alive_test_methods": [],
                    "reverse_lookup_unify": False,
                    "reverse_lookup_only": False,
                },
                "vts": [
                    {
                        "oid": "1.3.6.1.4.1.25623.1.0.100001",
                        "parameters": [{"id": 1, "value": "true"}],
                    }
                ],
                "scan_preferences": [
                    {"id": "auto_enable_dependencies", "value": "True"}
                ],
            },
        )

    def test_create_scan_without_scan_preferences(self):
        mock_resp = _mock_response()
        self.mock_client.post.return_value = mock_resp

        api = ScansAPI(self.mock_client)

        target = Target(hosts=["localhost"])
        vt_selection = [VTSelection(oid="1.3.6.1.4.1.25623.1.0.100001")]

        api.create(target, vt_selection)

        self.mock_client.post.assert_called_once_with(
            "/scans",
            json={
                "target": {
                    "hosts": ["localhost"],
                    "excluded_hosts": [],
                    "ports": [],
                    "credentials": [],
                    "alive_test_ports": [],
                    "alive_test_methods": [],
                    "reverse_lookup_unify": False,
                    "reverse_lookup_only": False,
                },
                "vts": [
                    {"oid": "1.3.6.1.4.1.25623.1.0.100001", "parameters": []}
                ],
            },
        )

    def test_create_scan_failure_raises_httpx_error(self):
        mock_response = _mock_response()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request",
            request=MagicMock(),
            response=MagicMock(status_code=400),
        )
        self.mock_client.post.return_value = mock_response

        api = ScansAPI(self.mock_client)

        target = Target(hosts=["localhost"])
        vt_selection = [VTSelection(oid="test-oid")]
        preferences = [ScanPreference(id="test", value="4")]

        with self.assertRaises(httpx.HTTPStatusError):
            api.create(target, vt_selection, scan_preferences=preferences)

        self.mock_client.post.assert_called_once_with(
            "/scans",
            json={
                "target": {
                    "hosts": ["localhost"],
                    "excluded_hosts": [],
                    "ports": [],
                    "credentials": [],
                    "alive_test_ports": [],
                    "alive_test_methods": [],
                    "reverse_lookup_unify": False,
                    "reverse_lookup_only": False,
                },
                "vts": [{"oid": "test-oid", "parameters": []}],
                "scan_preferences": [{"id": "test", "value": "4"}],
            },
        )

    def test_create_scan_failure_httpx_error_with_suppress_exceptions(self):
        mock_response = _mock_response()
        mock_http_error = httpx.HTTPStatusError(
            "Bad Request",
            request=MagicMock(),
            response=MagicMock(status_code=400),
        )
        mock_response.raise_for_status.side_effect = mock_http_error
        self.mock_client.post.return_value = mock_response

        api = ScansAPI(self.mock_client, suppress_exceptions=True)

        target = Target(hosts=["localhost"])
        vt_selection = [VTSelection(oid="1")]
        preferences = [ScanPreference(id="test", value="4")]

        response = api.create(
            target, vt_selection, scan_preferences=preferences
        )

        self.mock_client.post.assert_called_once_with(
            "/scans",
            json={
                "target": {
                    "hosts": ["localhost"],
                    "excluded_hosts": [],
                    "ports": [],
                    "credentials": [],
                    "alive_test_ports": [],
                    "alive_test_methods": [],
                    "reverse_lookup_unify": False,
                    "reverse_lookup_only": False,
                },
                "vts": [{"oid": "1", "parameters": []}],
                "scan_preferences": [{"id": "test", "value": "4"}],
            },
        )

        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 400)

    def test_delete_scan_success(self):
        mock_resp = _mock_response(status_code=204)
        self.mock_client.delete.return_value = mock_resp

        api = ScansAPI(self.mock_client)
        result = api.delete("scan-123")
        self.assertEqual(result, 204)

    def test_delete_scan_returns_500_on_httpx_error_with_suppress_exceptions(
        self,
    ):
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 500

        self.mock_client.delete.side_effect = httpx.HTTPStatusError(
            "failed", request=MagicMock(), response=mock_response
        )

        api = ScansAPI(self.mock_client, suppress_exceptions=True)
        status = api.delete("scan-1")
        self.assertEqual(status, 500)

    def test_delete_scan_raise_on_httpx_error(self):
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 500

        self.mock_client.delete.side_effect = httpx.HTTPStatusError(
            "failed", request=MagicMock(), response=mock_response
        )

        api = ScansAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.delete("scan-1")

    def test_get_all_scans(self):
        mock_resp = _mock_response()
        self.mock_client.get.return_value = mock_resp

        api = ScansAPI(self.mock_client)
        result = api.get_all()
        self.mock_client.get.assert_called_once_with("/scans")
        self.assertEqual(result, mock_resp)

    def test_get_all_scans_failure_raises_httpx_error(self):
        mock_response = _mock_response()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        self.mock_client.get.return_value = mock_response

        api = ScansAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.get_all()

        self.mock_client.get.assert_called_once_with("/scans")

    def test_get_all_scans_failure_returns_500_with_suppress_exceptions(self):
        mock_response = _mock_response()
        mock_http_error = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        mock_response.raise_for_status.side_effect = mock_http_error
        self.mock_client.get.return_value = mock_response

        api = ScansAPI(self.mock_client, suppress_exceptions=True)
        response = api.get_all()

        self.mock_client.get.assert_called_once_with("/scans")
        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 500)

    def test_get_scan_by_id(self):
        mock_resp = _mock_response()
        self.mock_client.get.return_value = mock_resp

        api = ScansAPI(self.mock_client)
        result = api.get("scan-1")
        self.mock_client.get.assert_called_once_with("/scans/scan-1")
        self.assertEqual(result, mock_resp)

    def test_get_scan_by_id_failure_raises_httpx_error(self):
        mock_response = _mock_response()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        self.mock_client.get.return_value = mock_response

        api = ScansAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.get("scan-1")

        self.mock_client.get.assert_called_once_with("/scans/scan-1")

    def test_get_scan_by_id_failure_return_500_httpx_error_with_suppress_exceptions(
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

        api = ScansAPI(self.mock_client, suppress_exceptions=True)
        response = api.get("scan-1")

        self.mock_client.get.assert_called_once_with("/scans/scan-1")
        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 500)

    def test_get_results_with_range(self):
        mock_resp = _mock_response()
        self.mock_client.get.return_value = mock_resp

        api = ScansAPI(self.mock_client)
        api.get_results("scan-1", range_start=5, range_end=10)
        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={"range": "5-10"}
        )

    def test_get_results_only_range_start(self):
        mock_response = _mock_response()
        self.mock_client.get.return_value = mock_response

        api = ScansAPI(self.mock_client)
        result = api.get_results("scan-1", range_start=7)
        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={"range": "7"}
        )
        self.assertEqual(result, mock_response)

    def test_get_results_only_range_end(self):
        mock_response = _mock_response()
        self.mock_client.get.return_value = mock_response

        api = ScansAPI(self.mock_client)
        result = api.get_results("scan-1", range_end=9)
        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={"range": "0-9"}
        )
        self.assertEqual(result, mock_response)

    def test_get_results_without_range(self):
        mock_response = _mock_response()
        self.mock_client.get.return_value = mock_response

        api = ScansAPI(self.mock_client)
        result = api.get_results("scan-1")
        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={}
        )
        self.assertEqual(result, mock_response)

    def test_get_results_invalid_range_type_for_range_start(self):
        api = ScansAPI(self.mock_client)
        with self.assertRaises(InvalidArgumentType):
            api.get_results("scan-1", range_start="wrong", range_end=5)

    def test_get_results_invalid_range_type_for_range_end(self):
        api = ScansAPI(self.mock_client)
        with self.assertRaises(InvalidArgumentType):
            api.get_results("scan-1", range_start=5, range_end="wrong")

    def test_get_results_invalid_range_end_type_only(self):
        api = ScansAPI(self.mock_client)
        with self.assertRaises(InvalidArgumentType):
            api.get_results("scan-1", range_end="not-an-int")

    def test_get_results_with_range_failure_raises_httpx_error(self):
        mock_response = _mock_response()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        self.mock_client.get.return_value = mock_response

        api = ScansAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.get_results("scan-1", range_start=5, range_end=10)

        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={"range": "5-10"}
        )

    def test_get_results_with_range_failure_return_500_httpx_error_with_suppress_exceptions(
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

        api = ScansAPI(self.mock_client, suppress_exceptions=True)
        response = api.get_results("scan-1", range_start=5, range_end=10)

        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={"range": "5-10"}
        )
        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 500)

    def test_get_result(self):
        mock_resp = _mock_response()
        self.mock_client.get.return_value = mock_resp

        api = ScansAPI(self.mock_client)
        api.get_result("scan-1", "99")
        self.mock_client.get.assert_called_once_with("/scans/scan-1/results/99")

    def test_get_result_failure_raises_httpx_error(self):
        mock_response = _mock_response()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        self.mock_client.get.return_value = mock_response

        api = ScansAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.get_result("scan-1", "99")

        self.mock_client.get.assert_called_once_with("/scans/scan-1/results/99")

    def test_get_result_failure_return_500_httpx_error_with_suppress_exceptions(
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

        api = ScansAPI(self.mock_client, suppress_exceptions=True)
        response = api.get_result("scan-1", "99")

        self.mock_client.get.assert_called_once_with("/scans/scan-1/results/99")
        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 500)

    def test_get_status(self):
        mock_resp = _mock_response()
        self.mock_client.get.return_value = mock_resp

        api = ScansAPI(self.mock_client)
        api.get_status("scan-1")
        self.mock_client.get.assert_called_once_with("/scans/scan-1/status")

    def test_get_status_failure_raises_httpx_error(self):
        mock_response = _mock_response()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        self.mock_client.get.return_value = mock_response

        api = ScansAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api.get_status("scan-1")

        self.mock_client.get.assert_called_once_with("/scans/scan-1/status")

    def test_get_status_failure_return_500_httpx_error_with_suppress_exceptions(
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

        api = ScansAPI(self.mock_client, suppress_exceptions=True)
        response = api.get_status("scan-1")

        self.mock_client.get.assert_called_once_with("/scans/scan-1/status")
        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 500)

    def test_run_action_success(self):
        mock_resp = _mock_response(status_code=202)
        self.mock_client.post.return_value = mock_resp

        api = ScansAPI(self.mock_client)
        status = api._run_action("scan-1", ScanAction.START)
        self.assertEqual(status, 202)

    def test_run_action_failure_raise_httpx_error(self):
        self.mock_client.post.side_effect = httpx.HTTPStatusError(
            "failed", request=MagicMock(), response=MagicMock(status_code=500)
        )
        api = ScansAPI(self.mock_client)
        with self.assertRaises(httpx.HTTPStatusError):
            api._run_action("scan-1", ScanAction.STOP)

    def test_run_action_failure_returns_500_with_suppress_exceptions(self):
        self.mock_client.post.side_effect = httpx.HTTPStatusError(
            "failed", request=MagicMock(), response=MagicMock(status_code=500)
        )

        api = ScansAPI(self.mock_client, suppress_exceptions=True)
        status = api._run_action("scan-1", ScanAction.STOP)
        self.assertEqual(status, 500)

    def test_start_scan(self):
        api = ScansAPI(self.mock_client)
        api._run_action = MagicMock(return_value=200)
        result = api.start("scan-abc")
        api._run_action.assert_called_once_with("scan-abc", ScanAction.START)
        self.assertEqual(result, 200)

    def test_start_scan_failure_raises_httpx_error(self):
        api = ScansAPI(self.mock_client)
        api._run_action = MagicMock(
            side_effect=httpx.HTTPStatusError(
                "Scan start failed",
                request=MagicMock(),
                response=MagicMock(status_code=500),
            )
        )

        with self.assertRaises(httpx.HTTPStatusError):
            api.start("scan-abc")

    def test_start_scan_failure_returns_500_with_suppress_exceptions(self):
        api = ScansAPI(self.mock_client, suppress_exceptions=True)
        api._run_action = MagicMock(return_value=500)
        result = api.start("scan-abc")
        self.assertEqual(result, 500)

    def test_stop_scan(self):
        api = ScansAPI(self.mock_client)
        api._run_action = MagicMock(return_value=200)
        result = api.stop("scan-abc")
        api._run_action.assert_called_once_with("scan-abc", ScanAction.STOP)
        self.assertEqual(result, 200)

    def test_stop_scan_failure_raises_httpx_error(self):
        api = ScansAPI(self.mock_client)
        api._run_action = MagicMock(
            side_effect=httpx.HTTPStatusError(
                "Scan stop failed",
                request=MagicMock(),
                response=MagicMock(status_code=500),
            )
        )

        with self.assertRaises(httpx.HTTPStatusError):
            api.stop("scan-abc")

    def test_stop_scan_failure_returns_500_with_suppress_exceptions(self):
        api = ScansAPI(self.mock_client, suppress_exceptions=True)
        api._run_action = MagicMock(return_value=500)
        result = api.stop("scan-abc")
        self.assertEqual(result, 500)

    def test_get_preferences_success(self):
        mock_resp = _mock_response(
            200,
            [
                {
                    "id": "optimize_test",
                    "name": "Optimize Test",
                    "default": True,
                    "description": "By default, optimize_test is enabled...",
                }
            ],
        )
        self.mock_client.get.return_value = mock_resp

        api = ScansAPI(self.mock_client)
        response = api.get_preferences()

        self.mock_client.get.assert_called_once_with("/scans/preferences")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["id"], "optimize_test")

    def test_get_preferences_failure_raises_httpx_error(self):
        mock_resp = _mock_response()
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        self.mock_client.get.return_value = mock_resp

        api = ScansAPI(self.mock_client)

        with self.assertRaises(httpx.HTTPStatusError):
            api.get_preferences()

        self.mock_client.get.assert_called_once_with("/scans/preferences")

    def test_get_preferences_suppressed_exception_returns_response(self):
        mock_error_response = MagicMock(status_code=400)
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request",
            request=MagicMock(),
            response=mock_error_response,
        )
        self.mock_client.get.return_value = mock_resp

        api = ScansAPI(self.mock_client, suppress_exceptions=True)
        response = api.get_preferences()

        self.mock_client.get.assert_called_once_with("/scans/preferences")
        self.assertEqual(response, mock_error_response)
        self.assertEqual(response.status_code, 400)
