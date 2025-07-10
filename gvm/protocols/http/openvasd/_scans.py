# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
API wrapper for interacting with the /scans endpoints of the openvasd HTTP API.
"""

import urllib.parse
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from gvm.errors import InvalidArgumentType

from ._api import OpenvasdAPI

ID = Union[str, UUID]


@dataclass
class PortRange:
    """
    Represents a range of ports.

    Attributes:
        start: The starting port number.
        end: The ending port number.
    """

    start: int
    end: int


@dataclass
class Port:
    """
    Represents a port configuration for scanning.

    Attributes:
        protocol: The protocol to use ("tcp" or "udp").
        range: A list of port ranges to scan.
    """

    protocol: str  # e.g., "tcp", "udp"
    range: list[PortRange]


@dataclass
class CredentialUP:
    """
    Represents username/password credentials for a service.

    Attributes:
        username: The login username.
        password: The login password.
        privilege_username: Optional privilege escalation username.
        privilege_password: Optional privilege escalation password.
    """

    username: str
    password: str
    privilege_username: Optional[str] = None
    privilege_password: Optional[str] = None


@dataclass
class CredentialKRB5:
    """
    Represents Kerberos credentials.

    Attributes:
        username: Kerberos username.
        password: Kerberos password.
        realm: Kerberos realm.
        kdc: Key Distribution Center hostname.
    """

    username: str
    password: str
    realm: str
    kdc: str


@dataclass
class CredentialUSK:
    """
    Represents credentials using a user/SSH key combination.

    Attributes:
        username: SSH username.
        password: Password for SSH key (if encrypted).
        private: Private key content or reference.
        privilege_username: Optional privilege escalation username.
        privilege_password: Optional privilege escalation password.
    """

    username: str
    password: str
    private: str
    privilege_username: Optional[str] = None
    privilege_password: Optional[str] = None


@dataclass
class CredentialSNMP:
    """
    Represents SNMP credentials.

    Attributes:
        username: SNMP username.
        password: SNMP authentication password.
        community: SNMP community string.
        auth_algorithm: Authentication algorithm (e.g., "md5").
        privacy_password: Privacy password for SNMPv3.
        privacy_algorithm: Privacy algorithm (e.g., "aes").
    """

    username: str
    password: str
    community: str
    auth_algorithm: str
    privacy_password: str
    privacy_algorithm: str


@dataclass
class Credential:
    """
    Represents a full credential configuration for a specific service.

    Attributes:
        service: Name of the service (e.g., "ssh", "snmp").
        port: Port number associated with the service.
        up: Optional username/password credentials.
        krb5: Optional Kerberos credentials.
        usk: Optional user/SSH key credentials.
        snmp: Optional SNMP credentials.
    """

    service: str
    port: int
    up: Optional[CredentialUP] = None
    krb5: Optional[CredentialKRB5] = None
    usk: Optional[CredentialUSK] = None
    snmp: Optional[CredentialSNMP] = None


@dataclass
class Target:
    """
    Represents the scan target configuration.

    Attributes:
        hosts: List of target IPs or hostnames.
        excluded_hosts: List of IPs or hostnames to exclude.
        ports: List of port configurations.
        credentials: List of credentials to use during scanning.
        alive_test_ports: Port ranges used to test if hosts are alive.
        alive_test_methods: Methods used to check if hosts are alive (e.g., "icmp").
        reverse_lookup_unify: Whether to unify reverse lookup results.
        reverse_lookup_only: Whether to rely solely on reverse DNS lookups.
    """

    hosts: list[str]
    excluded_hosts: list[str] = field(default_factory=list)
    ports: list[Port] = field(default_factory=list)
    credentials: list[Credential] = field(default_factory=list)
    alive_test_ports: list[Port] = field(default_factory=list)
    alive_test_methods: list[str] = field(default_factory=list)
    reverse_lookup_unify: bool = False
    reverse_lookup_only: bool = False


@dataclass
class VTParameter:
    """
    Represents a parameter for a specific vulnerability test.

    Attributes:
        id: Identifier of the VT parameter.
        value: Value to assign to the parameter.
    """

    id: int
    value: str


@dataclass
class VTSelection:
    """
    Represents a selected vulnerability test (VT) and its parameters.

    Attributes:
        oid: The OID (Object Identifier) of the VT.
        parameters: A list of parameters to customize VT behavior.
    """

    oid: str
    parameters: list[VTParameter] = field(default_factory=list)


@dataclass
class ScanPreference:
    """
    Represents a scan-level preference or configuration option.

    Attributes:
        id: Preference ID or name (e.g., "max_checks", "scan_speed").
        value: The value assigned to the preference.
    """

    id: str
    value: str


def _to_dict(obj: Any) -> Any:
    """Recursively convert dataclass instances to dictionaries."""
    if isinstance(obj, list):
        return [_to_dict(item) for item in obj]
    elif hasattr(obj, "__dataclass_fields__"):
        return {k: _to_dict(v) for k, v in asdict(obj).items() if v is not None}
    return obj


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
        target: Target,
        vt_selection: list[VTSelection],
        *,
        scan_preferences: Optional[list[ScanPreference]] = None,
    ) -> httpx.Response:
        """
        Create a new scan with the specified target configuration and VT selection.

        Args:
            target: A `Target` dataclass instance describing the scan target(s), including hosts, ports, credentials, and alive test settings.
            vt_selection: A list of `VTSelection` instances specifying which vulnerability tests (VTs) to include in the scan.
            scan_preferences: Optional list of `ScanPreference` instances to customize scan behavior (e.g., number of threads, timeout values).

        Returns:
            The full HTTP response returned by the POST /scans request.

        Raises:
            httpx.HTTPStatusError: If the server responds with an error status
                and the exception is not suppressed.

        See: POST /scans in the openvasd API documentation.
        """
        request_json = {
            "target": _to_dict(target),
            "vts": _to_dict(vt_selection),
        }
        if scan_preferences:
            request_json["scan_preferences"] = _to_dict(scan_preferences)

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

    def get_preferences(self) -> httpx.Response:
        """
        Retrieve all available scan preferences from the scanner.

        Returns:
            The full HTTP response of the GET /scans/preferences request.

        Raises:
            httpx.HTTPStatusError: If the server responds with an error status
                and the exception is not suppressed.

        See: GET /scans/preferences in the openvasd API documentation.
        """
        try:
            response = self._client.get("/scans/preferences")
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if self._suppress_exceptions:
                return e.response
            raise
