#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Mapping, Optional, Sequence, Union

from gvm.protocols.gmp.requests import EntityID

from ...utils import SupportsStr
from .._protocol import T
from ._gmp227 import GMPv227
from .requests.next import (
    AgentGroups,
    AgentInstallers,
    Agents,
    Credentials,
    CredentialStoreCredentialType,
    CredentialStores,
    OCIImageTargets,
    Tasks,
)
from .requests.v224 import HostsOrdering


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
        update_to_latest: Optional[bool] = None,
        config: Optional[Mapping[str, Any]] = None,
        comment: Optional[str] = None,
    ) -> T:
        """
        Modify multiple agents.

        Args:
            agent_ids: List of agent UUIDs to modify.
            authorized: Whether the agent is authorized.
            update_to_latest: Whether the agent is allowed to update to latest automatically.
            config: Nested config for Agent Controller.
            comment: Optional comment for the change.
        """
        return self._send_request_and_transform_response(
            Agents.modify_agents(
                agent_ids=agent_ids,
                authorized=authorized,
                update_to_latest=update_to_latest,
                config=config,
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

    def modify_agent_control_scan_config(
        self,
        agent_control_id: EntityID,
        config: Mapping[str, Any],
    ) -> T:
        """
        Modify agent control scan config.

        Args:
            agent_control_id: The agent control UUID.
            config: Nested config for Agent Controller.
        """
        return self._send_request_and_transform_response(
            Agents.modify_agent_control_scan_config(
                agent_control_id=agent_control_id,
                config=config,
            )
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

    def create_credential_store_credential(
        self,
        name: str,
        credential_type: Union[CredentialStoreCredentialType, str],
        *,
        comment: Optional[str] = None,
        credential_store_id: Optional[EntityID] = None,
        vault_id: Optional[str] = None,
        host_identifier: Optional[str] = None,
    ) -> T:
        """Create a new credential store type credential

        Args:
            name: Name of the credential
            credential_type: Type of the credential
            comment: Optional comment for the credential object
            credential_store_id: Optional credential store id to fetch the credential from
            vault_id: Vault id used to fetch the credential from credential store
            host_identifier: Host identifier used to fetch the credential from credential store
        """
        return self._send_request_and_transform_response(
            Credentials.create_credential_store_credential(
                name=name,
                credential_type=credential_type,
                comment=comment,
                credential_store_id=credential_store_id,
                vault_id=vault_id,
                host_identifier=host_identifier,
            )
        )

    def modify_credential_store_credential(
        self,
        credential_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        credential_store_id: Optional[EntityID] = None,
        vault_id: Optional[str] = None,
        host_identifier: Optional[str] = None,
    ) -> T:
        """Modify an existing credential stored in a credential store

        Args:
            credential_id: UUID of the credential to modify
            name: Name of the credential
            comment: Optional comment for the credential object
            credential_store_id: Optional credential store id to fetch the credential from
            vault_id: Vault id used to fetch the credential from credential store
            host_identifier: Host identifier used to fetch the credential from credential store
        """
        return self._send_request_and_transform_response(
            Credentials.modify_credential_store_credential(
                credential_id=credential_id,
                name=name,
                comment=comment,
                credential_store_id=credential_store_id,
                vault_id=vault_id,
                host_identifier=host_identifier,
            )
        )

    def get_credential_store(
        self,
        credential_store_id: EntityID,
        *,
        details: Optional[bool] = None,
    ) -> T:
        """Request a credential store

        Args:
            credential_store_id: ID of credential store to fetch
            details: True to request all details
        """
        return self._send_request_and_transform_response(
            CredentialStores.get_credential_store(
                credential_store_id=credential_store_id,
                details=details,
            )
        )

    def get_credential_stores(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
    ) -> T:
        """Request a list of credential stores

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: True to request all details
        """
        return self._send_request_and_transform_response(
            CredentialStores.get_credential_stores(
                filter_string=filter_string,
                filter_id=filter_id,
                details=details,
            )
        )

    def modify_credential_store(
        self,
        credential_store_id: EntityID,
        *,
        active: Optional[bool] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        path: Optional[str] = None,
        app_id: Optional[str] = None,
        client_cert: Optional[str] = None,
        client_key: Optional[str] = None,
        client_pkcs12_file: Optional[str] = None,
        passphrase: Optional[str] = None,
        server_ca_cert: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> T:
        """Modify an existing credential store

        Args:
            credential_store_id: ID of credential store to fetch
            active: Whether the credential store is active
            host: The host to use for reaching the credential store
            port: The port to use for reaching the credential store
            path: The URI path the credential store is using
            app_id: Depends on the credential store used. Usually called the same in the credential store
            client_cert: The client certificate to use for authorization, as a plain string
            client_key: The client key to use for authorization, as a plain string
            client_pkcs12_file: The pkcs12 file contents to use for authorization, as a plain string
                (alternative to using client_cert and client_key)
            passphrase: The passphrase to use to decrypt client_pkcs12_file or client_key file
            server_ca_cert: The server certificate, so the credential store can be trusted
            comment: An optional comment to store alongside the credential store
        """
        return self._send_request_and_transform_response(
            CredentialStores.modify_credential_store(
                credential_store_id=credential_store_id,
                active=active,
                host=host,
                port=port,
                path=path,
                app_id=app_id,
                client_cert=client_cert,
                client_key=client_key,
                client_pkcs12_file=client_pkcs12_file,
                passphrase=passphrase,
                server_ca_cert=server_ca_cert,
                comment=comment,
            )
        )

    def verify_credential_store(
        self,
        credential_store_id: EntityID,
    ) -> T:
        """Verify that the connection to an existing credential store works

        Args:
            credential_store_id: The uuid of the credential store to verify
        """
        return self._send_request_and_transform_response(
            CredentialStores.verify_credential_store(
                credential_store_id=credential_store_id,
            )
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

    def clone_task(self, task_id: EntityID) -> T:
        """Clone an existing task

        Args:
            task_id: UUID of existing task to clone from
        """
        return self._send_request_and_transform_response(
            Tasks.clone_task(task_id)
        )

    def create_agent_group_task(
        self,
        name: str,
        agent_group_id: EntityID,
        scanner_id: EntityID,
        *,
        comment: Optional[str] = None,
        alterable: Optional[bool] = None,
        schedule_id: Optional[EntityID] = None,
        alert_ids: Optional[Sequence[EntityID]] = None,
        schedule_periods: Optional[int] = None,
        observers: Optional[Sequence[str]] = None,
        preferences: Optional[Mapping[str, SupportsStr]] = None,
    ) -> T:
        """Create a new scan task using an agent group.

        Args:
            name: Name of the new task.
            agent_group_id: UUID of the agent group to be scanned.
            scanner_id: UUID of scanner to use for scanning the agents.
            comment: Optional comment for the task.
            alterable: Whether the task should be alterable.
            alert_ids: List of UUIDs for alerts to be applied to the task.
            schedule_id: UUID of a schedule when the task should be run.
            schedule_periods: Limit to number of scheduled runs, 0 for unlimited.
            observers: List of usernames or IDs allowed to observe the task.
            preferences: Scanner preferences as name/value pairs.
        """
        return self._send_request_and_transform_response(
            Tasks.create_agent_group_task(
                name=name,
                agent_group_id=agent_group_id,
                scanner_id=scanner_id,
                comment=comment,
                alterable=alterable,
                schedule_id=schedule_id,
                alert_ids=alert_ids,
                schedule_periods=schedule_periods,
                observers=observers,
                preferences=preferences,
            )
        )

    def create_container_image_task(
        self,
        name: str,
        oci_image_target_id: EntityID,
        scanner_id: EntityID,
        *,
        comment: Optional[str] = None,
        alterable: Optional[bool] = None,
        schedule_id: Optional[EntityID] = None,
        alert_ids: Optional[Sequence[EntityID]] = None,
        schedule_periods: Optional[int] = None,
        observers: Optional[Sequence[str]] = None,
        preferences: Optional[Mapping[str, SupportsStr]] = None,
    ) -> T:
        """Create a new scan task using an OCI image target.

        Args:
            name: Name of the new task.
            oci_image_target_id: UUID of the OCI image target to be scanned.
            scanner_id: UUID of scanner to use for scanning the agents.
            comment: Optional comment for the task.
            alterable: Whether the task should be alterable.
            alert_ids: List of UUIDs for alerts to be applied to the task.
            schedule_id: UUID of a schedule when the task should be run.
            schedule_periods: Limit to number of scheduled runs, 0 for unlimited.
            observers: List of usernames or IDs allowed to observe the task.
            preferences: Scanner preferences as name/value pairs.
        """
        return self._send_request_and_transform_response(
            Tasks.create_container_image_task(
                name=name,
                oci_image_target_id=oci_image_target_id,
                scanner_id=scanner_id,
                comment=comment,
                alterable=alterable,
                schedule_id=schedule_id,
                alert_ids=alert_ids,
                schedule_periods=schedule_periods,
                observers=observers,
                preferences=preferences,
            )
        )

    def create_import_task(
        self, name: str, *, comment: Optional[str] = None
    ) -> T:
        """Create a new import task

        An import task is a "meta" task to import and view reports from other
        systems.

        Args:
            name: Name of the task
            comment: Comment for the task
        """
        return self._send_request_and_transform_response(
            Tasks.create_import_task(name=name, comment=comment)
        )

    def create_container_task(
        self, name: str, *, comment: Optional[str] = None
    ) -> T:
        """[DEPRECATED] Use create_import_task instead.

        This method will be removed in a future version.
        """
        return self._send_request_and_transform_response(
            Tasks.create_container_task(name=name, comment=comment)
        )

    def create_task(
        self,
        name: str,
        config_id: EntityID,
        target_id: EntityID,
        scanner_id: EntityID,
        *,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[EntityID] = None,
        alert_ids: Optional[Sequence[EntityID]] = None,
        comment: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        observers: Optional[Sequence[str]] = None,
        preferences: Optional[Mapping[str, SupportsStr]] = None,
    ) -> T:
        """Create a new scan task

        Args:
            name: Name of the new task
            config_id: UUID of config to use by the task
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: Comment for the task
            alterable: Whether the task should be alterable
            alert_ids: List of UUIDs for alerts to be applied to the task
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the task should be run.
            schedule_periods: A limit to the number of times the task will be
                scheduled, or 0 for no limit
            observers: List of names or ids of users which should be allowed to
                observe this task
            preferences: Name/Value pairs of scanner preferences.
        """
        return self._send_request_and_transform_response(
            Tasks.create_task(
                name=name,
                config_id=config_id,
                target_id=target_id,
                scanner_id=scanner_id,
                alterable=alterable,
                hosts_ordering=hosts_ordering,
                schedule_id=schedule_id,
                alert_ids=alert_ids,
                comment=comment,
                schedule_periods=schedule_periods,
                observers=observers,
                preferences=preferences,
            )
        )

    def delete_task(
        self, task_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Deletes an existing task

        Args:
            task_id: UUID of the task to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_request_and_transform_response(
            Tasks.delete_task(task_id=task_id, ultimate=ultimate)
        )

    def get_tasks(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        schedules_only: Optional[bool] = None,
        ignore_pagination: Optional[bool] = None,
    ) -> T:
        """Request a list of tasks

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan tasks instead
            details: Whether to include full task details
            schedules_only: Whether to only include id, name and schedule
                details
            ignore_pagination: Whether to ignore pagination settings (filter
                terms "first" and "rows"). Default is False.
        """
        return self._send_request_and_transform_response(
            Tasks.get_tasks(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
                details=details,
                schedules_only=schedules_only,
                ignore_pagination=ignore_pagination,
            )
        )

    def get_task(self, task_id: EntityID) -> T:
        """Request a single task

        Args:
            task_id: UUID of an existing task
        """
        return self._send_request_and_transform_response(
            Tasks.get_task(task_id=task_id)
        )

    def modify_task(
        self,
        task_id: EntityID,
        *,
        name: Optional[str] = None,
        config_id: Optional[EntityID] = None,
        target_id: Optional[EntityID] = None,
        scanner_id: Optional[EntityID] = None,
        agent_group_id: Optional[EntityID] = None,
        oci_image_target_id: Optional[EntityID] = None,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[EntityID] = None,
        schedule_periods: Optional[int] = None,
        comment: Optional[str] = None,
        alert_ids: Optional[Sequence[EntityID]] = None,
        observers: Optional[Sequence[str]] = None,
        preferences: Optional[Mapping[str, SupportsStr]] = None,
    ) -> T:
        """Modifies an existing task.

        Args:
            task_id: UUID of task to modify.
            name: The name of the task.
            config_id: UUID of scan config to use by the task
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            agent_group_id: UUID of agent group to use for scanning
            oci_image_target_id: UUID of the OCI Image target to be scanned.
            comment: The comment on the task.
            alert_ids: List of UUIDs for alerts to be applied to the task
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the task should be run.
            schedule_periods: A limit to the number of times the task will be
                scheduled, or 0 for no limit.
            observers: List of names or ids of users which should be allowed to
                observe this task
            preferences: Name/Value pairs of scanner preferences.
        """
        return self._send_request_and_transform_response(
            Tasks.modify_task(
                task_id=task_id,
                name=name,
                config_id=config_id,
                target_id=target_id,
                scanner_id=scanner_id,
                agent_group_id=agent_group_id,
                oci_image_target_id=oci_image_target_id,
                alterable=alterable,
                hosts_ordering=hosts_ordering,
                schedule_id=schedule_id,
                alert_ids=alert_ids,
                comment=comment,
                schedule_periods=schedule_periods,
                observers=observers,
                preferences=preferences,
            )
        )

    def move_task(
        self, task_id: EntityID, *, slave_id: Optional[EntityID] = None
    ) -> T:
        """Move an existing task to another GMP slave scanner or the master

        Args:
            task_id: UUID of the task to be moved
            slave_id: UUID of the sensor to reassign the task to, empty for master.
        """
        return self._send_request_and_transform_response(
            Tasks.move_task(
                task_id=task_id,
                slave_id=slave_id,
            )
        )

    def start_task(self, task_id: EntityID) -> T:
        """Start an existing task

        Args:
            task_id: UUID of the task to be started
        """
        return self._send_request_and_transform_response(
            Tasks.start_task(task_id=task_id)
        )

    def resume_task(self, task_id: EntityID) -> T:
        """Resume an existing stopped task

        Args:
            task_id: UUID of the task to be resumed
        """
        return self._send_request_and_transform_response(
            Tasks.resume_task(task_id=task_id)
        )

    def stop_task(self, task_id: EntityID) -> T:
        """Stop an existing running task

        Args:
            task_id: UUID of the task to be stopped
        """
        return self._send_request_and_transform_response(
            Tasks.stop_task(task_id=task_id)
        )
