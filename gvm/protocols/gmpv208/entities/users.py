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
from typing import Any, List, Optional

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.utils import add_filter, to_bool, to_comma_list
from gvm.xml import XmlCommand


class UserAuthType(Enum):
    """Enum for Sources allowed for authentication for the user"""

    FILE = "file"
    LDAP_CONNECT = "ldap_connect"
    RADIUS_CONNECT = "radius_connect"

    @classmethod
    def from_string(
        cls,
        user_auth_type: Optional[str],
    ) -> Optional["UserAuthType"]:
        """Convert a user auth type string into a UserAuthType instance"""
        if not user_auth_type:
            return None

        try:
            return cls[user_auth_type.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="user_auth_type",
                function=cls.from_string.__name__,
            ) from None


class UsersMixin:
    def clone_user(self, user_id: str) -> Any:
        """Clone an existing user

        Arguments:
            user_id: UUID of existing user to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not user_id:
            raise RequiredArgument(
                function=self.clone_user.__name__, argument="user_id"
            )

        cmd = XmlCommand("create_user")
        cmd.add_element("copy", user_id)
        return self._send_xml_command(cmd)

    def create_user(
        self,
        name: str,
        *,
        password: Optional[str] = None,
        hosts: Optional[List[str]] = None,
        hosts_allow: Optional[bool] = False,
        ifaces: Optional[List[str]] = None,
        ifaces_allow: Optional[bool] = False,
        role_ids: Optional[List[str]] = None,
    ) -> Any:
        """Create a new user

        Arguments:
            name: Name of the user
            password: Password of the user
            hosts: A list of host addresses (IPs, DNS names)
            hosts_allow: If True allow only access to passed hosts otherwise
                deny access. Default is False for deny hosts.
            ifaces: A list of interface names
            ifaces_allow: If True allow only access to passed interfaces
                otherwise deny access. Default is False for deny interfaces.
            role_ids: A list of role UUIDs for the user

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_user.__name__, argument="name"
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

        if ifaces:
            cmd.add_element(
                "ifaces",
                to_comma_list(ifaces),
                attrs={"allow": to_bool(ifaces_allow)},
            )

        if role_ids:
            for role in role_ids:
                cmd.add_element("role", attrs={"id": role})

        return self._send_xml_command(cmd)

    def delete_user(
        self,
        user_id: str = None,
        *,
        name: Optional[str] = None,
        inheritor_id: Optional[str] = None,
        inheritor_name: Optional[str] = None,
    ) -> Any:
        """Deletes an existing user

        Either user_id or name must be passed.

        Arguments:
            user_id: UUID of the task to be deleted.
            name: The name of the user to be deleted.
            inheritor_id: The ID of the inheriting user or "self". Overrides
                inheritor_name.
            inheritor_name: The name of the inheriting user.

        """
        if not user_id and not name:
            raise RequiredArgument(
                function=self.delete_user.__name__, argument="user_id or name"
            )

        cmd = XmlCommand("delete_user")

        if user_id:
            cmd.set_attribute("user_id", user_id)

        if name:
            cmd.set_attribute("name", name)

        if inheritor_id:
            cmd.set_attribute("inheritor_id", inheritor_id)
        if inheritor_name:
            cmd.set_attribute("inheritor_name", inheritor_name)

        return self._send_xml_command(cmd)

    def get_users(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
    ) -> Any:
        """Request a list of users

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_users")

        add_filter(cmd, filter_string, filter_id)

        return self._send_xml_command(cmd)

    def get_user(self, user_id: str) -> Any:
        """Request a single user

        Arguments:
            user_id: UUID of an existing user

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_users")

        if not user_id:
            raise RequiredArgument(
                function=self.get_user.__name__, argument="user_id"
            )

        cmd.set_attribute("user_id", user_id)
        return self._send_xml_command(cmd)

    def modify_user(
        self,
        user_id: str = None,
        name: str = None,
        *,
        new_name: Optional[str] = None,
        comment: Optional[str] = None,
        password: Optional[str] = None,
        auth_source: Optional[UserAuthType] = None,
        role_ids: Optional[List[str]] = None,
        hosts: Optional[List[str]] = None,
        hosts_allow: Optional[bool] = False,
        ifaces: Optional[List[str]] = None,
        ifaces_allow: Optional[bool] = False,
        group_ids: Optional[List[str]] = None,
    ) -> Any:
        """Modifies an existing user.

        Most of the fields need to be supplied
        for changing a single field even if no change is wanted for those.
        Else empty values are inserted for the missing fields instead.

        Arguments:
            user_id: UUID of the user to be modified. Overrides name element
                argument.
            name: The name of the user to be modified. Either user_id or name
                must be passed.
            new_name: The new name for the user.
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
            ifaces: User access rules: List of ifaces.
            ifaces_allow: Defines how the ifaces list is to be interpreted.
                If False (default) the list is treated as a deny list.
                All ifaces are allowed by default except those provided by
                the ifaces parameter. If True the list is treated as a
                allow list. All ifaces are denied by default except those
                provided by the ifaces parameter.
            group_ids: List of group UUIDs for the user.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not user_id and not name:
            raise RequiredArgument(
                function=self.modify_user.__name__, argument="user_id or name"
            )

        cmd = XmlCommand("modify_user")

        if user_id:
            cmd.set_attribute("user_id", user_id)
        else:
            cmd.add_element("name", name)

        if new_name:
            cmd.add_element("new_name", new_name)

        if role_ids:
            for role in role_ids:
                cmd.add_element("role", attrs={"id": role})

        if hosts:
            cmd.add_element(
                "hosts",
                to_comma_list(hosts),
                attrs={"allow": to_bool(hosts_allow)},
            )

        if ifaces:
            cmd.add_element(
                "ifaces",
                to_comma_list(ifaces),
                attrs={"allow": to_bool(ifaces_allow)},
            )

        if comment:
            cmd.add_element("comment", comment)

        if password:
            cmd.add_element("password", password)

        if auth_source:
            _xmlauthsrc = cmd.add_element("sources")
            _xmlauthsrc.add_element("source", auth_source.value)

        if group_ids:
            _xmlgroups = cmd.add_element("groups")
            for group_id in group_ids:
                _xmlgroups.add_element("group", attrs={"id": group_id})

        return self._send_xml_command(cmd)
