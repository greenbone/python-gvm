# -*- coding: utf-8 -*-
# Copyright (C) 2021 Greenbone Networks GmbH
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

# pylint:  disable=redefined-builtin

from typing import Any, Optional

from gvm.errors import RequiredArgument
from gvm.utils import add_filter
from gvm.xml import XmlCommand


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
                function=self.create_host.__name__, argument='name'
            )

        cmd = XmlCommand("create_asset")
        host = cmd.add_element("asset")
        host.add_element("type", "host")  # ignored for gmp7, required for gmp8
        host.add_element("name", name)

        if comment:
            host.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def delete_host(
        self, *, host_id: Optional[str] = None, report_id: Optional[str] = None
    ) -> Any:
        """Deletes an existing host

        Arguments:
            host_id: UUID of the single host to delete.
            report_id: UUID of report from which to get all
                hosts to delete.
        """
        if not host_id and not report_id:
            raise RequiredArgument(
                function=self.delete_host.__name__,
                argument='host_id or report_id',
            )

        cmd = XmlCommand("delete_asset")
        if host_id:
            cmd.set_attribute("asset_id", host_id)
        else:
            cmd.set_attribute("report_id", report_id)

        return self._send_xml_command(cmd)

    def get_hosts(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
    ) -> Any:
        """Request a list of hosts

        Arguments:
            host_type: Either 'os' or 'host'
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        cmd = XmlCommand("get_assets")

        cmd.set_attribute("type", "host")

        add_filter(cmd, filter, filter_id)

        return self._send_xml_command(cmd)

    def get_host(self, host_id: str) -> Any:
        """Request a single host

        Arguments:
            host_id: UUID of an existing host
            host_type: Either 'os' or 'host'

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_assets")

        if not host_id:
            raise RequiredArgument(
                function=self.get_host.__name__, argument='host_id'
            )

        cmd.set_attribute("asset_id", host_id)
        cmd.set_attribute("type", "host")

        return self._send_xml_command(cmd)

    def modify_host(self, host_id: str, comment: Optional[str] = "") -> Any:
        """Modifies an existing host.

        Arguments:
            host_id: UUID of the host to be modified.
            comment: Comment for the host.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not host_id:
            raise RequiredArgument(
                function=self.modify_host.__name__, argument='host_id'
            )

        cmd = XmlCommand("modify_asset")
        cmd.set_attribute("asset_id", host_id)
        cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)
