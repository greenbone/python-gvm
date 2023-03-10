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

from typing import Any, List, Optional

from gvm.errors import RequiredArgument
from gvm.utils import add_filter, to_bool, to_comma_list
from gvm.xml import XmlCommand


class GroupsMixin:
    def clone_group(self, group_id: str) -> Any:
        """Clone an existing group

        Arguments:
            group_id: UUID of an existing group to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_id:
            raise RequiredArgument(
                function=self.clone_group.__name__, argument="group_id"
            )

        cmd = XmlCommand("create_group")
        cmd.add_element("copy", group_id)
        return self._send_xml_command(cmd)

    def create_group(
        self,
        name: str,
        *,
        comment: Optional[str] = None,
        special: Optional[bool] = False,
        users: Optional[List[str]] = None,
    ) -> Any:
        """Create a new group

        Arguments:
            name: Name of the new group
            comment: Comment for the group
            special: Create permission giving members full access to each
                other's entities
            users: List of user names to be in the group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_group.__name__, argument="name"
            )

        cmd = XmlCommand("create_group")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if special:
            _xmlspecial = cmd.add_element("specials")
            _xmlspecial.add_element("full")

        if users:
            cmd.add_element("users", to_comma_list(users))

        return self._send_xml_command(cmd)

    def delete_group(
        self, group_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing group

        Arguments:
            group_id: UUID of the group to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not group_id:
            raise RequiredArgument(
                function=self.delete_group.__name__, argument="group_id"
            )

        cmd = XmlCommand("delete_group")
        cmd.set_attribute("group_id", group_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_groups(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
    ) -> Any:
        """Request a list of groups

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan groups instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_groups")

        add_filter(cmd, filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_group(self, group_id: str) -> Any:
        """Request a single group

        Arguments:
            group_id: UUID of an existing group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_groups")

        if not group_id:
            raise RequiredArgument(
                function=self.get_group.__name__, argument="group_id"
            )

        cmd.set_attribute("group_id", group_id)
        return self._send_xml_command(cmd)

    def modify_group(
        self,
        group_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        users: Optional[List[str]] = None,
    ) -> Any:
        """Modifies an existing group.

        Arguments:
            group_id: UUID of group to modify.
            comment: Comment on group.
            name: Name of group.
            users: List of user names to be in the group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_id:
            raise RequiredArgument(
                function=self.modify_group.__name__, argument="group_id"
            )

        cmd = XmlCommand("modify_group")
        cmd.set_attribute("group_id", group_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if users:
            cmd.add_element("users", to_comma_list(users))

        return self._send_xml_command(cmd)
