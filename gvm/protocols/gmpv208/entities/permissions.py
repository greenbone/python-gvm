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

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv208.entities.entities import EntityType
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class PermissionSubjectType(Enum):
    """Enum for permission subject type"""

    USER = "user"
    GROUP = "group"
    ROLE = "role"

    @classmethod
    def from_string(
        cls,
        subject_type: Optional[str],
    ) -> Optional["PermissionSubjectType"]:
        """Convert a permission subject type string to an actual
        PermissionSubjectType instance

        Arguments:
            subject_type: Permission subject type string to convert to a
                PermissionSubjectType
        """
        if not subject_type:
            return None

        try:
            return cls[subject_type.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="subject_type",
                function=cls.from_string.__name__,
            ) from None


class PermissionsMixin:
    def clone_permission(self, permission_id: str) -> Any:
        """Clone an existing permission

        Arguments:
            permission_id: UUID of an existing permission to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not permission_id:
            raise RequiredArgument(
                function=self.clone_permission.__name__,
                argument="permission_id",
            )

        cmd = XmlCommand("create_permission")
        cmd.add_element("copy", permission_id)
        return self._send_xml_command(cmd)

    def create_permission(
        self,
        name: str,
        subject_id: str,
        subject_type: PermissionSubjectType,
        *,
        resource_id: Optional[str] = None,
        resource_type: Optional[EntityType] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Create a new permission

        Arguments:
            name: Name of the new permission
            subject_id: UUID of subject to whom the permission is granted
            subject_type: Type of the subject user, group or role
            comment: Comment for the permission
            resource_id: UUID of entity to which the permission applies
            resource_type: Type of the resource. For Super permissions user,
                group or role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_permission.__name__, argument="name"
            )

        if not subject_id:
            raise RequiredArgument(
                function=self.create_permission.__name__, argument="subject_id"
            )

        if not isinstance(subject_type, PermissionSubjectType):
            raise InvalidArgumentType(
                function=self.create_permission.__name__,
                argument="subject_type",
                arg_type=PermissionSubjectType.__name__,
            )

        cmd = XmlCommand("create_permission")
        cmd.add_element("name", name)

        _xmlsubject = cmd.add_element("subject", attrs={"id": subject_id})
        _xmlsubject.add_element("type", subject_type.value)

        if comment:
            cmd.add_element("comment", comment)

        if resource_id or resource_type:
            if not resource_id:
                raise RequiredArgument(
                    function=self.create_permission.__name__,
                    argument="resource_id",
                )

            if not resource_type:
                raise RequiredArgument(
                    function=self.create_permission.__name__,
                    argument="resource_type",
                )

            if not isinstance(resource_type, EntityType):
                raise InvalidArgumentType(
                    function=self.create_permission.__name__,
                    argument="resource_type",
                    arg_type=EntityType.__name__,
                )

            _xmlresource = cmd.add_element(
                "resource", attrs={"id": resource_id}
            )

            _actual_resource_type = resource_type
            if resource_type.value == EntityType.AUDIT.value:
                _actual_resource_type = EntityType.TASK
            elif resource_type.value == EntityType.POLICY.value:
                _actual_resource_type = EntityType.SCAN_CONFIG

            _xmlresource.add_element("type", _actual_resource_type.value)

        return self._send_xml_command(cmd)

    def delete_permission(
        self, permission_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing permission

        Arguments:
            permission_id: UUID of the permission to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not permission_id:
            raise RequiredArgument(
                function=self.delete_permission.__name__,
                argument="permission_id",
            )

        cmd = XmlCommand("delete_permission")
        cmd.set_attribute("permission_id", permission_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_permissions(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
    ) -> Any:
        """Request a list of permissions

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get permissions in the trashcan instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_permissions")

        add_filter(cmd, filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_permission(self, permission_id: str) -> Any:
        """Request a single permission

        Arguments:
            permission_id: UUID of an existing permission

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_permissions")

        if not permission_id:
            raise RequiredArgument(
                function=self.get_permission.__name__, argument="permission_id"
            )

        cmd.set_attribute("permission_id", permission_id)
        return self._send_xml_command(cmd)

    def modify_permission(
        self,
        permission_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[EntityType] = None,
        subject_id: Optional[str] = None,
        subject_type: Optional[PermissionSubjectType] = None,
    ) -> Any:
        """Modifies an existing permission.

        Arguments:
            permission_id: UUID of permission to be modified.
            comment: The comment on the permission.
            name: Permission name, currently the name of a command.
            subject_id: UUID of subject to whom the permission is granted
            subject_type: Type of the subject user, group or role
            resource_id: UUID of entity to which the permission applies
            resource_type: Type of the resource. For Super permissions user,
                group or role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not permission_id:
            raise RequiredArgument(
                function=self.modify_permission.__name__,
                argument="permission_id",
            )

        cmd = XmlCommand("modify_permission")
        cmd.set_attribute("permission_id", permission_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if resource_id or resource_type:
            if not resource_id:
                raise RequiredArgument(
                    function=self.modify_permission.__name__,
                    argument="resource_id",
                )

            if not resource_type:
                raise RequiredArgument(
                    function=self.modify_permission.__name__,
                    argument="resource_type",
                )

            if not isinstance(resource_type, EntityType):
                raise InvalidArgumentType(
                    function=self.modify_permission.__name__,
                    argument="resource_type",
                    arg_type=EntityType.__name__,
                )

            _xmlresource = cmd.add_element(
                "resource", attrs={"id": resource_id}
            )
            _actual_resource_type = resource_type
            if resource_type.value == EntityType.AUDIT.value:
                _actual_resource_type = EntityType.TASK
            elif resource_type.value == EntityType.POLICY.value:
                _actual_resource_type = EntityType.SCAN_CONFIG
            _xmlresource.add_element("type", _actual_resource_type.value)

        if subject_id or subject_type:
            if not subject_id:
                raise RequiredArgument(
                    function=self.modify_permission.__name__,
                    argument="subject_id",
                )

            if not isinstance(subject_type, PermissionSubjectType):
                raise InvalidArgumentType(
                    function=self.modify_permission.__name__,
                    argument="subject_type",
                    arg_type=PermissionSubjectType.__name__,
                )

            _xmlsubject = cmd.add_element("subject", attrs={"id": subject_id})
            _xmlsubject.add_element("type", subject_type.value)

        return self._send_xml_command(cmd)
