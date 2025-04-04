# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
openvasd HTTP API version 1
"""

import urllib.parse
from typing import Any, Optional

from gvm.errors import InvalidArgumentType
from gvm.http.core._api import GvmHttpApi
from gvm.http.core.connector import HttpApiConnector
from gvm.http.core.response import HttpResponse


class OpenvasdHttpApiV1(GvmHttpApi):
    """
    Class for sending requests to a version 1 openvasd API.
    """

    def __init__(
        self,
        connector: HttpApiConnector,
        *,
        api_key: Optional[str] = None,
    ):
        """
        Create a new openvasd HTTP API instance.

        Args:
            connector: The connector handling the HTTP(S) connection
            api_key: Optional API key for authentication
        """
        super().__init__(connector, api_key=api_key)
        if api_key:
            connector.update_headers({"X-API-KEY": api_key})

    def get_health_alive(
        self, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Gets the "alive" health status of the scanner.

        Args:
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See GET /health/alive in the openvasd API documentation.
        """
        return self._connector.get(
            "/health/alive", raise_for_status=raise_for_status
        )

    def get_health_ready(
        self, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Gets the "ready" health status of the scanner.

        Args:
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See GET /health/ready in the openvasd API documentation.
        """
        return self._connector.get(
            "/health/ready", raise_for_status=raise_for_status
        )

    def get_health_started(
        self, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Gets the "started" health status of the scanner.

        Args:
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See GET /health/started in the openvasd API documentation.
        """
        return self._connector.get(
            "/health/started", raise_for_status=raise_for_status
        )

    def get_notus_os_list(
        self, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Gets the list of operating systems available in Notus.

        Args:
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See GET /notus in the openvasd API documentation.
        """
        return self._connector.get("/notus", raise_for_status=raise_for_status)

    def run_notus_scan(
        self,
        os: str,
        package_list: list[str],
        *,
        raise_for_status: bool = False,
    ) -> HttpResponse:
        """
        Gets the Notus results for a given operating system and list of packages.

        Args:
            os: Name of the operating system as returned in the list returned by
             get_notus_os_products.
            package_list: List of package names to check.
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See POST /notus/{os} in the openvasd API documentation.
        """
        quoted_os = urllib.parse.quote(os)
        return self._connector.post_json(
            f"/notus/{quoted_os}",
            package_list,
            raise_for_status=raise_for_status,
        )

    def get_scan_preferences(
        self, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Gets the list of available scan preferences.

        Args:
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See POST /scans/preferences in the openvasd API documentation.
        """
        return self._connector.get(
            "/scans/preferences", raise_for_status=raise_for_status
        )

    def create_scan(
        self,
        target: dict[str, Any],
        vt_selection: dict[str, Any],
        scanner_params: Optional[dict[str, Any]] = None,
        *,
        raise_for_status: bool = False,
    ) -> HttpResponse:
        """
        Creates a new scan without starting it.

        See POST /scans in the openvasd API documentation for the expected format of the parameters.

        Args:
            target: The target definition for the scan.
            vt_selection: The VT selection for the scan, including VT preferences.
            scanner_params: The optional scanner parameters.
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See POST /scans in the openvasd API documentation.
        """
        request_json: dict = {
            "target": target,
            "vts": vt_selection,
        }
        if scanner_params:
            request_json["scan_preferences"] = scanner_params
        return self._connector.post_json(
            "/scans", request_json, raise_for_status=raise_for_status
        )

    def delete_scan(
        self, scan_id: str, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Deletes a scan with the given id.

        Args:
            scan_id: The id of the scan to perform the action on.
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See DELETE /scans/{id} in the openvasd API documentation.
        """
        quoted_scan_id = urllib.parse.quote(scan_id)
        return self._connector.delete(
            f"/scans/{quoted_scan_id}", raise_for_status=raise_for_status
        )

    def get_scans(self, *, raise_for_status: bool = False) -> HttpResponse:
        """
        Gets the list of available scans.

        Args:
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See GET /scans in the openvasd API documentation.
        """
        return self._connector.get("/scans", raise_for_status=raise_for_status)

    def get_scan(
        self, scan_id: str, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Gets a scan with the given id.

        Args:
            scan_id: The id of the scan to get.
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See GET /scans/{id} in the openvasd API documentation.
        """
        quoted_scan_id = urllib.parse.quote(scan_id)
        return self._connector.get(
            f"/scans/{quoted_scan_id}", raise_for_status=raise_for_status
        )

    def get_scan_results(
        self,
        scan_id: str,
        range_start: Optional[int] = None,
        range_end: Optional[int] = None,
        *,
        raise_for_status: bool = False,
    ) -> HttpResponse:
        """
        Gets results of a scan with the given id.

        Args:
            scan_id: The id of the scan to get the results of.
            range_start: Optional index of the first result to get.
            range_end: Optional index of the last result to get.
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See GET /scans/{id}/results in the openvasd API documentation.
        """
        quoted_scan_id = urllib.parse.quote(scan_id)
        params = {}
        if range_start is not None:
            if not isinstance(range_start, int):
                raise InvalidArgumentType(
                    argument="range_start",
                    function=self.get_scan_results.__name__,
                )

            if range_end is not None:
                if not isinstance(range_end, int):
                    raise InvalidArgumentType(
                        argument="range_end",
                        function=self.get_scan_results.__name__,
                    )
                params["range"] = f"{range_start}-{range_end}"
            else:
                params["range"] = str(range_start)
        else:
            if range_end is not None:
                if not isinstance(range_end, int):
                    raise InvalidArgumentType(
                        argument="range_end",
                        function=self.get_scan_results.__name__,
                    )
                params["range"] = f"0-{range_end}"

        return self._connector.get(
            f"/scans/{quoted_scan_id}/results",
            params=params,
            raise_for_status=raise_for_status,
        )

    def get_scan_result(
        self,
        scan_id: str,
        result_id: str | int,
        *,
        raise_for_status: bool = False,
    ) -> HttpResponse:
        """
        Gets a single result of a scan with the given id.

        Args:
            scan_id: The id of the scan to get the results of.
            result_id: The id of the result to get.
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See GET /scans/{id}/{rid} in the openvasd API documentation.
        """
        quoted_scan_id = urllib.parse.quote(scan_id)
        quoted_result_id = urllib.parse.quote(str(result_id))

        return self._connector.get(
            f"/scans/{quoted_scan_id}/results/{quoted_result_id}",
            raise_for_status=raise_for_status,
        )

    def get_scan_status(
        self, scan_id: str, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Gets a scan with the given id.

        Args:
            scan_id: The id of the scan to get the status of.
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See GET /scans/{id}/{rid} in the openvasd API documentation.
        """
        quoted_scan_id = urllib.parse.quote(scan_id)
        return self._connector.get(
            f"/scans/{quoted_scan_id}/status", raise_for_status=raise_for_status
        )

    def run_scan_action(
        self, scan_id: str, scan_action: str, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Performs an action like starting or stopping on a scan with the given id.

        Args:
            scan_id: The id of the scan to perform the action on.
            scan_action: The action to perform.
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See POST /scans/{id} in the openvasd API documentation.
        """
        quoted_scan_id = urllib.parse.quote(scan_id)
        action_json = {"action": scan_action}
        return self._connector.post_json(
            f"/scans/{quoted_scan_id}",
            action_json,
            raise_for_status=raise_for_status,
        )

    def start_scan(
        self, scan_id: str, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Starts a scan with the given id.

        Args:
            scan_id: The id of the scan to perform the action on.
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See POST /scans/{id} in the openvasd API documentation.
        """
        return self.run_scan_action(
            scan_id, "start", raise_for_status=raise_for_status
        )

    def stop_scan(
        self, scan_id: str, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Stops a scan with the given id.

        Args:
            scan_id: The id of the scan to perform the action on.
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See POST /scans/{id} in the openvasd API documentation.
        """
        return self.run_scan_action(
            scan_id, "stop", raise_for_status=raise_for_status
        )

    def get_vts(self, *, raise_for_status: bool = False) -> HttpResponse:
        """
        Gets a list of available vulnerability tests (VTs) on the scanner.

        Args:
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See GET /vts in the openvasd API documentation.
        """
        return self._connector.get("/vts", raise_for_status=raise_for_status)

    def get_vt(
        self, oid: str, *, raise_for_status: bool = False
    ) -> HttpResponse:
        """
        Gets the details of a vulnerability test (VT).

        Args:
            oid: OID of the VT to get.
            raise_for_status: Whether to raise an error if scanner responded with a
             non-success HTTP status code.

        Return:
            The HTTP response. See DELETE /scans/{id} in the openvasd API documentation.
        """
        quoted_oid = urllib.parse.quote(oid)
        return self._connector.get(
            f"/vts/{quoted_oid}", raise_for_status=raise_for_status
        )
