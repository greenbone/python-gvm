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

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv208.entities.entities import EntityType
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class TagsMixin:
    def clone_tag(self, tag_id: str) -> Any:
        """Clone an existing tag

        Arguments:
            tag_id: UUID of an existing tag to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tag_id:
            raise RequiredArgument(
                function=self.clone_tag.__name__, argument="tag_id"
            )

        cmd = XmlCommand("create_tag")
        cmd.add_element("copy", tag_id)
        return self._send_xml_command(cmd)

    def create_tag(
        self,
        name: str,
        resource_type: EntityType,
        *,
        resource_filter: Optional[str] = None,
        resource_ids: Optional[List[str]] = None,
        value: Optional[str] = None,
        comment: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> Any:
        """Create a tag.

        Arguments:
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

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_tag.__name__, argument="name"
            )

        if resource_filter and resource_ids:
            raise InvalidArgument(
                "create_tag accepts either resource_filter or resource_ids "
                "argument",
                function=self.create_tag.__name__,
            )

        if not resource_type:
            raise RequiredArgument(
                function=self.create_tag.__name__, argument="resource_type"
            )

        if not isinstance(resource_type, EntityType):
            raise InvalidArgumentType(
                function=self.create_tag.__name__,
                argument="resource_type",
                arg_type=EntityType.__name__,
            )

        cmd = XmlCommand("create_tag")
        cmd.add_element("name", name)

        _xmlresources = cmd.add_element("resources")
        if resource_filter is not None:
            _xmlresources.set_attribute("filter", resource_filter)

        for resource_id in resource_ids or []:
            _xmlresources.add_element(
                "resource", attrs={"id": str(resource_id)}
            )

        _actual_resource_type = resource_type
        if resource_type.value == EntityType.AUDIT.value:
            _actual_resource_type = EntityType.TASK
        elif resource_type.value == EntityType.POLICY.value:
            _actual_resource_type = EntityType.SCAN_CONFIG
        _xmlresources.add_element("type", _actual_resource_type.value)

        if comment:
            cmd.add_element("comment", comment)

        if value:
            cmd.add_element("value", value)

        if active is not None:
            if active:
                cmd.add_element("active", "1")
            else:
                cmd.add_element("active", "0")

        return self._send_xml_command(cmd)

    def delete_tag(
        self, tag_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing tag

        Arguments:
            tag_id: UUID of the tag to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not tag_id:
            raise RequiredArgument(
                function=self.delete_tag.__name__, argument="tag_id"
            )

        cmd = XmlCommand("delete_tag")
        cmd.set_attribute("tag_id", tag_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_tags(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        names_only: Optional[bool] = None,
    ) -> Any:
        """Request a list of tags

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get tags from the trashcan instead
            names_only: Whether to get only distinct tag names

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tags")

        add_filter(cmd, filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if names_only is not None:
            cmd.set_attribute("names_only", to_bool(names_only))

        return self._send_xml_command(cmd)

    def get_tag(self, tag_id: str) -> Any:
        """Request a single tag

        Arguments:
            tag_id: UUID of an existing tag

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tags")

        if not tag_id:
            raise RequiredArgument(
                function=self.get_tag.__name__, argument="tag_id"
            )

        cmd.set_attribute("tag_id", tag_id)
        return self._send_xml_command(cmd)

    def modify_tag(
        self,
        tag_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        value=None,
        active=None,
        resource_action: Optional[str] = None,
        resource_type: Optional[EntityType] = None,
        resource_filter: Optional[str] = None,
        resource_ids: Optional[List[str]] = None,
    ) -> Any:
        """Modifies an existing tag.

        Arguments:
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

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tag_id:
            raise RequiredArgument(
                function=self.modify_tag.__name__, argument="tag_id"
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
                    function=self.modify_tag.__name__, argument="resource_type"
                )

            _xmlresources = cmd.add_element("resources")
            if resource_action is not None:
                _xmlresources.set_attribute("action", resource_action)

            if resource_filter is not None:
                _xmlresources.set_attribute("filter", resource_filter)

            for resource_id in resource_ids or []:
                _xmlresources.add_element(
                    "resource", attrs={"id": str(resource_id)}
                )

            if resource_type is not None:
                if not isinstance(resource_type, EntityType):
                    raise InvalidArgumentType(
                        function=self.modify_tag.__name__,
                        argument="resource_type",
                        arg_type=EntityType.__name__,
                    )
                _actual_resource_type = resource_type
                if resource_type.value == EntityType.AUDIT.value:
                    _actual_resource_type = EntityType.TASK
                elif resource_type.value == EntityType.POLICY.value:
                    _actual_resource_type = EntityType.SCAN_CONFIG
                _xmlresources.add_element("type", _actual_resource_type.value)

        return self._send_xml_command(cmd)
