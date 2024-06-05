# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm._enum import Enum
from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool, to_comma_list
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class UserAuthType(Enum):
    """Enum for Sources allowed for authentication for the user"""

    FILE = "file"
    LDAP_CONNECT = "ldap_connect"
    RADIUS_CONNECT = "radius_connect"


class Users:

    @classmethod
    def create_user(
        cls,
        name: str,
        *,
        password: Optional[str] = None,
        hosts: Optional[list[str]] = None,
        hosts_allow: Optional[bool] = False,
        role_ids: Optional[list[EntityID]] = None,
    ) -> Request:
        """Create a new user

        Args:
            name: Name of the user
            password: Password of the user
            hosts: A list of host addresses (IPs, DNS names)
            hosts_allow: If True allow only access to passed hosts otherwise
                deny access. Default is False for deny hosts.
            role_ids: A list of role UUIDs for the user
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_user.__name__, argument="name"
            )

        cmd = XmlCommand("create_user")
        cmd.add_element("name", name)

        if password:
            cmd.add_element("password", password)

        if hosts:
            cmd.add_element(
                "hosts",
                to_comma_list(hosts),
                attrs={"allow": to_bool(hosts_allow)},
            )

        if role_ids:
            for role in role_ids:
                cmd.add_element("role", attrs={"id": str(role)})

        return cmd

    @classmethod
    def modify_user(
        cls,
        user_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        password: Optional[str] = None,
        auth_source: Optional[Union[UserAuthType, str]] = None,
        role_ids: Optional[list[EntityID]] = None,
        hosts: Optional[list[str]] = None,
        hosts_allow: Optional[bool] = False,
        group_ids: Optional[list[EntityID]] = None,
    ) -> Request:
        """Modify an existing user.

        Most of the fields need to be supplied
        for changing a single field even if no change is wanted for those.
        Else empty values are inserted for the missing fields instead.

        Args:
            user_id: UUID of the user to be modified.
            name: The new name for the user.
            comment: Comment on the user.
            password: The password for the user.
            auth_source: Source allowed for authentication for this user.
            roles_id: List of roles UUIDs for the user.
            hosts: User access rules: List of hosts.
            hosts_allow: Defines how the hosts list is to be interpreted.
                If False (default) the list is treated as a deny list.
                All hosts are allowed by default except those provided by
                the hosts parameter. If True the list is treated as a
                allow list. All hosts are denied by default except those
                provided by the hosts parameter.
            group_ids: List of group UUIDs for the user.
        """
        if not user_id:
            raise RequiredArgument(
                function=cls.modify_user.__name__, argument="user_id"
            )

        cmd = XmlCommand("modify_user")

        cmd.set_attribute("user_id", str(user_id))

        if name:
            cmd.add_element("new_name", name)

        if role_ids:
            for role in role_ids:
                cmd.add_element("role", attrs={"id": role})

        if hosts:
            cmd.add_element(
                "hosts",
                to_comma_list(hosts),
                attrs={"allow": to_bool(hosts_allow)},
            )

        if comment:
            cmd.add_element("comment", comment)

        if password:
            cmd.add_element("password", password)

        if auth_source:
            xml_auth_src = cmd.add_element("sources")
            if not isinstance(auth_source, UserAuthType):
                auth_source = UserAuthType(auth_source)
            xml_auth_src.add_element("source", auth_source.value)

        if group_ids:
            xml_groups = cmd.add_element("groups")
            for group_id in group_ids:
                xml_groups.add_element("group", attrs={"id": group_id})

        return cmd

    @classmethod
    def clone_user(cls, user_id: EntityID) -> Request:
        """Clone an existing user.

        Args:
            user_id: UUID of the user to be cloned.
        """
        if not user_id:
            raise RequiredArgument(
                function=cls.clone_user.__name__, argument="user_id"
            )

        cmd = XmlCommand("create_user")
        cmd.add_element("copy", str(user_id))
        return cmd

    @classmethod
    def delete_user(
        cls,
        user_id: Optional[EntityID] = None,
        *,
        name: Optional[str] = None,
        inheritor_id: Optional[EntityID] = None,
        inheritor_name: Optional[str] = None,
    ) -> Request:
        """Delete an existing user

        Either user_id or name must be passed.

        Args:
            user_id: UUID of the task to be deleted.
            name: The name of the user to be deleted.
            inheritor_id: The UUID of the inheriting user or "self". Overrides
                inheritor_name.
            inheritor_name: The name of the inheriting user.

        """
        if not user_id and not name:
            raise RequiredArgument(
                function=cls.delete_user.__name__, argument="user_id or name"
            )

        cmd = XmlCommand("delete_user")

        if user_id:
            cmd.set_attribute("user_id", str(user_id))

        if name:
            cmd.set_attribute("name", name)

        if inheritor_id:
            cmd.set_attribute("inheritor_id", str(inheritor_id))
        if inheritor_name:
            cmd.set_attribute("inheritor_name", inheritor_name)

        return cmd

    @staticmethod
    def get_users(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
    ) -> Request:
        """Request a list of users

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
        """
        cmd = XmlCommand("get_users")
        cmd.add_filter(filter_string, filter_id)
        return cmd

    @classmethod
    def get_user(cls, user_id: EntityID) -> Request:
        """Request a single user

        Args:
            user_id: UUID of the user to be requested.
        """
        if not user_id:
            raise RequiredArgument(
                function=cls.get_user.__name__, argument="user_id"
            )

        cmd = XmlCommand("get_users")
        cmd.set_attribute("user_id", str(user_id))
        return cmd
