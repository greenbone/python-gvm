# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool, to_comma_list
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class Groups:
    @classmethod
    def clone_group(cls, group_id: EntityID) -> Request:
        """Clone an existing group

        Args:
            group_id: UUID of an existing group to clone from
        """
        if not group_id:
            raise RequiredArgument(
                function=cls.clone_group.__name__, argument="group_id"
            )

        cmd = XmlCommand("create_group")
        cmd.add_element("copy", str(group_id))

        return cmd

    @classmethod
    def create_group(
        cls,
        name: str,
        *,
        comment: Optional[str] = None,
        special: Optional[bool] = False,
        users: Optional[list[str]] = None,
    ) -> Request:
        """Create a new group

        Args:
            name: Name of the new group
            comment: Comment for the group
            special: Create permission giving members full access to each
                other's entities
            users: List of user names to be in the group
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_group.__name__, argument="name"
            )

        cmd = XmlCommand("create_group")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if special:
            xml_special = cmd.add_element("specials")
            xml_special.add_element("full")

        if users:
            cmd.add_element("users", to_comma_list(users))

        return cmd

    @classmethod
    def delete_group(
        cls, group_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Deletes an existing group

        Args:
            group_id: UUID of the group to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not group_id:
            raise RequiredArgument(
                function=cls.delete_group.__name__, argument="group_id"
            )

        cmd = XmlCommand("delete_group")
        cmd.set_attribute("group_id", str(group_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @staticmethod
    def get_groups(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
    ) -> Request:
        """Request a list of groups

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan groups instead
        """
        cmd = XmlCommand("get_groups")

        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return cmd

    @classmethod
    def get_group(cls, group_id: EntityID) -> Request:
        """Request a single group

        Args:
            group_id: UUID of an existing group
        """
        cmd = XmlCommand("get_groups")

        if not group_id:
            raise RequiredArgument(
                function=cls.get_group.__name__, argument="group_id"
            )

        cmd.set_attribute("group_id", str(group_id))
        return cmd

    @classmethod
    def modify_group(
        cls,
        group_id: EntityID,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        users: Optional[list[str]] = None,
    ) -> Request:
        """Modifies an existing group.

        Args:
            group_id: UUID of group to modify.
            comment: Comment on group.
            name: Name of group.
            users: List of user names to be in the group
        """
        if not group_id:
            raise RequiredArgument(
                function=cls.modify_group.__name__, argument="group_id"
            )

        cmd = XmlCommand("modify_group")
        cmd.set_attribute("group_id", str(group_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if users:
            cmd.add_element("users", to_comma_list(users))

        return cmd
