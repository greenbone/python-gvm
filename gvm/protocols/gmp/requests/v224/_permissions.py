# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm._enum import Enum
from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID
from ._entity_type import EntityType


class PermissionSubjectType(Enum):
    """Enum for permission subject type"""

    USER = "user"
    GROUP = "group"
    ROLE = "role"


class Permissions:

    @classmethod
    def clone_permission(cls, permission_id: EntityID) -> Request:
        """Clone an existing permission

        Args:
            permission_id: UUID of an existing permission to clone from
        """
        if not permission_id:
            raise RequiredArgument(
                function=cls.clone_permission.__name__,
                argument="permission_id",
            )

        cmd = XmlCommand("create_permission")
        cmd.add_element("copy", str(permission_id))
        return cmd

    @classmethod
    def create_permission(
        cls,
        name: str,
        subject_id: EntityID,
        subject_type: Union[PermissionSubjectType, str],
        *,
        resource_id: Optional[str] = None,
        resource_type: Optional[Union[EntityType, str]] = None,
        comment: Optional[str] = None,
    ) -> Request:
        """Create a new permission

        Args:
            name: Name of the new permission
            subject_id: UUID of subject to whom the permission is granted
            subject_type: Type of the subject user, group or role
            comment: Comment for the permission
            resource_id: UUID of entity to which the permission applies
            resource_type: Type of the resource. For Super permissions user,
                group or role
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_permission.__name__, argument="name"
            )

        if not subject_id:
            raise RequiredArgument(
                function=cls.create_permission.__name__, argument="subject_id"
            )

        if not isinstance(subject_type, PermissionSubjectType):
            subject_type = PermissionSubjectType(subject_type)

        cmd = XmlCommand("create_permission")
        cmd.add_element("name", name)

        xml_subject = cmd.add_element("subject", attrs={"id": str(subject_id)})
        xml_subject.add_element("type", subject_type.value)

        if comment:
            cmd.add_element("comment", comment)

        if resource_id or resource_type:
            if not resource_id:
                raise RequiredArgument(
                    function=cls.create_permission.__name__,
                    argument="resource_id",
                )

            if not resource_type:
                raise RequiredArgument(
                    function=cls.create_permission.__name__,
                    argument="resource_type",
                )

            if not isinstance(resource_type, EntityType):
                resource_type = EntityType(resource_type)

            xml_resource = cmd.add_element(
                "resource", attrs={"id": resource_id}
            )

            actual_resource_type = resource_type
            if resource_type.value == EntityType.AUDIT.value:
                actual_resource_type = EntityType.TASK
            elif resource_type.value == EntityType.POLICY.value:
                actual_resource_type = EntityType.SCAN_CONFIG

            xml_resource.add_element("type", actual_resource_type.value)

        return cmd

    @classmethod
    def delete_permission(
        cls, permission_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Deletes an existing permission

        Args:
            permission_id: UUID of the permission to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not permission_id:
            raise RequiredArgument(
                function=cls.delete_permission.__name__,
                argument="permission_id",
            )

        cmd = XmlCommand("delete_permission")
        cmd.set_attribute("permission_id", str(permission_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @staticmethod
    def get_permissions(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
    ) -> Request:
        """Request a list of permissions

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get permissions in the trashcan instead
        """
        cmd = XmlCommand("get_permissions")

        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return cmd

    @classmethod
    def get_permission(cls, permission_id: EntityID) -> Request:
        """Request a single permission

        Args:
            permission_id: UUID of an existing permission
        """
        cmd = XmlCommand("get_permissions")

        if not permission_id:
            raise RequiredArgument(
                function=cls.get_permission.__name__, argument="permission_id"
            )

        cmd.set_attribute("permission_id", str(permission_id))
        return cmd

    @classmethod
    def modify_permission(
        cls,
        permission_id: EntityID,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        resource_id: Optional[EntityID] = None,
        resource_type: Optional[Union[EntityType, str]] = None,
        subject_id: Optional[EntityID] = None,
        subject_type: Optional[Union[PermissionSubjectType, str]] = None,
    ) -> Request:
        """Modifies an existing permission.

        Args:
            permission_id: UUID of permission to be modified.
            comment: The comment on the permission.
            name: Permission name, currently the name of a command.
            subject_id: UUID of subject to whom the permission is granted
            subject_type: Type of the subject user, group or role
            resource_id: UUID of entity to which the permission applies
            resource_type: Type of the resource. For Super permissions user,
                group or role
        """
        if not permission_id:
            raise RequiredArgument(
                function=cls.modify_permission.__name__,
                argument="permission_id",
            )

        cmd = XmlCommand("modify_permission")
        cmd.set_attribute("permission_id", str(permission_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if resource_id or resource_type:
            if not resource_id:
                raise RequiredArgument(
                    function=cls.modify_permission.__name__,
                    argument="resource_id",
                )

            if not resource_type:
                raise RequiredArgument(
                    function=cls.modify_permission.__name__,
                    argument="resource_type",
                )

            if not isinstance(resource_type, EntityType):
                resource_type = EntityType(resource_type)

            xml_resource = cmd.add_element(
                "resource", attrs={"id": str(resource_id)}
            )
            actual_resource_type = resource_type
            if resource_type.value == EntityType.AUDIT.value:
                actual_resource_type = EntityType.TASK
            elif resource_type.value == EntityType.POLICY.value:
                actual_resource_type = EntityType.SCAN_CONFIG
            xml_resource.add_element("type", actual_resource_type.value)

        if subject_id or subject_type:
            if not subject_id:
                raise RequiredArgument(
                    function=cls.modify_permission.__name__,
                    argument="subject_id",
                )

            if not subject_type:
                raise RequiredArgument(
                    function=cls.modify_permission.__name__,
                    argument="subject_type",
                )

            if not isinstance(subject_type, PermissionSubjectType):
                subject_type = PermissionSubjectType(subject_type)

            xml_subject = cmd.add_element(
                "subject", attrs={"id": str(subject_id)}
            )
            xml_subject.add_element("type", subject_type.value)

        return cmd
