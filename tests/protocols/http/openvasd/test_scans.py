# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock

import httpx

from gvm.errors import InvalidArgumentType
from gvm.protocols.http.openvasd.scans import ScanAction, ScansAPI


def _mock_response(status_code=200, json_data=None):
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    resp.raise_for_status = MagicMock()
    return resp


class TestScansAPI(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(spec=httpx.Client)
        self.api = ScansAPI(self.mock_client)

    def test_create_scan_success(self):
        mock_resp = _mock_response()
        self.mock_client.post.return_value = mock_resp

        self.api.create({"host": "localhost"}, [{"id": "1"}], {"threads": 4})
        self.mock_client.post.assert_called_once_with(
            "/scans",
            json={
                "target": {"host": "localhost"},
                "vts": [{"id": "1"}],
                "scan_preferences": {"threads": 4},
            },
        )

    def test_create_scan_without_scan_preferences(self):
        mock_resp = _mock_response()
        self.mock_client.post.return_value = mock_resp

        self.api.create({"host": "localhost"}, [{"id": "1"}])

        self.mock_client.post.assert_called_once_with(
            "/scans",
            json={"target": {"host": "localhost"}, "vts": [{"id": "1"}]},
        )

    def test_create_scan_failure_raises_httpx_error(self):
        mock_response = _mock_response()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request",
            request=MagicMock(),
            response=MagicMock(status_code=400),
        )
        self.mock_client.post.return_value = mock_response

        with self.assertRaises(httpx.HTTPStatusError):
            self.api.create({"host": "localhost"}, [{"id": "1"}], {"test": 4})

        self.mock_client.post.assert_called_once_with(
            "/scans",
            json={
                "target": {"host": "localhost"},
                "vts": [{"id": "1"}],
                "scan_preferences": {"test": 4},
            },
        )

    def test_create_scan_failure_httpx_error_with_safe_true(self):
        mock_response = _mock_response()
        mock_http_error = httpx.HTTPStatusError(
            "Bad Request",
            request=MagicMock(),
            response=MagicMock(status_code=400),
        )
        mock_response.raise_for_status.side_effect = mock_http_error
        self.mock_client.post.return_value = mock_response

        response = self.api.create(
            {"host": "localhost"}, [{"id": "1"}], {"test": 4}, safe=True
        )

        self.mock_client.post.assert_called_once_with(
            "/scans",
            json={
                "target": {"host": "localhost"},
                "vts": [{"id": "1"}],
                "scan_preferences": {"test": 4},
            },
        )

        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 400)

    def test_delete_scan_success(self):
        mock_resp = _mock_response(status_code=204)
        self.mock_client.delete.return_value = mock_resp

        result = self.api.delete("scan-123")
        self.assertEqual(result, 204)

    def test_delete_scan_returns_500_on_httpx_error_with_safe_true(self):
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 500

        self.mock_client.delete.side_effect = httpx.HTTPStatusError(
            "failed", request=MagicMock(), response=mock_response
        )

        status = self.api.delete("scan-1", True)
        self.assertEqual(status, 500)

    def test_delete_scan_raise_on_httpx_error(self):
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 500

        self.mock_client.delete.side_effect = httpx.HTTPStatusError(
            "failed", request=MagicMock(), response=mock_response
        )

        with self.assertRaises(httpx.HTTPStatusError):
            self.api.delete("scan-1")

    def test_get_all_scans(self):
        mock_resp = _mock_response()
        self.mock_client.get.return_value = mock_resp

        result = self.api.get_all()
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

        with self.assertRaises(httpx.HTTPStatusError):
            self.api.get_all()

        self.mock_client.get.assert_called_once_with("/scans")

    def test_get_all_scans_failure_returns_500_with_safe_true(self):
        mock_response = _mock_response()
        mock_http_error = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        mock_response.raise_for_status.side_effect = mock_http_error
        self.mock_client.get.return_value = mock_response

        response = self.api.get_all(safe=True)

        self.mock_client.get.assert_called_once_with("/scans")
        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 500)

    def test_get_scan_by_id(self):
        mock_resp = _mock_response()
        self.mock_client.get.return_value = mock_resp

        result = self.api.get("scan-1")
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

        with self.assertRaises(httpx.HTTPStatusError):
            self.api.get("scan-1")

        self.mock_client.get.assert_called_once_with("/scans/scan-1")

    def test_get_scan_by_id_failure_return_500_httpx_error_with_safe_true(self):
        mock_response = _mock_response()
        mock_http_error = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        mock_response.raise_for_status.side_effect = mock_http_error
        self.mock_client.get.return_value = mock_response

        response = self.api.get("scan-1", safe=True)

        self.mock_client.get.assert_called_once_with("/scans/scan-1")
        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 500)

    def test_get_results_with_range(self):
        mock_resp = _mock_response()
        self.mock_client.get.return_value = mock_resp

        self.api.get_results("scan-1", 5, 10)
        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={"range": "5-10"}
        )

    def test_get_results_only_range_start(self):
        mock_response = _mock_response()
        self.mock_client.get.return_value = mock_response

        result = self.api.get_results("scan-1", range_start=7)
        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={"range": "7"}
        )
        self.assertEqual(result, mock_response)

    def test_get_results_only_range_end(self):
        mock_response = _mock_response()
        self.mock_client.get.return_value = mock_response

        result = self.api.get_results("scan-1", range_end=9)
        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={"range": "0-9"}
        )
        self.assertEqual(result, mock_response)

    def test_get_results_without_range(self):
        mock_response = _mock_response()
        self.mock_client.get.return_value = mock_response

        result = self.api.get_results("scan-1")
        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={}
        )
        self.assertEqual(result, mock_response)

    def test_get_results_invalid_range_type_for_range_start(self):
        with self.assertRaises(InvalidArgumentType):
            self.api.get_results("scan-1", "wrong", 5)

    def test_get_results_invalid_range_type_for_range_end(self):
        with self.assertRaises(InvalidArgumentType):
            self.api.get_results("scan-1", 5, "wrong")

    def test_get_results_invalid_range_end_type_only(self):
        with self.assertRaises(InvalidArgumentType):
            self.api.get_results("scan-1", range_end="not-an-int")

    def test_get_results_with_range_failure_raises_httpx_error(self):
        mock_response = _mock_response()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        self.mock_client.get.return_value = mock_response

        with self.assertRaises(httpx.HTTPStatusError):
            self.api.get_results("scan-1", 5, 10)

        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={"range": "5-10"}
        )

    def test_get_results_with_range_failure_return_500_httpx_error_with_safe_true(
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

        response = self.api.get_results("scan-1", 5, 10, safe=True)

        self.mock_client.get.assert_called_once_with(
            "/scans/scan-1/results", params={"range": "5-10"}
        )
        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 500)

    def test_get_result(self):
        mock_resp = _mock_response()
        self.mock_client.get.return_value = mock_resp

        self.api.get_result("scan-1", 99)
        self.mock_client.get.assert_called_once_with("/scans/scan-1/results/99")

    def test_get_result_failure_raises_httpx_error(self):
        mock_response = _mock_response()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        self.mock_client.get.return_value = mock_response

        with self.assertRaises(httpx.HTTPStatusError):
            self.api.get_result("scan-1", 99)

        self.mock_client.get.assert_called_once_with("/scans/scan-1/results/99")

    def test_get_result_failure_return_500_httpx_error_with_safe_true(self):
        mock_response = _mock_response()
        mock_http_error = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        mock_response.raise_for_status.side_effect = mock_http_error
        self.mock_client.get.return_value = mock_response

        response = self.api.get_result("scan-1", 99, safe=True)

        self.mock_client.get.assert_called_once_with("/scans/scan-1/results/99")
        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 500)

    def test_get_status(self):
        mock_resp = _mock_response()
        self.mock_client.get.return_value = mock_resp

        self.api.get_status("scan-1")
        self.mock_client.get.assert_called_once_with("/scans/scan-1/status")

    def test_get_status_failure_raises_httpx_error(self):
        mock_response = _mock_response()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        self.mock_client.get.return_value = mock_response

        with self.assertRaises(httpx.HTTPStatusError):
            self.api.get_status("scan-1")

        self.mock_client.get.assert_called_once_with("/scans/scan-1/status")

    def test_get_status_failure_return_500_httpx_error_with_safe_true(self):
        mock_response = _mock_response()
        mock_http_error = httpx.HTTPStatusError(
            "Server failed",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )
        mock_response.raise_for_status.side_effect = mock_http_error
        self.mock_client.get.return_value = mock_response

        response = self.api.get_status("scan-1", safe=True)

        self.mock_client.get.assert_called_once_with("/scans/scan-1/status")
        self.assertEqual(response, mock_http_error.response)
        self.assertEqual(response.status_code, 500)

    def test_run_action_success(self):
        mock_resp = _mock_response(status_code=202)
        self.mock_client.post.return_value = mock_resp

        status = self.api.run_action("scan-1", ScanAction.START)
        self.assertEqual(status, 202)

    def test_run_action_failure_raise_httpx_error(self):
        self.mock_client.post.side_effect = httpx.HTTPStatusError(
            "failed", request=MagicMock(), response=MagicMock(status_code=500)
        )
        with self.assertRaises(httpx.HTTPStatusError):
            self.api.run_action("scan-1", ScanAction.STOP)

    def test_run_action_failure_returns_500_with_safe_true(self):
        self.mock_client.post.side_effect = httpx.HTTPStatusError(
            "failed", request=MagicMock(), response=MagicMock(status_code=500)
        )

        status = self.api.run_action("scan-1", ScanAction.STOP, safe=True)
        self.assertEqual(status, 500)

    def test_start_scan(self):
        self.api.run_action = MagicMock(return_value=200)
        result = self.api.start("scan-abc")
        self.api.run_action.assert_called_once_with(
            "scan-abc", ScanAction.START, False
        )
        self.assertEqual(result, 200)

    def test_start_scan_failure_raises_httpx_error(self):
        self.api.run_action = MagicMock(
            side_effect=httpx.HTTPStatusError(
                "Scan start failed",
                request=MagicMock(),
                response=MagicMock(status_code=500),
            )
        )

        with self.assertRaises(httpx.HTTPStatusError):
            self.api.start("scan-abc")

    def test_start_scan_failure_returns_500_with_safe_true(self):
        self.api.run_action = MagicMock(return_value=500)
        result = self.api.start("scan-abc", safe=True)
        self.assertEqual(result, 500)

    def test_stop_scan(self):
        self.api.run_action = MagicMock(return_value=200)
        result = self.api.stop("scan-abc")
        self.api.run_action.assert_called_once_with(
            "scan-abc", ScanAction.STOP, False
        )
        self.assertEqual(result, 200)

    def test_stop_scan_failure_raises_httpx_error(self):
        self.api.run_action = MagicMock(
            side_effect=httpx.HTTPStatusError(
                "Scan stop failed",
                request=MagicMock(),
                response=MagicMock(status_code=500),
            )
        )

        with self.assertRaises(httpx.HTTPStatusError):
            self.api.stop("scan-abc")

    def test_stop_scan_failure_returns_500_with_safe_true(self):
        self.api.run_action = MagicMock(return_value=500)
        result = self.api.stop("scan-abc", safe=True)
        self.assertEqual(result, 500)
