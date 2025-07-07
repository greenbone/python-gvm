#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests._entity_id import EntityID
from gvm.utils import to_bool
from gvm.xml import XmlCommand


class AgentInstallers:

    @staticmethod
    def get_agent_installers(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of agent installers

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan agent installers instead
            details: Whether to include extra details like tasks using this
                scanner
        """
        cmd = XmlCommand("get_agent_installers")
        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return cmd

    @classmethod
    def get_agent_installer(cls, agent_installer_id: EntityID) -> Request:
        """Request a single agent installer

        Args:
            agent_installer_id: UUID of an existing agent installer
        """
        if not agent_installer_id:
            raise RequiredArgument(
                function=cls.get_agent_installer.__name__,
                argument="agent_installer_id",
            )

        cmd = XmlCommand("get_agent_installers")
        cmd.set_attribute("agent_installer_id", str(agent_installer_id))

        # for single entity always request all details
        cmd.set_attribute("details", "1")

        return cmd

    @classmethod
    def get_agent_installer_file(cls, agent_installer_id: EntityID) -> Request:
        """Request a single agent installer

        Args:
            agent_installer_id: UUID of an existing agent installer
        """
        if not agent_installer_id:
            raise RequiredArgument(
                function=cls.get_agent_installer.__name__,
                argument="agent_installer_id",
            )

        cmd = XmlCommand("get_agent_installer_file")
        cmd.set_attribute("agent_installer_id", str(agent_installer_id))

        return cmd
