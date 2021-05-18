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


class OperatingSystemsMixin:
    def delete_operating_system(
        self,
        *,
        operating_system_id: Optional[str] = None,
        report_id: Optional[str] = None,
    ) -> Any:
        """Deletes an existing operating_system

        Arguments:
            operating_system_id: UUID of the single operating_system to delete.
            report_id: UUID of report from which to get all
                operating_systems to delete.
        """
        if not operating_system_id and not report_id:
            raise RequiredArgument(
                function=self.delete_operating_system.__name__,
                argument='operating_system_id or report_id',
            )

        cmd = XmlCommand("delete_asset")
        if operating_system_id:
            cmd.set_attribute("asset_id", operating_system_id)
        else:
            cmd.set_attribute("report_id", report_id)

        return self._send_xml_command(cmd)

    def get_operating_systems(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
    ) -> Any:
        """Request a list of operating_systems

        Arguments:
            operating_system_type: Either 'os' or 'host'
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        cmd = XmlCommand("get_assets")

        cmd.set_attribute("type", "os")

        add_filter(cmd, filter, filter_id)

        return self._send_xml_command(cmd)

    def get_operating_system(self, operating_system_id: str) -> Any:
        """Request a single operating_system

        Arguments:
            operating_system_id: UUID of an existing operating_system
            operating_system_type: Either 'os' or 'host'

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_assets")

        if not operating_system_id:
            raise RequiredArgument(
                function=self.get_operating_system.__name__,
                argument='operating_system_id',
            )

        cmd.set_attribute("asset_id", operating_system_id)
        cmd.set_attribute("type", "os")

        return self._send_xml_command(cmd)

    def modify_operating_system(
        self, operating_system_id: str, comment: Optional[str] = ""
    ) -> Any:
        """Modifies an existing operating_system.

        Arguments:
            operating_system_id: UUID of the operating_system to be modified.
            comment: Comment for the operating_system.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not operating_system_id:
            raise RequiredArgument(
                function=self.modify_operating_system.__name__,
                argument='operating_system_id',
            )

        cmd = XmlCommand("modify_asset")
        cmd.set_attribute("asset_id", operating_system_id)
        cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)