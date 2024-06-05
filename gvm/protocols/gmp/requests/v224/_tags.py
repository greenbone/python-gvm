# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID
from ._entity_type import EntityType


class Tags:

    @classmethod
    def clone_tag(cls, tag_id: EntityID) -> Request:
        """Clone an existing tag

        Args:
            tag_id: UUID of an existing tag to clone from
        """
        if not tag_id:
            raise RequiredArgument(
                function=cls.clone_tag.__name__, argument="tag_id"
            )

        cmd = XmlCommand("create_tag")
        cmd.add_element("copy", str(tag_id))
        return cmd

    @classmethod
    def create_tag(
        cls,
        name: str,
        resource_type: EntityType,
        *,
        resource_filter: Optional[str] = None,
        resource_ids: Optional[list[EntityID]] = None,
        value: Optional[str] = None,
        comment: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> Request:
        """Create a tag

        Args:
            name: Name of the tag. A full tag name consisting of namespace and
                predicate e.g. `foo:bar`.
            resource_type: Entity type the tag is to be attached to.
            resource_filter: Filter term to select resources the tag is to be
                attached to. Only one of resource_filter or resource_ids can be
                provided.
            resource_ids: IDs of the resources the tag is to be attached to.
                Only one of resource_filter or resource_ids can be provided.
            value: Value associated with the tag.
            comment: Comment for the tag.
            active: Whether the tag should be active.
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_tag.__name__, argument="name"
            )

        if resource_filter and resource_ids:
            raise InvalidArgument(
                "create_tag accepts either resource_filter or resource_ids "
                "argument",
                function=cls.create_tag.__name__,
            )

        if not resource_type:
            raise RequiredArgument(
                function=cls.create_tag.__name__, argument="resource_type"
            )

        if not isinstance(resource_type, EntityType):
            resource_type = EntityType(resource_type)

        cmd = XmlCommand("create_tag")
        cmd.add_element("name", name)

        xml_resources = cmd.add_element("resources")
        if resource_filter is not None:
            xml_resources.set_attribute("filter", resource_filter)

        for resource_id in resource_ids or []:
            xml_resources.add_element(
                "resource", attrs={"id": str(resource_id)}
            )

        actual_resource_type = resource_type
        if resource_type.value == EntityType.AUDIT.value:
            actual_resource_type = EntityType.TASK
        elif resource_type.value == EntityType.POLICY.value:
            actual_resource_type = EntityType.SCAN_CONFIG
        xml_resources.add_element("type", actual_resource_type.value)

        if comment:
            cmd.add_element("comment", comment)

        if value:
            cmd.add_element("value", value)

        if active is not None:
            cmd.add_element("active", to_bool(active))

        return cmd

    @classmethod
    def delete_tag(
        cls, tag_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Deletes an existing tag

        Args:
            tag_id: UUID of the tag to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not tag_id:
            raise RequiredArgument(
                function=cls.delete_tag.__name__, argument="tag_id"
            )

        cmd = XmlCommand("delete_tag")
        cmd.set_attribute("tag_id", str(tag_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @staticmethod
    def get_tags(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        names_only: Optional[bool] = None,
    ) -> Request:
        """Request a list of tags

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get tags from the trashcan instead
            names_only: Whether to get only distinct tag names
        """
        cmd = XmlCommand("get_tags")

        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if names_only is not None:
            cmd.set_attribute("names_only", to_bool(names_only))

        return cmd

    @classmethod
    def get_tag(cls, tag_id: EntityID) -> Request:
        """Request a single tag

        Args:
            tag_id: UUID of an existing tag
        """
        cmd = XmlCommand("get_tags")

        if not tag_id:
            raise RequiredArgument(
                function=cls.get_tag.__name__, argument="tag_id"
            )

        cmd.set_attribute("tag_id", str(tag_id))
        return cmd

    @classmethod
    def modify_tag(
        cls,
        tag_id: EntityID,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
        active: Optional[bool] = None,
        resource_action: Optional[str] = None,
        resource_type: Optional[EntityType] = None,
        resource_filter: Optional[str] = None,
        resource_ids: Optional[list[EntityID]] = None,
    ) -> Request:
        """Modifies an existing tag.

        Args:
            tag_id: UUID of the tag.
            comment: Comment to add to the tag.
            name: Name of the tag.
            value: Value of the tag.
            active: Whether the tag is active.
            resource_action: Whether to add or remove resources instead of
                overwriting. One of '', 'add', 'set' or 'remove'.
            resource_type: Type of the resources to which to attach the tag.
                Required if resource_filter is set.
            resource_filter: Filter term to select resources the tag is to be
                attached to.
            resource_ids: IDs of the resources to which to attach the tag.
        """
        if not tag_id:
            raise RequiredArgument(
                function=cls.modify_tag.__name__, argument="tag_id"
            )

        cmd = XmlCommand("modify_tag")
        cmd.set_attribute("tag_id", str(tag_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if value:
            cmd.add_element("value", value)

        if active is not None:
            cmd.add_element("active", to_bool(active))

        if resource_action or resource_filter or resource_ids or resource_type:
            if resource_filter and not resource_type:
                raise RequiredArgument(
                    function=cls.modify_tag.__name__, argument="resource_type"
                )

            xml_resources = cmd.add_element("resources")
            if resource_action is not None:
                xml_resources.set_attribute("action", resource_action)

            if resource_filter is not None:
                xml_resources.set_attribute("filter", resource_filter)

            for resource_id in resource_ids or []:
                xml_resources.add_element(
                    "resource", attrs={"id": str(resource_id)}
                )

            if resource_type is not None:
                if not isinstance(resource_type, EntityType):
                    resource_type = EntityType(resource_type)

                actual_resource_type = resource_type
                if resource_type.value == EntityType.AUDIT.value:
                    actual_resource_type = EntityType.TASK
                elif resource_type.value == EntityType.POLICY.value:
                    actual_resource_type = EntityType.SCAN_CONFIG
                xml_resources.add_element("type", actual_resource_type.value)

        return cmd
