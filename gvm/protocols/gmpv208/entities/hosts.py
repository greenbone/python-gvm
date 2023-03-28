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

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class HostsOrdering(Enum):
    """Enum for host ordering during scans"""

    SEQUENTIAL = "sequential"
    RANDOM = "random"
    REVERSE = "reverse"

    @classmethod
    def from_string(
        cls,
        hosts_ordering: Optional[str],
    ) -> Optional["HostsOrdering"]:
        """Convert a hosts ordering string to an actual HostsOrdering instance

        Arguments:
            hosts_ordering: Host ordering string to convert to a HostsOrdering
        """
        if not hosts_ordering:
            return None
        try:
            return cls[hosts_ordering.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="hosts_ordering",
                function=cls.from_string.__name__,
            ) from None


class HostsMixin:
    def create_host(self, name: str, *, comment: Optional[str] = None) -> Any:
        """Create a new host host

        Arguments:
            name: Name for the new host host
            comment: Comment for the new host host

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_host.__name__, argument="name"
            )

        cmd = XmlCommand("create_asset")
        host = cmd.add_element("asset")
        host.add_element("type", "host")
        host.add_element("name", name)

        if comment:
            host.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def delete_host(self, host_id: str) -> Any:
        """Deletes an existing host

        Arguments:
            host_id: UUID of the single host to delete.
        """
        if not host_id:
            raise RequiredArgument(
                function=self.delete_host.__name__,
                argument="host_id",
            )

        cmd = XmlCommand("delete_asset")
        cmd.set_attribute("asset_id", host_id)

        return self._send_xml_command(cmd)

    def get_hosts(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of hosts

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include additional information (e.g. tags)

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        cmd = XmlCommand("get_assets")

        cmd.set_attribute("type", "host")

        add_filter(cmd, filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return self._send_xml_command(cmd)

    def get_host(self, host_id: str, *, details: Optional[bool] = None) -> Any:
        """Request a single host

        Arguments:
            host_id: UUID of an existing host
            details: Whether to include additional information (e.g. tags)

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_assets")

        if not host_id:
            raise RequiredArgument(
                function=self.get_host.__name__, argument="host_id"
            )

        cmd.set_attribute("asset_id", host_id)
        cmd.set_attribute("type", "host")

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return self._send_xml_command(cmd)

    def modify_host(
        self, host_id: str, *, comment: Optional[str] = None
    ) -> Any:
        """Modifies an existing host.

        Arguments:
            host_id: UUID of the host to be modified.
            comment: Comment for the host. Not passing a comment
                arguments clears the comment for this host.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not host_id:
            raise RequiredArgument(
                function=self.modify_host.__name__, argument="host_id"
            )

        cmd = XmlCommand("modify_asset")
        cmd.set_attribute("asset_id", host_id)
        if not comment:
            comment = ""
        cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)
