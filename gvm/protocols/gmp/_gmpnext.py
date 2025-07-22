#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.protocols.gmp.requests import EntityID

from .._protocol import T
from ._gmp227 import GMPv227
from .requests.next import AgentGroups, AgentInstallers, Agents, OCIImageTargets


class GMPNext(GMPv227[T]):
    """
    A class implementing the "Next" version of Greenbone Management Protocol (GMP)
    containing features that are not part of the stable release yet.

    These features may change at any time and may not be available in all builds
    of the gvmd back-end.

    Example:

        .. code-block:: python

            from gvm.protocols.gmp.next import GMP

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

    def get_agents(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
    ) -> T:
        """Request a list of agents.

        Args:
            filter_string: Filter term to use for the query.
            filter_id: UUID of an existing filter to use for the query.
            details: Whether to include detailed agent info.
        """
        return self._send_request_and_transform_response(
            Agents.get_agents(
                filter_string=filter_string,
                filter_id=filter_id,
                details=details,
            )
        )

    def modify_agents(
        self,
        agent_ids: list[EntityID],
        *,
        authorized: Optional[bool] = None,
        min_interval: Optional[int] = None,
        heartbeat_interval: Optional[int] = None,
        schedule: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> T:
        """Modify multiple agents

        Args:
            agent_ids: List of agent UUIDs to modify
            authorized: Whether the agent is authorized
            min_interval: Minimum scan interval
            heartbeat_interval: Interval for sending heartbeats
            schedule: Cron-style schedule for agent
            comment: Comment for the agents
        """
        return self._send_request_and_transform_response(
            Agents.modify_agents(
                agent_ids=agent_ids,
                authorized=authorized,
                min_interval=min_interval,
                heartbeat_interval=heartbeat_interval,
                schedule=schedule,
                comment=comment,
            )
        )

    def delete_agents(self, agent_ids: list[EntityID]) -> T:
        """Delete multiple agents

        Args:
            agent_ids: List of agent UUIDs to delete
        """
        return self._send_request_and_transform_response(
            Agents.delete_agents(agent_ids=agent_ids)
        )

    def get_agent_groups(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
    ) -> T:
        """Request a list of agent groups.

        Args:
            filter_string: Filter expression to use.
            filter_id: UUID of a predefined filter.
            trash: If True, return trashed agent groups.

        Returns:
            Request object to fetch agent groups.
        """
        return self._send_request_and_transform_response(
            AgentGroups.get_agent_groups(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
            )
        )

    def get_agent_group(self, agent_group_id: EntityID) -> T:
        """Request a single agent group by ID.

        Args:
            agent_group_id: UUID of the agent group.

        Raises:
            RequiredArgument: If agent_group_id is not provided.

        Returns:
            Request object to fetch the specific agent group.
        """
        return self._send_request_and_transform_response(
            AgentGroups.get_agent_group(
                agent_group_id=agent_group_id,
            )
        )

    def create_agent_group(
        self,
        name: str,
        agent_ids: list[str],
        *,
        comment: Optional[str] = None,
    ) -> T:
        """Create a new agent group.

        Args:
            name: Name of the new agent group.
            agent_ids: List of agent UUIDs to include in the group (required).
            comment: Optional comment for the group.

        Raises:
            RequiredArgument: If name or agent_ids is not provided.
        """
        return self._send_request_and_transform_response(
            AgentGroups.create_agent_group(
                name=name,
                comment=comment,
                agent_ids=agent_ids,
            )
        )

    def modify_agent_group(
        self,
        agent_group_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        agent_ids: Optional[list[str]] = None,
    ) -> T:
        """Modify an existing agent group.

        Args:
            agent_group_id: UUID of the group to modify.
            name: Optional new name for the group.
            comment: Optional comment for the group.
            agent_ids: Optional list of agent UUIDs to set for the group.

        Raises:
            RequiredArgument: If agent_group_id is not provided.
        """
        return self._send_request_and_transform_response(
            AgentGroups.modify_agent_group(
                agent_group_id=agent_group_id,
                name=name,
                comment=comment,
                agent_ids=agent_ids,
            )
        )

    def delete_agent_group(
        self,
        agent_group_id: EntityID,
        ultimate: bool = False,
    ) -> T:
        """Delete an existing agent group.

        Args:
            agent_group_id: UUID of the group to delete.
            ultimate: Whether to permanently delete or move to trashcan.

        Raises:
            RequiredArgument: If agent_group_id is not provided.
        """
        return self._send_request_and_transform_response(
            AgentGroups.delete_agent_group(
                agent_group_id=agent_group_id,
                ultimate=ultimate,
            )
        )

    def clone_agent_group(
        self,
        agent_group_id: EntityID,
    ) -> T:
        """Clone an existing agent group

        Args:
            agent_group_id: UUID of an existing agent group to clone from

        Returns:
            Request: GMP command to create a new agent group based on a copy
        """
        return self._send_request_and_transform_response(
            AgentGroups.clone_agent_group(agent_group_id)
        )

    def create_oci_image_target(
        self,
        name: str,
        image_references: list[str],
        *,
        comment: Optional[str] = None,
        credential_id: Optional[EntityID] = None,
    ) -> T:
        """Create a new OCI image target

        Args:
            name: Name of the OCI image target
            image_references: List of OCI image URLs to scan
            comment: Comment for the target
            credential_id: UUID of a credential to use on target
        """
        return self._send_request_and_transform_response(
            OCIImageTargets.create_oci_image_target(
                name=name,
                image_references=image_references,
                comment=comment,
                credential_id=credential_id,
            )
        )

    def modify_oci_image_target(
        self,
        oci_image_target_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        image_references: Optional[list[str]] = None,
        credential_id: Optional[EntityID] = None,
    ) -> T:
        """Modify an existing OCI image target.

        Args:
            oci_image_target_id: UUID of target to modify.
            comment: Comment on target.
            name: Name of target.
            image_references: List of OCI image URLs to scan.
            credential_id: UUID of credential to use on target.
        """
        return self._send_request_and_transform_response(
            OCIImageTargets.modify_oci_image_target(
                oci_image_target_id,
                name=name,
                comment=comment,
                image_references=image_references,
                credential_id=credential_id,
            )
        )

    def clone_oci_image_target(self, oci_image_target_id: EntityID) -> T:
        """Clone an existing OCI image target.

        Args:
            oci_image_target_id: UUID of an existing OCI image target to clone.
        """
        return self._send_request_and_transform_response(
            OCIImageTargets.clone_oci_image_target(oci_image_target_id)
        )

    def delete_oci_image_target(
        self, oci_image_target_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Delete an existing OCI image target.

        Args:
            oci_image_target_id: UUID of an existing OCI image target to delete.
            ultimate: Whether to remove entirely or to the trashcan.
        """
        return self._send_request_and_transform_response(
            OCIImageTargets.delete_oci_image_target(
                oci_image_target_id, ultimate=ultimate
            )
        )

    def get_oci_image_target(
        self, oci_image_target_id: EntityID, *, tasks: Optional[bool] = None
    ) -> T:
        """Request a single OCI image target.

        Args:
            oci_image_target_id: UUID of the OCI image target to request.
            tasks: Whether to include list of tasks that use the target
        """
        return self._send_request_and_transform_response(
            OCIImageTargets.get_oci_image_target(
                oci_image_target_id, tasks=tasks
            )
        )

    def get_oci_image_targets(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> T:
        """Request a list of OCI image targets.

        Args:
            filter_string: Filter term to use for the query.
            filter_id: UUID of an existing filter to use for the query.
            trash: Whether to include targets in the trashcan.
            tasks: Whether to include list of tasks that use the target.
        """
        return self._send_request_and_transform_response(
            OCIImageTargets.get_oci_image_targets(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
                tasks=tasks,
            )
        )
