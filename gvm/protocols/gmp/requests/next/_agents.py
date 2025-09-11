# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Mapping, Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests._entity_id import EntityID
from gvm.utils import to_bool
from gvm.xml import XmlCommand


class Agents:

    @staticmethod
    def _add_el(parent, name: str, value) -> None:
        """
        Helper to add a sub-element with a value if the value is not None.

        Args:
            parent: The XML parent element to which the new element is added.
            name: Name of the sub-element to create.
            value: Value to set as the text of the sub-element. If None, the
                element will not be created.
        """
        if value is not None:
            parent.add_element(name, str(value))

    @classmethod
    def _append_agent_config(cls, parent, config: Mapping[str, Any]) -> None:
        """
        Append an agent configuration block to the given XML parent element.

        Expected config structure::

            {
                "agent_control": {
                    "retry": {
                        "attempts": 6,
                        "delay_in_seconds": 60,
                        "max_jitter_in_seconds": 10
                    }
                },
                "agent_script_executor": {
                    "bulk_size": 2,
                    "bulk_throttle_time_in_ms": 300,
                    "indexer_dir_depth": 100,
                    "scheduler_cron_time": ["0 */12 * * *"]
                },
                "heartbeat": {
                    "interval_in_seconds": 300,
                    "miss_until_inactive": 1
                }
            }

        Args:
            parent: The XML parent element to which the `<config>` element
                should be appended.
            config: Mapping containing the agent configuration fields to
                serialize.
        """
        xml_config = parent.add_element("config")

        # agent_control.retry
        ac = config["agent_control"]
        retry = ac["retry"]
        xml_ac = xml_config.add_element("agent_control")
        xml_retry = xml_ac.add_element("retry")
        cls._add_el(xml_retry, "attempts", retry.get("attempts"))
        cls._add_el(
            xml_retry, "delay_in_seconds", retry.get("delay_in_seconds")
        )
        cls._add_el(
            xml_retry,
            "max_jitter_in_seconds",
            retry.get("max_jitter_in_seconds"),
        )

        # agent_script_executor
        se = config["agent_script_executor"]
        xml_se = xml_config.add_element("agent_script_executor")
        cls._add_el(xml_se, "bulk_size", se.get("bulk_size"))
        cls._add_el(
            xml_se,
            "bulk_throttle_time_in_ms",
            se.get("bulk_throttle_time_in_ms"),
        )
        cls._add_el(xml_se, "indexer_dir_depth", se.get("indexer_dir_depth"))
        sched = se.get("scheduler_cron_time")
        if sched:
            xml_sched = xml_se.add_element("scheduler_cron_time")
            for item in sched:
                xml_sched.add_element("item", str(item))

        # heartbeat
        hb = config["heartbeat"]
        xml_hb = xml_config.add_element("heartbeat")
        cls._add_el(
            xml_hb, "interval_in_seconds", hb.get("interval_in_seconds")
        )
        cls._add_el(
            xml_hb, "miss_until_inactive", hb.get("miss_until_inactive")
        )

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
        config: Optional[Mapping[str, Any]] = None,
        comment: Optional[str] = None,
    ) -> Request:
        """
        Modify multiple agents.

        Args:
            agent_ids: List of agent UUIDs to modify.
            authorized: Whether the agent is authorized.
            config: Nested config, e.g.:
                {
                  "agent_control": {
                    "retry": {
                      "attempts": 6,
                      "delay_in_seconds": 60,
                      "max_jitter_in_seconds": 10,
                    }
                  },
                  "agent_script_executor": {
                      "bulk_size": 2,
                      "bulk_throttle_time_in_ms": 300,
                      "indexer_dir_depth": 100,
                      "scheduler_cron_time": ["0 */12 * * *"],  # str or list[str]
                  },
                  "heartbeat": {
                      "interval_in_seconds": 300,
                      "miss_until_inactive": 1,
                  },
                }
            comment: Optional comment for the change.
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

        if config is not None:
            cls._append_agent_config(cmd, config)

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

    @classmethod
    def modify_agent_control_scan_config(
        cls,
        agent_control_id: EntityID,
        config: Mapping[str, Any],
    ) -> Request:
        """
        Modify agent control scan config.

        Args:
            agent_control_id: The agent control UUID.
            config: Nested config, e.g.:
                {
                  "agent_control": {
                    "retry": {
                      "attempts": 6,
                      "delay_in_seconds": 60,
                      "max_jitter_in_seconds": 10,
                    }
                  },
                  "agent_script_executor": {
                      "bulk_size": 2,
                      "bulk_throttle_time_in_ms": 300,
                      "indexer_dir_depth": 100,
                      "scheduler_cron_time": ["0 */12 * * *"],  # str or list[str]
                  },
                  "heartbeat": {
                      "interval_in_seconds": 300,
                      "miss_until_inactive": 1,
                  },
                }
        """
        if not agent_control_id:
            raise RequiredArgument(
                function=cls.modify_agent_control_scan_config.__name__,
                argument="agent_control_id",
            )
        if not config:
            raise RequiredArgument(
                function=cls.modify_agent_control_scan_config.__name__,
                argument="config",
            )

        cmd = XmlCommand(
            "modify_agent_control_scan_config",
        )
        cmd.set_attribute("agent_control_id", str(agent_control_id))

        cls._append_agent_config(cmd, config)

        return cmd
