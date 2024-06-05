# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool, to_comma_list
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class Roles:

    @classmethod
    def clone_role(cls, role_id: EntityID) -> Request:
        """Clone an existing role

        Args:
            role_id: UUID of an existing role to clone from
        """
        if not role_id:
            raise RequiredArgument(
                function=cls.clone_role.__name__, argument="role_id"
            )

        cmd = XmlCommand("create_role")
        cmd.add_element("copy", str(role_id))
        return cmd

    @classmethod
    def create_role(
        cls,
        name: str,
        *,
        comment: Optional[str] = None,
        users: Optional[list[str]] = None,
    ) -> Request:
        """Create a new role

        Args:
            name: Name of the role
            comment: Comment for the role
            users: List of user names to add to the role
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_role.__name__, argument="name"
            )

        cmd = XmlCommand("create_role")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if users:
            cmd.add_element("users", to_comma_list(users))

        return cmd

    @classmethod
    def delete_role(
        cls, role_id: str, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Deletes an existing role

        Args:
            role_id: UUID of the role to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not role_id:
            raise RequiredArgument(
                function=cls.delete_role.__name__, argument="role_id"
            )

        cmd = XmlCommand("delete_role")
        cmd.set_attribute("role_id", role_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))
        return cmd

    @staticmethod
    def get_roles(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
    ) -> Request:
        """Request a list of roles

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan roles instead
        """
        cmd = XmlCommand("get_roles")

        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return cmd

    @classmethod
    def get_role(cls, role_id: EntityID) -> Request:
        """Request a single role

        Args:
            role_id: UUID of an existing role
        """
        if not role_id:
            raise RequiredArgument(
                function=cls.get_role.__name__, argument="role_id"
            )

        cmd = XmlCommand("get_roles")
        cmd.set_attribute("role_id", str(role_id))
        return cmd

    @classmethod
    def modify_role(
        cls,
        role_id: EntityID,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        users: Optional[list[str]] = None,
    ) -> Request:
        """Modifies an existing role.

        Args:
            role_id: UUID of role to modify.
            comment: Name of role.
            name: Comment on role.
            users: List of user names.
        """
        if not role_id:
            raise RequiredArgument(
                function=cls.modify_role.__name__, argument="role_id argument"
            )

        cmd = XmlCommand("modify_role")
        cmd.set_attribute("role_id", str(role_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if users:
            cmd.add_element("users", to_comma_list(users))

        return cmd
