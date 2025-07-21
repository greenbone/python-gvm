# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests._entity_id import EntityID
from gvm.utils import to_bool
from gvm.xml import XmlCommand


class Agents:
    @classmethod
    def get_agents(
        cls,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of agents.

        Args:
            filter_string: Filter term to use for the query.
            filter_id: UUID of an existing filter to use for the query.
            details: Whether to include detailed agent info.
        """
        cmd = XmlCommand("get_agents")
        cmd.add_filter(filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return cmd

    @classmethod
    def modify_agents(
        cls,
        agent_ids: list[EntityID],
        *,
        authorized: Optional[bool] = None,
        min_interval: Optional[int] = None,
        heartbeat_interval: Optional[int] = None,
        schedule: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> Request:
        """Modify multiple agents

        Args:
            agent_ids: List of agent UUIDs to modify
            authorized: Whether the agent is authorized
            min_interval: Minimum scan interval
            heartbeat_interval: Interval for sending heartbeats
            schedule: Cron-style schedule for agent
            comment: Comment for the agents
        """
        if not agent_ids:
            raise RequiredArgument(
                function=cls.modify_agents.__name__, argument="agent_ids"
            )

        cmd = XmlCommand("modify_agents")
        xml_agents = cmd.add_element("agents")

        for agent_id in agent_ids:
            xml_agents.add_element("agent", attrs={"id": agent_id})

        if authorized is not None:
            cmd.add_element("authorized", to_bool(authorized))
        if min_interval is not None:
            cmd.add_element("min_interval", str(min_interval))
        if heartbeat_interval is not None:
            cmd.add_element("heartbeat_interval", str(heartbeat_interval))
        if schedule:
            cmd.add_element("schedule", schedule)
        if comment:
            cmd.add_element("comment", comment)

        return cmd

    @classmethod
    def delete_agents(cls, agent_ids: list[EntityID]) -> Request:
        """Delete multiple agents

        Args:
            agent_ids: List of agent UUIDs to delete
        """
        if not agent_ids:
            raise RequiredArgument(
                function=cls.delete_agents.__name__, argument="agent_ids"
            )

        cmd = XmlCommand("delete_agents")
        xml_agents = cmd.add_element("agents")

        for agent_id in agent_ids:
            xml_agents.add_element("agent", attrs={"id": agent_id})

        return cmd
