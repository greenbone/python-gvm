# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm._enum import Enum
from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class HostsOrdering(Enum):
    """Enum for host ordering during scans"""

    SEQUENTIAL = "sequential"
    RANDOM = "random"
    REVERSE = "reverse"


class Hosts:

    @classmethod
    def create_host(
        cls, name: str, *, comment: Optional[str] = None
    ) -> Request:
        """Create a new host host

        Args:
            name: Name for the new host host
            comment: Comment for the new host host
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_host.__name__, argument="name"
            )

        cmd = XmlCommand("create_asset")
        host = cmd.add_element("asset")
        host.add_element("type", "host")
        host.add_element("name", name)

        if comment:
            host.add_element("comment", comment)

        return cmd

    @classmethod
    def delete_host(cls, host_id: EntityID) -> Request:
        """Deletes an existing host

        Args:
            host_id: UUID of the single host to delete.
        """
        if not host_id:
            raise RequiredArgument(
                function=cls.delete_host.__name__,
                argument="host_id",
            )

        cmd = XmlCommand("delete_asset")
        cmd.set_attribute("asset_id", str(host_id))

        return cmd

    @staticmethod
    def get_hosts(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of hosts

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include additional information (e.g. tags)
        """

        cmd = XmlCommand("get_assets")

        cmd.set_attribute("type", "host")

        cmd.add_filter(filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return cmd

    @classmethod
    def get_host(
        cls, host_id: EntityID, *, details: Optional[bool] = None
    ) -> Request:
        """Request a single host

        Arguments:
            host_id: UUID of an existing host
            details: Whether to include additional information (e.g. tags)
        """
        cmd = XmlCommand("get_assets")

        if not host_id:
            raise RequiredArgument(
                function=cls.get_host.__name__, argument="host_id"
            )

        cmd.set_attribute("asset_id", str(host_id))
        cmd.set_attribute("type", "host")

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return cmd

    @classmethod
    def modify_host(
        cls, host_id: EntityID, *, comment: Optional[str] = None
    ) -> Request:
        """Modifies an existing host.

        Args:
            host_id: UUID of the host to be modified.
            comment: Comment for the host. Not passing a comment
                arguments clears the comment for this host.
        """
        if not host_id:
            raise RequiredArgument(
                function=cls.modify_host.__name__, argument="host_id"
            )

        cmd = XmlCommand("modify_asset")
        cmd.set_attribute("asset_id", str(host_id))
        if not comment:
            comment = ""
        cmd.add_element("comment", comment)

        return cmd
