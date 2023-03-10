# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from enum import Enum
from typing import Any, Optional

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class ScannerType(Enum):
    """Enum for scanner type"""

    OSP_SCANNER_TYPE = "1"
    OPENVAS_SCANNER_TYPE = "2"
    CVE_SCANNER_TYPE = "3"
    GMP_SCANNER_TYPE = "4"  # formerly slave scanner
    GREENBONE_SENSOR_SCANNER_TYPE = "5"

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

        if scanner_type == cls.OSP_SCANNER_TYPE.value or scanner_type == "osp":
            return cls.OSP_SCANNER_TYPE

        if (
            scanner_type == cls.OPENVAS_SCANNER_TYPE.value
            or scanner_type == "openvas"
        ):
            return cls.OPENVAS_SCANNER_TYPE

        if scanner_type == cls.CVE_SCANNER_TYPE.value or scanner_type == "cve":
            return cls.CVE_SCANNER_TYPE

        if scanner_type == cls.GMP_SCANNER_TYPE.value or scanner_type == "gmp":
            return cls.GMP_SCANNER_TYPE

        if (
            scanner_type == cls.GREENBONE_SENSOR_SCANNER_TYPE.value
            or scanner_type == "greenbone"
        ):
            return cls.GREENBONE_SENSOR_SCANNER_TYPE

        raise InvalidArgument(
            argument="scanner_type", function=cls.from_string.__name__
        )


class ScannersMixin:
    def clone_scanner(self, scanner_id: str) -> Any:
        """Clone an existing scanner

        Arguments:
            scanner_id: UUID of an existing scanner to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.clone_scanner.__name__, argument="scanner_id"
            )

        cmd = XmlCommand("create_scanner")
        cmd.add_element("copy", scanner_id)
        return self._send_xml_command(cmd)

    def create_scanner(
        self,
        name: str,
        host: str,
        port: int,
        scanner_type: ScannerType,
        credential_id: str,
        *,
        ca_pub: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Create a new scanner

        Arguments:
            name: Name of the scanner
            host: The host of the scanner
            port: The port of the scanner
            scanner_type: Type of the scanner.
            credential_id: UUID of client certificate credential for the
                scanner
            ca_pub: Certificate of CA to verify scanner certificate
            comment: Comment for the scanner
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument="name"
            )

        if not host:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument="host"
            )

        if not port:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument="port"
            )

        if not scanner_type:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument="scanner_type"
            )

        if not credential_id:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument="credential_id"
            )

        if not isinstance(scanner_type, ScannerType):
            raise InvalidArgumentType(
                function=self.create_scanner.__name__,
                argument="scanner_type",
                arg_type=ScannerType.__name__,
            )

        cmd = XmlCommand("create_scanner")
        cmd.add_element("name", name)
        cmd.add_element("host", host)
        cmd.add_element("port", str(port))
        cmd.add_element("type", scanner_type.value)

        if ca_pub:
            cmd.add_element("ca_pub", ca_pub)

        cmd.add_element("credential", attrs={"id": str(credential_id)})

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def delete_scanner(
        self, scanner_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing scanner

        Arguments:
            scanner_id: UUID of the scanner to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.delete_scanner.__name__, argument="scanner_id"
            )

        cmd = XmlCommand("delete_scanner")
        cmd.set_attribute("scanner_id", scanner_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_scanners(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of scanners

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scanners instead
            details:  Whether to include extra details like tasks using this
                scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_scanners")

        add_filter(cmd, filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return self._send_xml_command(cmd)

    def get_scanner(self, scanner_id: str) -> Any:
        """Request a single scanner

        Arguments:
            scanner_id: UUID of an existing scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_scanners")

        if not scanner_id:
            raise RequiredArgument(
                function=self.get_scanner.__name__, argument="scanner_id"
            )

        cmd.set_attribute("scanner_id", scanner_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def modify_scanner(
        self,
        scanner_id: str,
        *,
        scanner_type: Optional[ScannerType] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        ca_pub: Optional[str] = None,
        credential_id: Optional[str] = None,
    ) -> Any:
        """Modifies an existing scanner.

        Arguments:
            scanner_id: UUID of scanner to modify.
            scanner_type: New type of the Scanner.
            host: Host of the scanner.
            port: Port of the scanner.
            comment: Comment on scanner.
            name: Name of scanner.
            ca_pub: Certificate of CA to verify scanner's certificate.
            credential_id: UUID of the client certificate credential for the
                Scanner.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.modify_scanner.__name__,
                argument="scanner_id argument",
            )

        cmd = XmlCommand("modify_scanner")
        cmd.set_attribute("scanner_id", scanner_id)

        if scanner_type is not None:
            if not isinstance(scanner_type, ScannerType):
                raise InvalidArgumentType(
                    function=self.modify_scanner.__name__,
                    argument="scanner_type",
                    arg_type=ScannerType.__name__,
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

        return self._send_xml_command(cmd)

    def verify_scanner(self, scanner_id: str) -> Any:
        """Verify an existing scanner

        Verifies if it is possible to connect to an existing scanner. It is
        *not* verified if the scanner works as expected by the user.

        Arguments:
            scanner_id: UUID of the scanner to be verified

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.verify_scanner.__name__, argument="scanner_id"
            )

        cmd = XmlCommand("verify_scanner")
        cmd.set_attribute("scanner_id", scanner_id)

        return self._send_xml_command(cmd)
