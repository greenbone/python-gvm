#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later

"""
Greenbone Management Protocol (GMP) version 22.7
"""

from typing import Optional, Union

from .._protocol import T
from ._gmp226 import GMPv226
from .requests.v227 import (
    EntityID,
    Scanners,
    ScannerType,
)


class GMPv227(GMPv226[T]):
    """
    A class implementing the Greenbone Management Protocol (GMP) version 22.7

    Example:

        .. code-block:: python

            from gvm.protocols.gmp import GMPv227 as GMP

            with GMP(connection) as gmp:
                resp = gmp.get_tasks()
    """

    @staticmethod
    def get_protocol_version() -> tuple[int, int]:
        return (22, 7)

    def create_scanner(  # type:ignore[override]
        self,
        name: str,
        host: str,
        port: Union[str, int],
        scanner_type: ScannerType,
        credential_id: str,
        *,
        ca_pub: Optional[str] = None,
        comment: Optional[str] = None,
        relay_host: Optional[str] = None,
        relay_port: Optional[Union[str, int]] = None,
    ) -> T:
        """Create a new scanner

        Args:
            name: Name of the new scanner
            host: Hostname or IP address of the scanner
            port: Port of the scanner
            scanner_type: Type of the scanner
            credential_id: UUID of client certificate credential for the
                scanner
            ca_pub: Certificate of CA to verify scanner certificate
            comment: Comment for the scanner
            relay_host: Hostname or IP address of the scanner relay
            relay_port: Port of the scanner relay
        """
        return self._send_request_and_transform_response(
            Scanners.create_scanner(
                name,
                host,
                port,
                scanner_type,
                credential_id,
                ca_pub=ca_pub,
                comment=comment,
                relay_host=relay_host,
                relay_port=relay_port,
            )
        )

    def modify_scanner(  # type:ignore[override]
        self,
        scanner_id: EntityID,
        *,
        name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        scanner_type: Optional[ScannerType] = None,
        credential_id: Optional[EntityID] = None,
        ca_pub: Optional[str] = None,
        comment: Optional[str] = None,
        relay_host: Optional[str] = None,
        relay_port: Optional[Union[str, int]] = None,
    ) -> T:
        """Modify an existing scanner

        Args:
            scanner_id: UUID of the scanner to modify
            name: New name of the scanner
            host: New hostname or IP address of the scanner
            port: New port of the scanner
            scanner_type: New type of the scanner
            credential_id: New UUID of client certificate credential for the
                scanner
            ca_pub: New certificate of CA to verify scanner certificate
            comment: New comment for the scanner
            relay_host: Hostname or IP address of the scanner relay
            relay_port: Port of the scanner relay
        """
        return self._send_request_and_transform_response(
            Scanners.modify_scanner(
                scanner_id,
                name=name,
                host=host,
                port=port,
                scanner_type=scanner_type,
                credential_id=credential_id,
                ca_pub=ca_pub,
                comment=comment,
                relay_host=relay_host,
                relay_port=relay_port,
            )
        )

    def get_scanners(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> T:
        """Request a list of scanners

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scanners instead
            details: Whether to include extra details like tasks using this
                scanner
        """
        return self._send_request_and_transform_response(
            Scanners.get_scanners(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
                details=details,
            )
        )

    def get_scanner(self, scanner_id: EntityID) -> T:
        """Request a single scanner

        Args:
            scanner_id: UUID of an existing scanner
        """
        return self._send_request_and_transform_response(
            Scanners.get_scanner(scanner_id)
        )

    def verify_scanner(self, scanner_id: EntityID) -> T:
        """Verify an existing scanner

        Args:
            scanner_id: UUID of an existing scanner
        """
        return self._send_request_and_transform_response(
            Scanners.verify_scanner(scanner_id)
        )

    def clone_scanner(self, scanner_id: EntityID) -> T:
        """Clone an existing scanner

        Args:
            scanner_id: UUID of an existing scanner
        """
        return self._send_request_and_transform_response(
            Scanners.clone_scanner(scanner_id)
        )

    def delete_scanner(
        self, scanner_id: EntityID, ultimate: Optional[bool] = False
    ) -> T:
        """Delete an existing scanner

        Args:
            scanner_id: UUID of an existing scanner
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_request_and_transform_response(
            Scanners.delete_scanner(scanner_id, ultimate=ultimate)
        )
