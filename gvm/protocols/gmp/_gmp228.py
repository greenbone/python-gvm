#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.protocols.gmp.requests import EntityID

from .._protocol import T
from ._gmp227 import GMPv227
from .requests.v228 import AgentInstallers


class GMPv228(GMPv227[T]):
    """
    A class implementing the Greenbone Management Protocol (GMP) version 22.8

    Example:

        .. code-block:: python

            from gvm.protocols.gmp import GMPv228 as GMP

            with GMP(connection) as gmp:
                resp = gmp.get_tasks()
    """

    @staticmethod
    def get_protocol_version() -> tuple[int, int]:
        return (22, 8)

    def get_agent_installers(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> T:
        """Request a list of agent installers

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan agent installers instead
            details: Whether to include extra details like tasks using this
                scanner
        """
        return self._send_request_and_transform_response(
            AgentInstallers.get_agent_installers(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
                details=details,
            )
        )

    def get_agent_installer(self, agent_installer_id: EntityID) -> T:
        """Request a single agent installer

        Args:
            agent_installer_id: UUID of an existing agent installer
        """
        return self._send_request_and_transform_response(
            AgentInstallers.get_agent_installer(agent_installer_id)
        )

    def get_agent_installer_file(self, agent_installer_id: EntityID) -> T:
        """Request a single agent installer file

        Args:
            agent_installer_id: UUID of an existing agent installer
        """
        return self._send_request_and_transform_response(
            AgentInstallers.get_agent_installer_file(agent_installer_id)
        )
