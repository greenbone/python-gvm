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
from gvm.protocols.gmpv208.entities.scanners import (
    ScannersMixin as Gmp208ScannersMixin,
)
from gvm.xml import XmlCommand


class ScannerType(Enum):
    """Enum for scanner type"""

    # 1 was removed (OSP_SCANNER_TYPE).
    OPENVAS_SCANNER_TYPE = "2"
    CVE_SCANNER_TYPE = "3"
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

        if (
            scanner_type == cls.OPENVAS_SCANNER_TYPE.value
            or scanner_type == "openvas"
        ):
            return cls.OPENVAS_SCANNER_TYPE

        if scanner_type == cls.CVE_SCANNER_TYPE.value or scanner_type == "cve":
            return cls.CVE_SCANNER_TYPE

        if (
            scanner_type == cls.GREENBONE_SENSOR_SCANNER_TYPE.value
            or scanner_type == "greenbone"
        ):
            return cls.GREENBONE_SENSOR_SCANNER_TYPE

        raise InvalidArgument(
            argument="scanner_type", function=cls.from_string.__name__
        )


class ScannersMixin(Gmp208ScannersMixin):
    # Override bc. of ScannerType (?)

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
