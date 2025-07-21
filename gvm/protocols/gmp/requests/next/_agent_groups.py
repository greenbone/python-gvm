# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests._entity_id import EntityID
from gvm.utils import to_bool
from gvm.xml import XmlCommand


class AgentGroups:
    @classmethod
    def create_agent_group(
        cls,
        name: str,
        *,
        agent_ids: list[str],
        comment: Optional[str] = None,
    ) -> Request:
        """Create a new agent group.

        Args:
            name: Name of the new agent group.
            agent_ids: List of agent UUIDs to include in the group (required).
            comment: Optional comment for the group.

        Raises:
            RequiredArgument: If name or agent_ids is not provided.
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_agent_group.__name__, argument="name"
            )

        if not agent_ids:
            raise RequiredArgument(
                function=cls.create_agent_group.__name__, argument="agent_ids"
            )

        cmd = XmlCommand("create_agent_group")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        agents_element = cmd.add_element("agents")
        for agent_id in agent_ids:
            agents_element.add_element("agent", attrs={"id": agent_id})

        return cmd

    @classmethod
    def clone_agent_group(cls, agent_group_id: EntityID) -> Request:
        """Clone an existing agent group

        Args:
            agent_group_id: UUID of an existing agent group to clone from

        Returns:
            Request: GMP command to create a new agent group based on a copy
        """
        if not agent_group_id:
            raise RequiredArgument(
                function=cls.clone_agent_group.__name__,
                argument="agent_group_id",
            )

        cmd = XmlCommand("create_agent_group")
        cmd.add_element("copy", str(agent_group_id))

        return cmd

    @classmethod
    def modify_agent_group(
        cls,
        agent_group_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        agent_ids: Optional[list[str]] = None,
    ) -> Request:
        """Modify an existing agent group.

        Args:
            agent_group_id: UUID of the group to modify.
            name: Optional new name for the group.
            comment: Optional comment for the group.
            agent_ids: Optional list of agent UUIDs to set for the group.

        Raises:
            RequiredArgument: If agent_group_id is not provided.
        """
        if not agent_group_id:
            raise RequiredArgument(
                function=cls.modify_agent_group.__name__,
                argument="agent_group_id",
            )

        cmd = XmlCommand("modify_agent_group")
        cmd.set_attribute("agent_group_id", str(agent_group_id))

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if agent_ids:
            agents_element = cmd.add_element("agents")
            for agent_id in agent_ids:
                agents_element.add_element("agent", attrs={"id": agent_id})

        return cmd

    @classmethod
    def delete_agent_group(
        cls,
        agent_group_id: EntityID,
        *,
        ultimate: Optional[bool] = False,
    ) -> Request:
        """Delete an existing agent group.

        Args:
            agent_group_id: UUID of the group to delete.
            ultimate: Whether to permanently delete or move to trashcan.

        Raises:
            RequiredArgument: If agent_group_id is not provided.
        """
        if not agent_group_id:
            raise RequiredArgument(
                function=cls.delete_agent_group.__name__,
                argument="agent_group_id",
            )

        cmd = XmlCommand("delete_agent_group")
        cmd.set_attribute("agent_group_id", str(agent_group_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @classmethod
    def get_agent_groups(
        cls,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
    ) -> Request:
        """Request a list of agent groups.

        Args:
            filter_string: Filter expression to use.
            filter_id: UUID of a predefined filter.
            trash: If True, return trashed agent groups.

        Returns:
            Request object to fetch agent groups.
        """
        cmd = XmlCommand("get_agent_groups")
        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return cmd

    @classmethod
    def get_agent_group(cls, agent_group_id: EntityID) -> Request:
        """Request a single agent group by ID.

        Args:
            agent_group_id: UUID of the agent group.

        Raises:
            RequiredArgument: If agent_group_id is not provided.

        Returns:
            Request object to fetch the specific agent group.
        """
        if not agent_group_id:
            raise RequiredArgument(
                function=cls.get_agent_group.__name__, argument="agent_group_id"
            )

        cmd = XmlCommand("get_agent_groups")
        cmd.set_attribute("agent_group_id", str(agent_group_id))

        return cmd
