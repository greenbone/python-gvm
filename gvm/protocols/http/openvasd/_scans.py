# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
API wrapper for interacting with the /scans endpoints of the openvasd HTTP API.
"""

import urllib.parse
from enum import Enum
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from gvm.errors import InvalidArgumentType

from ._api import OpenvasdAPI

ID = Union[str, UUID]


class ScanAction(str, Enum):
    """
    Enumeration of valid scan actions supported by the openvasd API.

    This enum defines the allowed actions that can be performed on a scan.
    Using an enum helps ensure type safety and prevents invalid action strings
    from being passed to the API.

    Values:
        START: Initiates the scan execution.
        STOP: Terminates an ongoing scan.
    """

    START = "start"  # Start the scan
    STOP = "stop"  # Stop the scan


class ScansAPI(OpenvasdAPI):
    """
    Provides access to scan-related operations in the openvasd HTTP API.

    Includes methods for creating, starting, stopping, and retrieving scan details
    and results.
    """

    def create(
        self,
        target: dict[str, Any],
        vt_selection: list[dict[str, Any]],
        *,
        scanner_params: Optional[dict[str, Any]] = None,
    ) -> httpx.Response:
        """
        Create a new scan with the specified target and VT selection.

        Args:
            target: Dictionary describing the scan target (e.g., host and port).
            vt_selection: List of dictionaries specifying which VTs to run.
            scanner_params: Optional dictionary of scan preferences.

        Returns:
            The full HTTP response of the POST /scans request.

        Raises:
            httpx.HTTPStatusError: If the server responds with an error status
                and the exception is not suppressed.

        See: POST /scans in the openvasd API documentation.
        """
        request_json = {"target": target, "vts": vt_selection}
        if scanner_params:
            request_json["scan_preferences"] = scanner_params

        try:
            response = self._client.post("/scans", json=request_json)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response
            raise

    def delete(self, scan_id: ID) -> int:
        """
        Delete a scan by its ID.

        Args:
            scan_id: The scan identifier.

        Returns:
            The HTTP status code returned by the server on success,
            or the error status code returned by the server on failure.

        Raises:
            httpx.HTTPStatusError: If the server responds with an error status
                and the exception is not suppressed.

        See: DELETE /scans/{id} in the openvasd API documentation.
        """
        try:
            response = self._client.delete(
                f"/scans/{urllib.parse.quote(str(scan_id))}"
            )
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response.status_code
            raise

    def get_all(self) -> httpx.Response:
        """
        Retrieve the list of all available scans.

        Returns:
            The full HTTP response of the GET /scans request.

        Raises:
            httpx.HTTPStatusError: If the request fails and exceptions are not suppressed.

        See: GET /scans in the openvasd API documentation.
        """
        try:
            response = self._client.get("/scans")
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response
            raise

    def get(self, scan_id: ID) -> httpx.Response:
        """
        Retrieve metadata of a single scan by ID.

        Args:
            scan_id: The scan identifier.

        Returns:
            The full HTTP response of the GET /scans/{id} request.

        Raises:
            httpx.HTTPStatusError: If the request fails and exceptions are not suppressed.

        See: GET /scans/{id} in the openvasd API documentation.
        """
        try:
            response = self._client.get(
                f"/scans/{urllib.parse.quote(str(scan_id))}"
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response
            raise

    def get_results(
        self,
        scan_id: ID,
        *,
        range_start: Optional[int] = None,
        range_end: Optional[int] = None,
    ) -> httpx.Response:
        """
        Retrieve a range of results for a given scan.

        Args:
            scan_id: The scan identifier.
            range_start: Optional start index for paginated results.
            range_end: Optional end index for paginated results.

        Returns:
            The full HTTP response of the GET /scans/{id}/results request.

        Raises:
            InvalidArgumentType: If provided range values are not integers.
            httpx.HTTPStatusError: If the request fails and exceptions are not suppressed.

        See: GET /scans/{id}/results in the openvasd API documentation.
        """
        params = {}
        if range_start is not None:
            if not isinstance(range_start, int):
                raise InvalidArgumentType("range_start")
            if range_end is not None:
                if not isinstance(range_end, int):
                    raise InvalidArgumentType("range_end")
                params["range"] = f"{range_start}-{range_end}"
            else:
                params["range"] = str(range_start)
        elif range_end is not None:
            if not isinstance(range_end, int):
                raise InvalidArgumentType("range_end")
            params["range"] = f"0-{range_end}"

        try:
            response = self._client.get(
                f"/scans/{urllib.parse.quote(str(scan_id))}/results",
                params=params,
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response
            raise

    def get_result(
        self,
        scan_id: ID,
        result_id: ID,
    ) -> httpx.Response:
        """
        Retrieve a specific scan result.

        Args:
            scan_id: The scan identifier.
            result_id: The specific result ID to fetch.

        Returns:
            The full HTTP response of the GET /scans/{id}/results/{rid} request.

        Raises:
            httpx.HTTPStatusError: If the request fails and exceptions are not suppressed.

        See: GET /scans/{id}/results/{rid} in the openvasd API documentation.
        """
        try:
            response = self._client.get(
                f"/scans/{urllib.parse.quote(str(scan_id))}/results/{urllib.parse.quote(str(result_id))}"
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response
            raise

    def get_status(self, scan_id: ID) -> httpx.Response:
        """
        Retrieve the status of a scan.

        Args:
            scan_id: The scan identifier.

        Returns:
            The full HTTP response of the GET /scans/{id}/status request.

        Raises:
            httpx.HTTPStatusError: If the request fails and exceptions are not suppressed.

        See: GET /scans/{id}/status in the openvasd API documentation.
        """
        try:
            response = self._client.get(
                f"/scans/{urllib.parse.quote(str(scan_id))}/status"
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response
            raise

    def _run_action(self, scan_id: ID, action: ScanAction) -> int:
        """
        Perform a scan action (start or stop) for the given scan ID.

        Args:
            scan_id: The unique identifier of the scan.
            action: A member of the ScanAction enum (e.g., ScanAction.START or ScanAction.STOP).

        Returns:
            The HTTP status code returned by the server on success,
            or the error status code returned by the server on failure.

        Raises:
            httpx.HTTPStatusError: If the request fails and exceptions are not suppressed.

        See: POST /scans/{id} in the openvasd API documentation.
        """
        try:
            response = self._client.post(
                f"/scans/{urllib.parse.quote(str(scan_id))}",
                json={"action": str(action.value)},
            )
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response.status_code
            raise

    def start(self, scan_id: ID) -> int:
        """
        Start the scan identified by the given scan ID.

        Args:
            scan_id: The unique identifier of the scan.

        Returns:
            HTTP status code (e.g., 200) if successful, or error code (e.g., 404, 500) if the request fails,
            and safe is False.

        Raises:
            httpx.HTTPStatusError: If the request fails and exceptions are not suppressed.

        See: POST /scans/{id} with action=start in the openvasd API documentation.
        """
        return self._run_action(scan_id, ScanAction.START)

    def stop(self, scan_id: ID) -> int:
        """
        Stop the scan identified by the given scan ID.

        Args:
            scan_id: The unique identifier of the scan.

        Returns:
            HTTP status code (e.g., 200) if successful, or error code (e.g., 404, 500) if the request fails,
            and safe is False.

        Raises:
            httpx.HTTPStatusError: If the request fails and exceptions are not suppressed.

        See: POST /scans/{id} with action=stop in the openvasd API documentation.
        """
        return self._run_action(scan_id, ScanAction.STOP)
