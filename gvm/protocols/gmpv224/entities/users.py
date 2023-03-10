# -*- coding: utf-8 -*-
# Copyright (C) 2022 Greenbone AG
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

# pylint: disable=arguments-differ, arguments-renamed

from typing import Any, List, Optional

from gvm.errors import RequiredArgument
from gvm.protocols.gmpv214.entities.users import UserAuthType
from gvm.protocols.gmpv214.entities.users import UsersMixin as Gmp214UsersMixin
from gvm.utils import deprecation, to_bool, to_comma_list
from gvm.xml import XmlCommand


class UsersMixin(Gmp214UsersMixin):
    def create_user(
        self,
        name: str,
        *,
        password: Optional[str] = None,
        hosts: Optional[List[str]] = None,
        hosts_allow: Optional[bool] = False,
        ifaces: Any = None,
        ifaces_allow: Any = None,
        role_ids: Optional[List[str]] = None,
    ) -> Any:
        """Create a new user

        Arguments:
            name: Name of the user
            password: Password of the user
            hosts: A list of host addresses (IPs, DNS names)
            hosts_allow: If True allow only access to passed hosts otherwise
                deny access. Default is False for deny hosts.
            ifaces: deprecated
            ifaces_allow: deprecated
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

        if ifaces is not None:
            major, minor = self.get_protocol_version()
            deprecation(
                "The ifaces parameter has been removed in GMP"
                f" version {major}{minor}"
            )

        if ifaces_allow is not None:
            major, minor = self.get_protocol_version()
            deprecation(
                "The ifaces_allow parameter has been removed in GMP"
                f" version {major}{minor}"
            )

        if role_ids:
            for role in role_ids:
                cmd.add_element("role", attrs={"id": role})

        return self._send_xml_command(cmd)

    def modify_user(
        self,
        user_id: str = None,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        password: Optional[str] = None,
        auth_source: Optional[UserAuthType] = None,
        role_ids: Optional[List[str]] = None,
        hosts: Optional[List[str]] = None,
        hosts_allow: Optional[bool] = False,
        ifaces: Any = None,
        ifaces_allow: Any = None,
        group_ids: Optional[List[str]] = None,
    ) -> Any:
        """Modifies an existing user.

        Most of the fields need to be supplied
        for changing a single field even if no change is wanted for those.
        Else empty values are inserted for the missing fields instead.

        Arguments:
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
            ifaces: deprecated
            ifaces_allow: deprecated
            group_ids: List of group UUIDs for the user.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not user_id:
            raise RequiredArgument(
                function=self.modify_user.__name__, argument="user_id"
            )

        cmd = XmlCommand("modify_user")

        cmd.set_attribute("user_id", user_id)

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

        if ifaces is not None:
            major, minor = self.get_protocol_version()
            deprecation(
                "The ifaces parameter has been removed in GMP"
                f" version {major}{minor}"
            )

        if ifaces_allow is not None:
            major, minor = self.get_protocol_version()
            deprecation(
                "The ifaces_allow parameter has been removed in GMP"
                f" version {major}{minor}"
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
