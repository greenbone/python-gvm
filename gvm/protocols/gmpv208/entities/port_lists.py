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


class PortRangeType(Enum):
    """Enum for port range type"""

    TCP = "TCP"
    UDP = "UDP"

    @classmethod
    def from_string(
        cls,
        port_range_type: Optional[str],
    ) -> Optional["PortRangeType"]:
        """Convert a port range type string to an actual
        PortRangeType instance

        Arguments:
            port_range_type: Port range type string to
            convert to a PortRangeType
        """
        if not port_range_type:
            return None

        try:
            return cls[port_range_type.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="port_range_type",
                function=cls.from_string.__name__,
            ) from None


class PortListMixin:
    def clone_port_list(self, port_list_id: str) -> Any:
        """Clone an existing port list

        Arguments:
            port_list_id: UUID of an existing port list to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument(
                function=self.clone_port_list.__name__, argument="port_list_id"
            )

        cmd = XmlCommand("create_port_list")
        cmd.add_element("copy", port_list_id)
        return self._send_xml_command(cmd)

    def create_port_list(
        self, name: str, port_range: str, *, comment: Optional[str] = None
    ) -> Any:
        """Create a new port list

        Arguments:
            name: Name of the new port list
            port_range: Port list ranges e.g. `"T: 1-1234"` for tcp port
                1 - 1234
            comment: Comment for the port list

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_port_list.__name__, argument="name"
            )

        if not port_range:
            raise RequiredArgument(
                function=self.create_port_list.__name__, argument="port_range"
            )

        cmd = XmlCommand("create_port_list")
        cmd.add_element("name", name)
        cmd.add_element("port_range", port_range)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def create_port_range(
        self,
        port_list_id: str,
        start: int,
        end: int,
        port_range_type: PortRangeType,
        *,
        comment: Optional[str] = None,
    ) -> Any:
        """Create new port range

        Arguments:
            port_list_id: UUID of the port list to which to add the range
            start: The first port in the range
            end: The last port in the range
            port_range_type: The type of the ports: TCP, UDP, ...
            comment: Comment for the port range

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument(
                function=self.create_port_range.__name__,
                argument="port_list_id",
            )

        if not port_range_type:
            raise RequiredArgument(
                function=self.create_port_range.__name__,
                argument="port_range_type",
            )

        if not start:
            raise RequiredArgument(
                function=self.create_port_range.__name__, argument="start"
            )

        if not end:
            raise RequiredArgument(
                function=self.create_port_range.__name__, argument="end"
            )

        if not isinstance(port_range_type, PortRangeType):
            raise InvalidArgumentType(
                function=self.create_port_range.__name__,
                argument="port_range_type",
                arg_type=PortRangeType.__name__,
            )

        cmd = XmlCommand("create_port_range")
        cmd.add_element("port_list", attrs={"id": port_list_id})
        cmd.add_element("start", str(start))
        cmd.add_element("end", str(end))
        cmd.add_element("type", port_range_type.value)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def delete_port_list(
        self, port_list_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing port list

        Arguments:
            port_list_id: UUID of the port list to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not port_list_id:
            raise RequiredArgument(
                function=self.delete_port_list.__name__, argument="port_list_id"
            )

        cmd = XmlCommand("delete_port_list")
        cmd.set_attribute("port_list_id", port_list_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_port_range(self, port_range_id: str) -> Any:
        """Deletes an existing port range

        Arguments:
            port_range_id: UUID of the port range to be deleted.
        """
        if not port_range_id:
            raise RequiredArgument(
                function=self.delete_port_range.__name__,
                argument="port_range_id",
            )

        cmd = XmlCommand("delete_port_range")
        cmd.set_attribute("port_range_id", port_range_id)

        return self._send_xml_command(cmd)

    def get_port_lists(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        details: Optional[bool] = None,
        targets: Optional[bool] = None,
        trash: Optional[bool] = None,
    ) -> Any:
        """Request a list of port lists

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include full port list details
            targets: Whether to include targets using this port list
            trash: Whether to get port lists in the trashcan instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_port_lists")

        add_filter(cmd, filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if targets is not None:
            cmd.set_attribute("targets", to_bool(targets))

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_port_list(self, port_list_id: str):
        """Request a single port list

        Arguments:
            port_list_id: UUID of an existing port list

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_port_lists")

        if not port_list_id:
            raise RequiredArgument(
                function=self.get_port_list.__name__, argument="port_list_id"
            )

        cmd.set_attribute("port_list_id", port_list_id)

        # for single entity always request all details

        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def modify_port_list(
        self,
        port_list_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Any:
        """Modifies an existing port list.

        Arguments:
            port_list_id: UUID of port list to modify.
            name: Name of port list.
            comment: Comment on port list.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument(
                function=self.modify_port_list.__name__, argument="port_list_id"
            )
        cmd = XmlCommand("modify_port_list")
        cmd.set_attribute("port_list_id", port_list_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        return self._send_xml_command(cmd)
