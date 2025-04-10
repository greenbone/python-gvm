# SPDX-FileCopyrightText: 2021-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm._enum import Enum
from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class ScannerType(Enum):
    """Enum for scanner type"""

    # 1 was removed (OSP_SCANNER_TYPE).
    OPENVAS_SCANNER_TYPE = "2"
    CVE_SCANNER_TYPE = "3"
    GREENBONE_SENSOR_SCANNER_TYPE = "5"
    OPENVASD_SCANNER_TYPE = "6"

    @classmethod
    def from_string(
        cls,
        scanner_type: Optional[str],
    ) -> Optional["ScannerType"]:
        """Convert a scanner type string to an actual ScannerType instance

        Arguments:
            scanner_type: Scanner type string to convert to a ScannerType
        """
        if not scanner_type:
            return None

        scanner_type = scanner_type.lower()

        if (
            scanner_type == cls.OPENVAS_SCANNER_TYPE.value
            or scanner_type == "openvas"
            or scanner_type == "openvas_scanner_type"
        ):
            return cls.OPENVAS_SCANNER_TYPE

        if (
            scanner_type == cls.CVE_SCANNER_TYPE.value
            or scanner_type == "cve"
            or scanner_type == "cve_scanner_type"
        ):
            return cls.CVE_SCANNER_TYPE

        if (
            scanner_type == cls.GREENBONE_SENSOR_SCANNER_TYPE.value
            or scanner_type == "greenbone"
            or scanner_type == "greenbone_sensor_scanner_type"
        ):
            return cls.GREENBONE_SENSOR_SCANNER_TYPE

        if (
            scanner_type == cls.OPENVASD_SCANNER_TYPE.value
            or scanner_type == "openvasd"
            or scanner_type == "openvasd_scanner_type"
        ):
            return cls.OPENVASD_SCANNER_TYPE

        raise InvalidArgument(
            argument="scanner_type", function=cls.from_string.__name__
        )


class Scanners:
    @classmethod
    def create_scanner(
        cls,
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
    ) -> Request:
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
        if not name:
            raise RequiredArgument(
                function=cls.create_scanner.__name__, argument="name"
            )

        if not host:
            raise RequiredArgument(
                function=cls.create_scanner.__name__, argument="host"
            )

        if not port:
            raise RequiredArgument(
                function=cls.create_scanner.__name__, argument="port"
            )

        if not scanner_type:
            raise RequiredArgument(
                function=cls.create_scanner.__name__, argument="scanner_type"
            )

        if not credential_id:
            raise RequiredArgument(
                function=cls.create_scanner.__name__, argument="credential_id"
            )

        cmd = XmlCommand("create_scanner")
        cmd.add_element("name", name)
        cmd.add_element("host", host)
        cmd.add_element("port", str(port))

        if not isinstance(scanner_type, ScannerType):
            scanner_type = ScannerType(scanner_type)

        cmd.add_element("type", scanner_type.value)

        cmd.add_element("credential", attrs={"id": str(credential_id)})

        if ca_pub:
            cmd.add_element("ca_pub", ca_pub)

        if comment:
            cmd.add_element("comment", comment)

        if relay_host:
            cmd.add_element("relay_host", relay_host)

        if relay_port:
            cmd.add_element("relay_port", str(relay_port))

        return cmd

    @classmethod
    def modify_scanner(
        cls,
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
    ) -> Request:
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
        if not scanner_id:
            raise RequiredArgument(
                function=cls.modify_scanner.__name__, argument="scanner_id"
            )

        cmd = XmlCommand("modify_scanner")
        cmd.set_attribute("scanner_id", str(scanner_id))

        if scanner_type is not None:
            if not isinstance(scanner_type, ScannerType):
                scanner_type = ScannerType(scanner_type)
            if not scanner_type:
                raise InvalidArgument(
                    argument="scanner_type",
                    function=cls.modify_scanner.__name__,
                )
            cmd.add_element("type", scanner_type.value)

        if host:
            cmd.add_element("host", host)

        if port:
            cmd.add_element("port", str(port))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if ca_pub:
            cmd.add_element("ca_pub", ca_pub)

        if credential_id:
            cmd.add_element("credential", attrs={"id": str(credential_id)})

        if relay_host:
            cmd.add_element("relay_host", relay_host)

        if relay_port:
            cmd.add_element("relay_port", str(relay_port))

        return cmd

    @staticmethod
    def get_scanners(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of scanners

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scanners instead
            details: Whether to include extra details like tasks using this
                scanner
        """
        cmd = XmlCommand("get_scanners")
        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return cmd

    @classmethod
    def get_scanner(cls, scanner_id: EntityID) -> Request:
        """Request a single scanner

        Args:
            scanner_id: UUID of an existing scanner
        """
        if not scanner_id:
            raise RequiredArgument(
                function=cls.get_scanner.__name__, argument="scanner_id"
            )

        cmd = XmlCommand("get_scanners")
        cmd.set_attribute("scanner_id", str(scanner_id))

        # for single entity always request all details
        cmd.set_attribute("details", "1")

        return cmd

    @classmethod
    def verify_scanner(cls, scanner_id: EntityID) -> Request:
        """Verify an existing scanner

        Args:
            scanner_id: UUID of an existing scanner
        """
        if not scanner_id:
            raise RequiredArgument(
                function=cls.verify_scanner.__name__, argument="scanner_id"
            )

        cmd = XmlCommand("verify_scanner")
        cmd.set_attribute("scanner_id", str(scanner_id))

        return cmd

    @classmethod
    def clone_scanner(cls, scanner_id: EntityID) -> Request:
        """Clone an existing scanner

        Args:
            scanner_id: UUID of an existing scanner
        """
        if not scanner_id:
            raise RequiredArgument(
                function=cls.clone_scanner.__name__, argument="scanner_id"
            )

        cmd = XmlCommand("create_scanner")
        cmd.add_element("copy", str(scanner_id))
        return cmd

    @classmethod
    def delete_scanner(
        cls, scanner_id: EntityID, ultimate: Optional[bool] = False
    ) -> Request:
        """Delete an existing scanner

        Args:
            scanner_id: UUID of an existing scanner
        """
        if not scanner_id:
            raise RequiredArgument(
                function=cls.delete_scanner.__name__, argument="scanner_id"
            )

        cmd = XmlCommand("delete_scanner")
        cmd.set_attribute("scanner_id", str(scanner_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd
