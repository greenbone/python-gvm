# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
openvasd HTTP API version 1

High-level API interface for interacting with openvasd HTTP services via
logical modules (health, metadata, scans, etc.).
"""

from typing import Optional, Tuple, Union

from ._client import StrOrPathLike, create_openvasd_http_client
from ._health import HealthAPI
from ._metadata import MetadataAPI
from ._notus import NotusAPI
from ._scans import ScansAPI
from ._vts import VtsAPI


class OpenvasdHttpAPIv1:
    """
    High-level interface for accessing openvasd HTTP API v1 endpoints.

    This class encapsulates modular sub-APIs (health, metadata, notus, scans, vts)
    and wires them to a shared `httpx.Client` configured for secure access.

    Each sub-API provides methods for interacting with a specific openvasd domain.
    """

    def __init__(
        self,
        host_name: str,
        port: int = 3000,
        *,
        api_key: Optional[str] = None,
        server_ca_path: Optional[StrOrPathLike] = None,
        client_cert_paths: Optional[
            Union[StrOrPathLike, Tuple[StrOrPathLike, StrOrPathLike]]
        ] = None,
        suppress_exceptions: bool = False,
    ):
        """
        Initialize the OpenvasdHttpApiV1 entry point.

        Args:
            host_name: Hostname or IP of the openvasd server (e.g., "localhost").
            port: Port of the openvasd service (default: 3000).
            api_key: Optional API key to be used for authentication.
            server_ca_path: Path to the server CA certificate (for HTTPS/mTLS).
            client_cert_paths: Path to client certificate or (cert, key) tuple for mTLS.
            suppress_exceptions: If True, suppress exceptions and return structured error
                responses. Default is False, which means exceptions will be raised.
        """
        self._client = create_openvasd_http_client(
            host_name=host_name,
            port=port,
            api_key=api_key,
            server_ca_path=server_ca_path,
            client_cert_paths=client_cert_paths,
        )

        # Sub-API modules
        self.__health = HealthAPI(
            self._client, suppress_exceptions=suppress_exceptions
        )
        self.__metadata = MetadataAPI(
            self._client, suppress_exceptions=suppress_exceptions
        )
        self.__notus = NotusAPI(
            self._client, suppress_exceptions=suppress_exceptions
        )
        self.__scans = ScansAPI(
            self._client, suppress_exceptions=suppress_exceptions
        )
        self.__vts = VtsAPI(
            self._client, suppress_exceptions=suppress_exceptions
        )

    @property
    def health(self) -> HealthAPI:
        """
        Access the health API module.

        Provides methods to check the health status of the openvasd service.
        """
        return self.__health

    @property
    def metadata(self) -> MetadataAPI:
        """
        Access the metadata API module.

        Provides methods to retrieve metadata about the openvasd service,
        including version and feed information.
        """
        return self.__metadata

    @property
    def notus(self) -> NotusAPI:
        """
        Access the Notus API module.

        Provides methods to interact with the Notus service for package-based
        vulnerability scanning.
        """
        return self.__notus

    @property
    def scans(self) -> ScansAPI:
        """
        Access the scans API module.

        Provides methods to manage and interact with vulnerability scans,
        including starting, stopping, and retrieving scan results.
        """
        return self.__scans

    @property
    def vts(self) -> VtsAPI:
        """
        Access the VTS API module.

        Provides methods to manage and interact with Vulnerability Tests
        (VTs) for vulnerability assessment.
        """
        return self.__vts
