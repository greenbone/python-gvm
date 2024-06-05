# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm._enum import Enum
from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class PortRangeType(Enum):
    """Enum for port range type"""

    TCP = "TCP"
    UDP = "UDP"


class PortLists:
    @classmethod
    def clone_port_list(cls, port_list_id: EntityID) -> Request:
        """Clone an existing port list

        Args:
            port_list_id: UUID of an existing port list to clone from
        """
        if not port_list_id:
            raise RequiredArgument(
                function=cls.clone_port_list.__name__, argument="port_list_id"
            )

        cmd = XmlCommand("create_port_list")
        cmd.add_element("copy", str(port_list_id))
        return cmd

    @classmethod
    def create_port_list(
        cls, name: str, port_range: str, *, comment: Optional[str] = None
    ) -> Request:
        """Create a new port list

        Args:
            name: Name of the new port list
            port_range: Port list ranges e.g. `"T: 1-1234"` for tcp port
                1 - 1234
            comment: Comment for the port list
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_port_list.__name__, argument="name"
            )

        if not port_range:
            raise RequiredArgument(
                function=cls.create_port_list.__name__, argument="port_range"
            )

        cmd = XmlCommand("create_port_list")
        cmd.add_element("name", name)
        cmd.add_element("port_range", port_range)

        if comment:
            cmd.add_element("comment", comment)

        return cmd

    @classmethod
    def create_port_range(
        cls,
        port_list_id: EntityID,
        start: int,
        end: int,
        port_range_type: Union[str, PortRangeType],
        *,
        comment: Optional[str] = None,
    ) -> Request:
        """Create new port range

        Args:
            port_list_id: UUID of the port list to which to add the range
            start: The first port in the range
            end: The last port in the range
            port_range_type: The type of the ports: TCP, UDP, ...
            comment: Comment for the port range
        """
        if not port_list_id:
            raise RequiredArgument(
                function=cls.create_port_range.__name__,
                argument="port_list_id",
            )

        if not port_range_type:
            raise RequiredArgument(
                function=cls.create_port_range.__name__,
                argument="port_range_type",
            )

        if not start:
            raise RequiredArgument(
                function=cls.create_port_range.__name__, argument="start"
            )

        if not end:
            raise RequiredArgument(
                function=cls.create_port_range.__name__, argument="end"
            )

        if not isinstance(port_range_type, PortRangeType):
            port_range_type = PortRangeType(port_range_type)

        cmd = XmlCommand("create_port_range")
        cmd.add_element("port_list", attrs={"id": str(port_list_id)})
        cmd.add_element("start", str(start))
        cmd.add_element("end", str(end))
        cmd.add_element("type", port_range_type.value)

        if comment:
            cmd.add_element("comment", comment)

        return cmd

    @classmethod
    def delete_port_list(
        cls, port_list_id: EntityID, *, ultimate: bool = False
    ) -> Request:
        """Deletes an existing port list

        Args:
            port_list_id: UUID of the port list to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not port_list_id:
            raise RequiredArgument(
                function=cls.delete_port_list.__name__, argument="port_list_id"
            )

        cmd = XmlCommand("delete_port_list")
        cmd.set_attribute("port_list_id", str(port_list_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @classmethod
    def delete_port_range(cls, port_range_id: EntityID) -> Request:
        """Deletes an existing port range

        Args:
            port_range_id: UUID of the port range to be deleted.
        """
        if not port_range_id:
            raise RequiredArgument(
                function=cls.delete_port_range.__name__,
                argument="port_range_id",
            )

        cmd = XmlCommand("delete_port_range")
        cmd.set_attribute("port_range_id", str(port_range_id))

        return cmd

    @classmethod
    def get_port_lists(
        cls,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
        targets: Optional[bool] = None,
        trash: Optional[bool] = None,
    ) -> Request:
        """Request a list of port lists

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include full port list details
            targets: Whether to include targets using this port list
            trash: Whether to get port lists in the trashcan instead
        """
        cmd = XmlCommand("get_port_lists")

        cmd.add_filter(filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if targets is not None:
            cmd.set_attribute("targets", to_bool(targets))

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return cmd

    @classmethod
    def get_port_list(cls, port_list_id: EntityID) -> Request:
        """Request a single port list

        Args:
            port_list_id: UUID of an existing port list
        """
        cmd = XmlCommand("get_port_lists")

        if not port_list_id:
            raise RequiredArgument(
                function=cls.get_port_list.__name__, argument="port_list_id"
            )

        cmd.set_attribute("port_list_id", str(port_list_id))

        # for single entity always request all details

        cmd.set_attribute("details", "1")
        return cmd

    @classmethod
    def modify_port_list(
        cls,
        port_list_id: EntityID,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Request:
        """Modifies an existing port list.

        Args:
            port_list_id: UUID of port list to modify.
            name: Name of port list.
            comment: Comment on port list.
        """
        if not port_list_id:
            raise RequiredArgument(
                function=cls.modify_port_list.__name__, argument="port_list_id"
            )
        cmd = XmlCommand("modify_port_list")
        cmd.set_attribute("port_list_id", str(port_list_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        return cmd
