# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Iterable, Optional, Sequence, Union

from .._protocol import GvmProtocol, T
from .requests import (
    Aggregates,
    AggregateStatistic,
    AlertCondition,
    AlertEvent,
    AlertMethod,
    Alerts,
    AliveTest,
    Audits,
    Authentication,
    CredentialFormat,
    Credentials,
    CredentialType,
    EntityID,
    EntityType,
    Feed,
    FeedType,
    Filters,
    FilterType,
    Groups,
    Help,
    HelpFormat,
    Hosts,
    HostsOrdering,
    Notes,
    OperatingSystems,
    Overrides,
    Permissions,
    PermissionSubjectType,
    Policies,
    PortLists,
    PortRangeType,
    ReportFormatType,
    Reports,
    ScanConfigs,
    Scanners,
    ScannerType,
    Severity,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
    SortOrder,
    SystemReports,
    Targets,
    TrashCan,
    UserAuthType,
    Users,
    UserSettings,
    Version,
)


class GMPv224(GvmProtocol[T]):
    _authenticated = False

    @staticmethod
    def get_protocol_version() -> tuple[int, int]:
        """
        Return the supported GMP version as major, minor version tuple
        """
        return (22, 4)

    def is_authenticated(self) -> bool:
        """Checks if the user is authenticated

        If the user is authenticated privileged GMP commands like get_tasks
        may be send to gvmd.

        Returns:
            bool: True if an authenticated connection to gvmd has been
            established.
        """
        return self._authenticated

    def authenticate(self, username: str, password: str) -> T:
        """Authenticate to gvmd.

        The generated authenticate command will be send to server.
        Afterwards the response is read, transformed and returned.

        Args:
            username: Username
            password: Password
        """
        response = self._send_command(
            Authentication.authenticate(username=username, password=password)
        )

        if response.is_success:
            self._authenticated = True

        return self._transform(response)

    def describe_auth(self) -> T:
        """Describe authentication methods

        Returns a list of all used authentication methods if such a list is
        available.
        """
        return self._send_and_transform_command(Authentication.describe_auth())

    def modify_auth(
        self, group_name: str, auth_conf_settings: dict[str, str]
    ) -> T:
        """Modifies an existing auth.

        Args:
            group_name: Name of the group to be modified.
            auth_conf_settings: The new auth config.
        """
        return self._send_and_transform_command(
            Authentication.modify_auth(group_name, auth_conf_settings)
        )

    def get_version(self) -> T:
        """Get the Greenbone Vulnerability Management Protocol (GMP) version
        used by the remote gvmd.
        """
        return self._send_and_transform_command(Version.get_version())

    def clone_port_list(self, port_list_id: EntityID) -> T:
        """Clone an existing port list

        Args:
            port_list_id: UUID of an existing port list to clone from
        """
        return self._send_and_transform_command(
            PortLists.clone_port_list(port_list_id)
        )

    def create_port_list(
        self, name: str, port_range: str, *, comment: Optional[str] = None
    ) -> T:
        """Create a new port list

        Args:
            name: Name of the new port list
            port_range: Port list ranges e.g. `"T: 1-1234"` for tcp port
                1 - 1234
            comment: Comment for the port list
        """
        return self._send_and_transform_command(
            PortLists.create_port_list(name, port_range, comment=comment)
        )

    def create_port_range(
        self,
        port_list_id: EntityID,
        start: int,
        end: int,
        port_range_type: Union[str, PortRangeType],
        *,
        comment: Optional[str] = None,
    ) -> T:
        """Create new port range

        Args:
            port_list_id: UUID of the port list to which to add the range
            start: The first port in the range
            end: The last port in the range
            port_range_type: The type of the ports: TCP, UDP, ...
            comment: Comment for the port range
        """
        return self._send_and_transform_command(
            PortLists.create_port_range(
                port_list_id, start, end, port_range_type, comment=comment
            )
        )

    def delete_port_list(
        self, port_list_id: EntityID, *, ultimate: bool = False
    ) -> T:
        """Delete an existing port list

        Args:
            port_list_id: UUID of the port list to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_and_transform_command(
            PortLists.delete_port_list(port_list_id, ultimate=ultimate)
        )

    def delete_port_range(self, port_range_id: EntityID) -> T:
        """Delete an existing port range

        Args:
            port_range_id: UUID of the port range to be deleted.
        """
        return self._send_and_transform_command(
            PortLists.delete_port_range(port_range_id)
        )

    def get_port_lists(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
        targets: Optional[bool] = None,
        trash: Optional[bool] = None,
    ) -> T:
        """Request a list of port lists

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include full port list details
            targets: Whether to include targets using this port list
            trash: Whether to get port lists in the trashcan instead
        """
        return self._send_and_transform_command(
            PortLists.get_port_lists(
                filter_string=filter_string,
                filter_id=filter_id,
                details=details,
                targets=targets,
                trash=trash,
            )
        )

    def get_port_list(self, port_list_id: EntityID) -> T:
        """Request a single port list

        Args:
            port_list_id: UUID of an existing port list
        """
        return self._send_and_transform_command(
            PortLists.get_port_list(port_list_id)
        )

    def modify_port_list(
        self,
        port_list_id: EntityID,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
    ) -> T:
        """Modify an existing port list.

        Args:
            port_list_id: UUID of port list to modify.
            name: Name of port list.
            comment: Comment on port list.
        """
        return self._send_and_transform_command(
            PortLists.modify_port_list(port_list_id, comment=comment, name=name)
        )

    def get_aggregates(
        self,
        resource_type: Union[EntityType, str],
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        sort_criteria: Optional[
            Iterable[dict[str, Union[str, SortOrder, AggregateStatistic]]]
        ] = None,
        data_columns: Optional[Iterable[str]] = None,
        group_column: Optional[str] = None,
        subgroup_column: Optional[str] = None,
        text_columns: Optional[Iterable[str]] = None,
        first_group: Optional[int] = None,
        max_groups: Optional[int] = None,
        mode: Optional[int] = None,
        **kwargs,
    ) -> T:
        """Request aggregated information on a resource / entity type

        Additional arguments can be set via the kwargs parameter for backward
        compatibility with older versions of python-gvm, but are not validated.

        Args:
            resource_type: The entity type to gather data from
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            sort_criteria: List of sort criteria (dicts that can contain
                a field, stat and order)
            data_columns: List of fields to aggregate data from
            group_column: The field to group the entities by
            subgroup_column: The field to further group the entities
                inside groups by
            text_columns: List of simple text columns which no statistics
                are calculated for
            first_group: The index of the first aggregate group to return
            max_groups: The maximum number of aggregate groups to return,
                -1 for all
            mode: Special mode for aggregation
        """
        return self._send_and_transform_command(
            Aggregates.get_aggregates(
                resource_type,
                filter_string=filter_string,
                filter_id=filter_id,
                sort_criteria=sort_criteria,
                data_columns=data_columns,
                group_column=group_column,
                subgroup_column=subgroup_column,
                text_columns=text_columns,
                first_group=first_group,
                max_groups=max_groups,
                **kwargs,
            )
        )

    def get_feeds(self) -> T:
        """Request the list of feeds"""
        return self._send_and_transform_command(Feed.get_feeds())

    def get_feed(self, feed_type: Union[FeedType, str]) -> T:
        """Request a single feed

        Args:
            feed_type: Type of single feed to get: NVT, CERT or SCAP
        """
        return self._send_and_transform_command(Feed.get_feed(feed_type))

    def help(
        self,
        *,
        help_format: Optional[Union[HelpFormat, str]] = None,
        brief: Optional[bool] = None,
    ) -> T:
        """Get the help text

        Args:
            help_format: Format of of the help:
                "html", "rnc", "text" or "xml
            brief: If True help is brief
        """
        return self._send_and_transform_command(
            Help.help(help_format=help_format, brief=brief)
        )

    def system_reports(
        self,
        *,
        name: Optional[str] = None,
        duration: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        brief: Optional[bool] = None,
        slave_id: Optional[EntityID] = None,
    ) -> T:
        """Request a list of system reports

        Args:
            name: A string describing the required system report
            duration: The number of seconds into the past that the system report
                should include
            start_time: The start of the time interval the system report should
                include in ISO time format
            end_time: The end of the time interval the system report should
                include in ISO time format
            brief: Whether to include the actual system reports
            slave_id: UUID of GMP scanner from which to get the system reports
        """
        return self._send_and_transform_command(
            SystemReports.get_system_reports(
                name=name,
                duration=duration,
                start_time=start_time,
                end_time=end_time,
                brief=brief,
                slave_id=slave_id,
            )
        )

    def empty_trash(self) -> T:
        """Empty the trashcan

        Remove all entities from the trashcan. **Attention:** this command can
        not be reverted
        """
        return self._send_and_transform_command(TrashCan.empty_trashcan())

    def restore_from_trash(self, entity_id: EntityID) -> T:
        """Restore an entity from the trashcan

        Args:
            entity_id: ID of the entity to be restored from the trashcan
        """
        return self._send_and_transform_command(
            TrashCan.restore_from_trashcan(entity_id)
        )

    def get_user_settings(self, *, filter_string: Optional[str] = None) -> T:
        """Request a list of user settings

        Args:
            filter_string: Filter term to use for the query
        """
        return self._send_and_transform_command(
            UserSettings.get_user_settings(filter_string=filter_string)
        )

    def get_user_setting(self, setting_id: EntityID) -> T:
        """Request a single user setting

        Args:
            setting_id: UUID of an existing setting
        """
        return self._send_and_transform_command(
            UserSettings.get_user_setting(setting_id)
        )

    def modify_user_setting(
        self,
        *,
        setting_id: Optional[EntityID] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ) -> T:
        """Modifies an existing user setting.

        Args:
            setting_id: UUID of the setting to be changed.
            name: The name of the setting. Either setting_id or name must be
                passed.
            value: The value of the setting.
        """
        return self._send_and_transform_command(
            UserSettings.modify_user_setting(
                setting_id=setting_id, name=name, value=value
            )
        )

    def clone_scan_config(self, config_id: EntityID) -> T:
        """Clone a scan config from an existing one

        Args:
            config_id: UUID of the existing scan config
        """
        return self._send_and_transform_command(
            ScanConfigs.clone_scan_config(config_id)
        )

    def create_scan_config(
        self,
        config_id: EntityID,
        name: str,
        *,
        comment: Optional[str] = None,
    ) -> T:
        """Create a new scan config

        Args:
            config_id: UUID of the existing scan config
            name: Name of the new scan config
            comment: A comment on the config
        """
        return self._send_and_transform_command(
            ScanConfigs.create_scan_config(config_id, name, comment=comment)
        )

    def delete_scan_config(
        self, config_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Deletes an existing config

        Args:
            config_id: UUID of the config to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_and_transform_command(
            ScanConfigs.delete_scan_config(config_id, ultimate=ultimate)
        )

    def get_scan_configs(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        families: Optional[bool] = None,
        preferences: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> T:
        """Request a list of scan configs

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scan configs instead
            details: Whether to get config families, preferences, nvt selectors
                and tasks.
            families: Whether to include the families if no details are
                requested
            preferences: Whether to include the preferences if no details are
                requested
            tasks: Whether to get tasks using this config
        """
        return self._send_and_transform_command(
            ScanConfigs.get_scan_configs(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
                details=details,
                families=families,
                preferences=preferences,
                tasks=tasks,
            )
        )

    def get_scan_config(
        self, config_id: EntityID, *, tasks: Optional[bool] = None
    ) -> T:
        """Request a single scan config

        Args:
            config_id: UUID of an existing scan config
            tasks: Whether to get tasks using this config
        """
        return self._send_and_transform_command(
            ScanConfigs.get_scan_config(config_id, tasks=tasks)
        )

    def get_scan_config_preferences(
        self,
        *,
        nvt_oid: Optional[str] = None,
        config_id: Optional[EntityID] = None,
    ) -> T:
        """Request a list of scan_config preferences

        When the command includes a config_id attribute, the preference element
        includes the preference name, type and value, and the NVT to which the
        preference applies.
        If the command includes a config_id and an nvt_oid, the preferences for
        the given nvt in the config will be shown.

        Args:
            nvt_oid: OID of nvt
            config_id: UUID of scan config of which to show preference values
        """
        return self._send_and_transform_command(
            ScanConfigs.get_scan_config_preferences(
                nvt_oid=nvt_oid, config_id=config_id
            )
        )

    def get_scan_config_preference(
        self,
        name: str,
        *,
        nvt_oid: Optional[str] = None,
        config_id: Optional[EntityID] = None,
    ) -> T:
        """Request a nvt preference

        Args:
            name: name of a particular preference
            nvt_oid: OID of nvt
            config_id: UUID of scan config of which to show preference values
        """
        return self._send_and_transform_command(
            ScanConfigs.get_scan_config_preference(
                name, nvt_oid=nvt_oid, config_id=config_id
            )
        )

    def import_scan_config(self, config: str) -> T:
        """Import a scan config from XML

        Args:
            config: Scan Config XML as string to import. This XML must
                contain a :code:`<get_configs_response>` root element.
        """
        return self._send_and_transform_command(
            ScanConfigs.import_scan_config(config)
        )

    def modify_scan_config_set_nvt_preference(
        self,
        config_id: EntityID,
        name: str,
        nvt_oid: str,
        *,
        value: Optional[str] = None,
    ) -> T:
        """Modifies the nvt preferences of an existing scan config.

        Args:
            config_id: UUID of scan config to modify.
            name: Name for nvt preference to change.
            nvt_oid: OID of the NVT associated with preference to modify
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        return self._send_and_transform_command(
            ScanConfigs.modify_scan_config_set_nvt_preference(
                config_id, name, nvt_oid, value=value
            )
        )

    def modify_scan_config_set_name(self, config_id: EntityID, name: str) -> T:
        """Modifies the name of an existing scan config

        Args:
            config_id: UUID of scan config to modify.
            name: New name for the config.
        """
        return self._send_and_transform_command(
            ScanConfigs.modify_scan_config_set_name(config_id, name)
        )

    def modify_scan_config_set_comment(
        self, config_id: EntityID, *, comment: Optional[str] = None
    ) -> T:
        """Modifies the comment of an existing scan config

        Args:
            config_id: UUID of scan config to modify.
            comment: Comment to set on a config. Default is an
                empty comment and the previous comment will be
                removed.
        """
        return self._send_and_transform_command(
            ScanConfigs.modify_scan_config_set_comment(
                config_id, comment=comment
            )
        )

    def modify_scan_config_set_scanner_preference(
        self,
        config_id: EntityID,
        name: str,
        *,
        value: Optional[str] = None,
    ) -> T:
        """Modifies the scanner preferences of an existing scan config

        Args:
            config_id: UUID of scan config to modify.
            name: Name of the scanner preference to change
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        return self._send_and_transform_command(
            ScanConfigs.modify_scan_config_set_scanner_preference(
                config_id, name, value=value
            )
        )

    def modify_scan_config_set_nvt_selection(
        self,
        config_id: EntityID,
        family: str,
        nvt_oids: Union[tuple[str], list[str]],
    ) -> T:
        """Modifies the selected nvts of an existing scan config

        The manager updates the given family in the config to include only the
        given NVTs.

        Arguments:
            config_id: UUID of scan config to modify.
            family: Name of the NVT family to include NVTs from
            nvt_oids: List of NVTs to select for the family.
        """
        return self._send_and_transform_command(
            ScanConfigs.modify_scan_config_set_nvt_selection(
                config_id, family, nvt_oids
            )
        )

    def modify_scan_config_set_family_selection(
        self,
        config_id: EntityID,
        families: list[tuple[str, bool, bool]],
        *,
        auto_add_new_families: Optional[bool] = True,
    ) -> T:
        """
        Selected the NVTs of a scan config at a family level.

        Args:
            config_id: UUID of scan config to modify.
            families: A list of tuples (str, bool, bool):
                str: the name of the NVT family selected,
                bool: add new NVTs  to the family automatically,
                bool: include all NVTs from the family
            auto_add_new_families: Whether new families should be added to the
                scan config automatically. Default: True.
        """
        return self._send_and_transform_command(
            ScanConfigs.modify_scan_config_set_family_selection(
                config_id, families, auto_add_new_families=auto_add_new_families
            )
        )

    def create_scanner(
        self,
        name: str,
        host: str,
        port: Union[str, int],
        scanner_type: ScannerType,
        credential_id: str,
        *,
        ca_pub: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> T:
        """Create a new scanner

        Args:
            name: Name of the new scanner
            host: Hostname or IP address of the scanner
            port: Port of the scanner
            scanner_type: Type of the scanner
            credential_id: UUID of client certificate credential for the
                scanner
            ca_pub: Certificate of CA to verify scanner certificate
            comment: Comment for the scanner
        """
        return self._send_and_transform_command(
            Scanners.create_scanner(
                name,
                host,
                port,
                scanner_type,
                credential_id,
                ca_pub=ca_pub,
                comment=comment,
            )
        )

    def modify_scanner(
        self,
        scanner_id: EntityID,
        *,
        name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        scanner_type: Optional[ScannerType] = None,
        credential_id: Optional[EntityID] = None,
        ca_pub: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> T:
        """Modify an existing scanner

        Args:
            scanner_id: UUID of the scanner to modify
            name: New name of the scanner
            host: New hostname or IP address of the scanner
            port: New port of the scanner
            scanner_type: New type of the scanner
            credential_id: New UUID of client certificate credential for the
                scanner
            ca_pub: New certificate of CA to verify scanner certificate
            comment: New comment for the scanner
        """
        return self._send_and_transform_command(
            Scanners.modify_scanner(
                scanner_id,
                name=name,
                host=host,
                port=port,
                scanner_type=scanner_type,
                credential_id=credential_id,
                ca_pub=ca_pub,
                comment=comment,
            )
        )

    def get_scanners(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> T:
        """Request a list of scanners

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scanners instead
            details: Whether to include extra details like tasks using this
                scanner
        """
        return self._send_and_transform_command(
            Scanners.get_scanners(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
                details=details,
            )
        )

    def get_scanner(self, scanner_id: EntityID) -> T:
        """Request a single scanner

        Args:
            scanner_id: UUID of an existing scanner
        """
        return self._send_and_transform_command(
            Scanners.get_scanner(scanner_id)
        )

    def verify_scanner(self, scanner_id: EntityID) -> T:
        """Verify an existing scanner

        Args:
            scanner_id: UUID of an existing scanner
        """
        return self._send_and_transform_command(
            Scanners.verify_scanner(scanner_id)
        )

    def clone_scanner(self, scanner_id: EntityID) -> T:
        """Clone an existing scanner

        Args:
            scanner_id: UUID of an existing scanner
        """
        return self._send_and_transform_command(
            Scanners.clone_scanner(scanner_id)
        )

    def delete_scanner(
        self, scanner_id: EntityID, ultimate: Optional[bool] = False
    ) -> T:
        """Delete an existing scanner

        Args:
            scanner_id: UUID of an existing scanner
        """
        return self._send_and_transform_command(
            Scanners.delete_scanner(scanner_id, ultimate=ultimate)
        )

    def create_user(
        self,
        name: str,
        *,
        password: Optional[str] = None,
        hosts: Optional[list[str]] = None,
        hosts_allow: Optional[bool] = False,
        role_ids: Optional[list[EntityID]] = None,
    ) -> T:
        """Create a new user

        Args:
            name: Name of the user
            password: Password of the user
            hosts: A list of host addresses (IPs, DNS names)
            hosts_allow: If True allow only access to passed hosts otherwise
                deny access. Default is False for deny hosts.
            role_ids: A list of role UUIDs for the user
        """
        return self._send_and_transform_command(
            Users.create_user(
                name,
                password=password,
                hosts=hosts,
                hosts_allow=hosts_allow,
                role_ids=role_ids,
            )
        )

    def modify_user(
        self,
        user_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        password: Optional[str] = None,
        auth_source: Optional[UserAuthType] = None,
        role_ids: Optional[list[EntityID]] = None,
        hosts: Optional[list[str]] = None,
        hosts_allow: Optional[bool] = False,
        group_ids: Optional[list[EntityID]] = None,
    ) -> T:
        """Modify an existing user.

        Most of the fields need to be supplied
        for changing a single field even if no change is wanted for those.
        Else empty values are inserted for the missing fields instead.

        Args:
            user_id: UUID of the user to be modified.
            name: The new name for the user.
            comment: Comment on the user.
            password: The password for the user.
            auth_source: Source allowed for authentication for this user.
            roles_id: List of roles UUIDs for the user.
            hosts: User access rules: List of hosts.
            hosts_allow: Defines how the hosts list is to be interpreted.
                If False (default) the list is treated as a deny list.
                All hosts are allowed by default except those provided by
                the hosts parameter. If True the list is treated as a
                allow list. All hosts are denied by default except those
                provided by the hosts parameter.
            group_ids: List of group UUIDs for the user.
        """
        return self._send_and_transform_command(
            Users.modify_user(
                user_id,
                name=name,
                comment=comment,
                password=password,
                auth_source=auth_source,
                role_ids=role_ids,
                hosts=hosts,
                hosts_allow=hosts_allow,
                group_ids=group_ids,
            )
        )

    def clone_user(self, user_id: EntityID) -> T:
        """Clone an existing user.

        Args:
            user_id: UUID of the user to be cloned.
        """
        return self._send_and_transform_command(Users.clone_user(user_id))

    def delete_user(
        self,
        user_id: Optional[EntityID] = None,
        *,
        name: Optional[str] = None,
        inheritor_id: Optional[EntityID] = None,
        inheritor_name: Optional[str] = None,
    ) -> T:
        """Delete an existing user

        Either user_id or name must be passed.

        Args:
            user_id: UUID of the task to be deleted.
            name: The name of the user to be deleted.
            inheritor_id: The UUID of the inheriting user or "self". Overrides
                inheritor_name.
            inheritor_name: The name of the inheriting user.
        """
        return self._send_and_transform_command(
            Users.delete_user(
                user_id=user_id,
                name=name,
                inheritor_id=inheritor_id,
                inheritor_name=inheritor_name,
            )
        )

    def get_users(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
    ) -> T:
        """Request a list of users

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
        """
        return self._send_and_transform_command(
            Users.get_users(filter_string=filter_string, filter_id=filter_id)
        )

    def get_user(self, user_id: EntityID) -> T:
        """Request a single user

        Args:
            user_id: UUID of the user to be requested.
        """
        return self._send_and_transform_command(Users.get_user(user_id))

    def create_note(
        self,
        text: str,
        nvt_oid: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[list[str]] = None,
        port: Optional[str] = None,
        result_id: Optional[EntityID] = None,
        severity: Optional[Severity] = None,
        task_id: Optional[EntityID] = None,
    ) -> T:
        """Create a new note

        Args:
            text: Text of the new note
            nvt_id: OID of the nvt to which note applies
            days_active: Days note will be active. -1 on
                always, 0 off
            hosts: A list of host addresses
            port: Port to which the override applies, needs to be a string
                  in the form {number}/{protocol}
            result_id: UUID of a result to which note applies
            severity: Severity to which note applies
            task_id: UUID of task to which note applies
        """
        return self._send_and_transform_command(
            Notes.create_note(
                text,
                nvt_oid,
                days_active=days_active,
                hosts=hosts,
                port=port,
                result_id=result_id,
                severity=severity,
                task_id=task_id,
            )
        )

    def modify_note(
        self,
        note_id: EntityID,
        text: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[list[str]] = None,
        port: Optional[str] = None,
        result_id: Optional[EntityID] = None,
        severity: Optional[Severity] = None,
        task_id: Optional[EntityID] = None,
    ) -> T:
        """Modify a note

        Args:
            note_id: The UUID of the note to modify
            text: Text of the note
            days_active: Days note will be active. -1 on always, 0 off
            hosts: A list of host addresses
            port: Port to which the override applies, needs to be a string
                  in the form {number}/{protocol}
            result_id: UUID of a result to which note applies
            severity: Severity to which note applies
            task_id: UUID of task to which note applies
        """
        return self._send_and_transform_command(
            Notes.modify_note(
                note_id,
                text,
                days_active=days_active,
                hosts=hosts,
                port=port,
                result_id=result_id,
                severity=severity,
                task_id=task_id,
            )
        )

    def clone_note(self, note_id: EntityID) -> T:
        """Clone an existing note

        Args:
            note_id: UUID of an existing note to clone from
        """
        return self._send_and_transform_command(Notes.clone_note(note_id))

    def delete_note(
        self, note_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Delete an existing note

        Args:
            note_id: UUID of the note to be deleted.
            ultimate: Whether to remove entirely or to the trashcan.
        """
        return self._send_and_transform_command(
            Notes.delete_note(note_id, ultimate=ultimate)
        )

    def get_notes(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
        result: Optional[bool] = None,
    ) -> T:
        """Request a list of notes

        Args:
            filter_string: Filter notes by a string
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Add info about connected results and tasks
            result: Return the details of possible connected results.
        """
        return self._send_and_transform_command(
            Notes.get_notes(
                filter_string=filter_string,
                filter_id=filter_id,
                details=details,
                result=result,
            )
        )

    def get_note(self, note_id: EntityID) -> T:
        """Request a single note

        Arguments:
            note_id: UUID of an existing note
        """
        return self._send_and_transform_command(Notes.get_note(note_id))

    def create_override(
        self,
        text: str,
        nvt_oid: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[list[str]] = None,
        port: Optional[str] = None,
        result_id: Optional[EntityID] = None,
        severity: Optional[Severity] = None,
        new_severity: Optional[Severity] = None,
        task_id: Optional[EntityID] = None,
    ) -> T:
        """Create a new override

        Args:
            text: Text of the new override
            nvt_id: OID of the nvt to which override applies
            days_active: Days override will be active. -1 on always, 0 off
            hosts: A list of host addresses
            port: Port to which the override applies, needs to be a string
                  in the form {number}/{protocol}
            result_id: UUID of a result to which override applies
            severity: Severity to which override applies
            new_severity: New severity for result
            task_id: UUID of task to which override applies
        """
        return self._send_and_transform_command(
            Overrides.create_override(
                text,
                nvt_oid,
                days_active=days_active,
                hosts=hosts,
                port=port,
                result_id=result_id,
                severity=severity,
                new_severity=new_severity,
                task_id=task_id,
            )
        )

    def modify_override(
        self,
        override_id: EntityID,
        text: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[list[str]] = None,
        port: Optional[str] = None,
        result_id: Optional[EntityID] = None,
        severity: Optional[Severity] = None,
        new_severity: Optional[Severity] = None,
        task_id: Optional[EntityID] = None,
    ) -> T:
        """Modify an existing override.

        Args:
            override_id: UUID of override to modify.
            text: The text of the override.
            days_active: Days override will be active. -1 on always,
                0 off.
            hosts: A list of host addresses
            port: Port to which the override applies, needs to be a string
                  in the form {number}/{protocol}
            result_id: Result to which override applies.
            severity: Severity to which override applies.
            new_severity: New severity score for result.
            task_id: Task to which override applies.
        """
        return self._send_and_transform_command(
            Overrides.modify_override(
                override_id,
                text,
                days_active=days_active,
                hosts=hosts,
                port=port,
                result_id=result_id,
                severity=severity,
                new_severity=new_severity,
                task_id=task_id,
            )
        )

    def clone_override(self, override_id: EntityID) -> T:
        """Clone an existing override

        Args:
            override_id: UUID of an existing override to clone from
        """
        return self._send_and_transform_command(
            Overrides.clone_override(override_id)
        )

    def delete_override(
        self, override_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Delete an existing override

        Args:
            override_id: UUID of an existing override to delete
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_and_transform_command(
            Overrides.delete_override(override_id, ultimate=ultimate)
        )

    def get_overrides(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
        result: Optional[bool] = None,
    ) -> T:
        """Request a list of overrides

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include full details
            result: Whether to include results using the override
        """
        return self._send_and_transform_command(
            Overrides.get_overrides(
                filter_string=filter_string,
                filter_id=filter_id,
                details=details,
                result=result,
            )
        )

    def get_override(self, override_id: EntityID) -> T:
        """Request a single override

        Args:
            override_id: UUID of an existing override
        """
        return self._send_and_transform_command(
            Overrides.get_override(override_id)
        )

    def create_target(
        self,
        name: str,
        *,
        asset_hosts_filter: Optional[str] = None,
        hosts: Optional[list[str]] = None,
        comment: Optional[str] = None,
        exclude_hosts: Optional[list[str]] = None,
        ssh_credential_id: Optional[EntityID] = None,
        ssh_credential_port: Optional[Union[int, str]] = None,
        smb_credential_id: Optional[EntityID] = None,
        esxi_credential_id: Optional[EntityID] = None,
        snmp_credential_id: Optional[EntityID] = None,
        alive_test: Optional[Union[str, AliveTest]] = None,
        allow_simultaneous_ips: Optional[bool] = None,
        reverse_lookup_only: Optional[bool] = None,
        reverse_lookup_unify: Optional[bool] = None,
        port_range: Optional[str] = None,
        port_list_id: Optional[EntityID] = None,
    ) -> T:
        """Create a new target

        Args:
            name: Name of the target
            asset_hosts_filter: Filter to select target host from assets hosts
            hosts: List of hosts addresses to scan
            exclude_hosts: List of hosts addresses to exclude from scan
            comment: Comment for the target
            ssh_credential_id: UUID of a ssh credential to use on target
            ssh_credential_port: The port to use for ssh credential
            smb_credential_id: UUID of a smb credential to use on target
            snmp_credential_id: UUID of a snmp credential to use on target
            esxi_credential_id: UUID of a esxi credential to use on target
            alive_test: Which alive test to use
            allow_simultaneous_ips: Whether to scan multiple IPs of the
                same host simultaneously
            reverse_lookup_only: Whether to scan only hosts that have names
            reverse_lookup_unify: Whether to scan only one IP when multiple IPs
                have the same name.
            port_range: Port range for the target
            port_list_id: UUID of the port list to use on target
        """
        return self._send_and_transform_command(
            Targets.create_target(
                name,
                asset_hosts_filter=asset_hosts_filter,
                hosts=hosts,
                comment=comment,
                exclude_hosts=exclude_hosts,
                ssh_credential_id=ssh_credential_id,
                ssh_credential_port=ssh_credential_port,
                smb_credential_id=smb_credential_id,
                esxi_credential_id=esxi_credential_id,
                snmp_credential_id=snmp_credential_id,
                alive_test=alive_test,
                allow_simultaneous_ips=allow_simultaneous_ips,
                reverse_lookup_only=reverse_lookup_only,
                reverse_lookup_unify=reverse_lookup_unify,
                port_range=port_range,
                port_list_id=port_list_id,
            )
        )

    def modify_target(
        self,
        target_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        hosts: Optional[list[str]] = None,
        exclude_hosts: Optional[list[str]] = None,
        ssh_credential_id: Optional[EntityID] = None,
        ssh_credential_port: Optional[Union[str, int]] = None,
        smb_credential_id: Optional[EntityID] = None,
        esxi_credential_id: Optional[EntityID] = None,
        snmp_credential_id: Optional[EntityID] = None,
        alive_test: Optional[Union[AliveTest, str]] = None,
        allow_simultaneous_ips: Optional[bool] = None,
        reverse_lookup_only: Optional[bool] = None,
        reverse_lookup_unify: Optional[bool] = None,
        port_list_id: Optional[EntityID] = None,
    ) -> T:
        """Modify an existing target.

        Args:
            target_id: UUID of target to modify.
            comment: Comment on target.
            name: Name of target.
            hosts: List of target hosts.
            exclude_hosts: A list of hosts to exclude.
            ssh_credential_id: UUID of SSH credential to use on target.
            ssh_credential_port: The port to use for ssh credential
            smb_credential_id: UUID of SMB credential to use on target.
            esxi_credential_id: UUID of ESXi credential to use on target.
            snmp_credential_id: UUID of SNMP credential to use on target.
            port_list_id: UUID of port list describing ports to scan.
            alive_test: Which alive tests to use.
            allow_simultaneous_ips: Whether to scan multiple IPs of the
                same host simultaneously
            reverse_lookup_only: Whether to scan only hosts that have names.
            reverse_lookup_unify: Whether to scan only one IP when multiple IPs
                have the same name.
        """
        return self._send_and_transform_command(
            Targets.modify_target(
                target_id,
                name=name,
                comment=comment,
                hosts=hosts,
                exclude_hosts=exclude_hosts,
                ssh_credential_id=ssh_credential_id,
                ssh_credential_port=ssh_credential_port,
                smb_credential_id=smb_credential_id,
                esxi_credential_id=esxi_credential_id,
                snmp_credential_id=snmp_credential_id,
                alive_test=alive_test,
                allow_simultaneous_ips=allow_simultaneous_ips,
                reverse_lookup_only=reverse_lookup_only,
                reverse_lookup_unify=reverse_lookup_unify,
                port_list_id=port_list_id,
            )
        )

    def clone_target(self, target_id: EntityID) -> T:
        """Clone an existing target.

        Args:
            target_id: UUID of an existing target to clone.
        """
        return self._send_and_transform_command(Targets.clone_target(target_id))

    def delete_target(
        self, target_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Delete an existing target.

        Args:
            target_id: UUID of an existing target to delete.
            ultimate: Whether to remove entirely or to the trashcan.
        """
        return self._send_and_transform_command(
            Targets.delete_target(target_id, ultimate=ultimate)
        )

    def get_target(
        self, target_id: EntityID, *, tasks: Optional[bool] = None
    ) -> T:
        """Request a single target.

        Args:
            target_id: UUID of the target to request.
            tasks: Whether to include list of tasks that use the target
        """
        return self._send_and_transform_command(
            Targets.get_target(target_id, tasks=tasks)
        )

    def get_targets(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> T:
        """Request a list of targets.

        Args:
            filter_string: Filter term to use for the query.
            filter_id: UUID of an existing filter to use for the query.
            trash: Whether to include targets in the trashcan.
            tasks: Whether to include list of tasks that use the target.
        """
        return self._send_and_transform_command(
            Targets.get_targets(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
                tasks=tasks,
            )
        )

    def create_alert(
        self,
        name: str,
        condition: AlertCondition,
        event: AlertEvent,
        method: AlertMethod,
        *,
        method_data: Optional[dict[str, str]] = None,
        event_data: Optional[dict[str, str]] = None,
        condition_data: Optional[dict[str, str]] = None,
        filter_id: Optional[EntityID] = None,
        comment: Optional[str] = None,
    ) -> T:
        """Create a new alert

        Args:
            name: Name of the new Alert
            condition: The condition that must be satisfied for the alert
                to occur; if the event is either 'Updated SecInfo arrived' or
                'New SecInfo arrived', condition must be 'Always'. Otherwise,
                condition can also be on of 'Severity at least', 'Filter count
                changed' or 'Filter count at least'.
            event: The event that must happen for the alert to occur, one
                of 'Task run status changed', 'Updated SecInfo arrived' or 'New
                SecInfo arrived'
            method: The method by which the user is alerted, one of 'SCP',
                'Send', 'SMB', 'SNMP', 'Syslog' or 'Email'; if the event is
                neither 'Updated SecInfo arrived' nor 'New SecInfo arrived',
                method can also be one of 'Start Task', 'HTTP Get', 'Sourcefire
                Connector' or 'verinice Connector'.
            condition_data: Data that defines the condition
            event_data: Data that defines the event
            method_data: Data that defines the method
            filter_id: Filter to apply when executing alert
            comment: Comment for the alert
        """
        return self._send_and_transform_command(
            Alerts.create_alert(
                name,
                condition,
                event,
                method,
                method_data=method_data,
                event_data=event_data,
                condition_data=condition_data,
                filter_id=filter_id,
                comment=comment,
            )
        )

    def modify_alert(
        self,
        alert_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        event: Optional[Union[AlertEvent, str]] = None,
        event_data: Optional[dict] = None,
        condition: Optional[Union[AlertCondition, str]] = None,
        condition_data: Optional[dict[str, str]] = None,
        method: Optional[Union[AlertMethod, str]] = None,
        method_data: Optional[dict[str, str]] = None,
    ) -> T:
        """Modify an existing alert.

        Args:
            alert_id: UUID of the alert to be modified.
            name: Name of the Alert.
            condition: The condition that must be satisfied for the alert to
                occur. If the event is either 'Updated SecInfo
                arrived' or 'New SecInfo arrived', condition must be 'Always'.
                Otherwise, condition can also be on of 'Severity at least',
                'Filter count changed' or 'Filter count at least'.
            condition_data: Data that defines the condition
            event: The event that must happen for the alert to occur, one of
                'Task run status changed', 'Updated SecInfo arrived' or
                'New SecInfo arrived'
            event_data: Data that defines the event
            method: The method by which the user is alerted, one of 'SCP',
                'Send', 'SMB', 'SNMP', 'Syslog' or 'Email';
                if the event is neither 'Updated SecInfo arrived' nor
                'New SecInfo arrived', method can also be one of 'Start Task',
                'HTTP Get', 'Sourcefire Connector' or 'verinice Connector'.
            method_data: Data that defines the method
            filter_id: Filter to apply when executing alert
            comment: Comment for the alert
        """
        return self._send_and_transform_command(
            Alerts.modify_alert(
                alert_id,
                name=name,
                comment=comment,
                filter_id=filter_id,
                event=event,
                event_data=event_data,
                condition=condition,
                condition_data=condition_data,
                method=method,
                method_data=method_data,
            )
        )

    def clone_alert(self, alert_id: EntityID) -> T:
        """Clone an existing alert

        Args:
            alert_id: UUID of the alert to clone from
        """
        return self._send_and_transform_command(Alerts.clone_alert(alert_id))

    def delete_alert(
        self, alert_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Delete an existing alert

        Args:
            alert_id: UUID of the alert to delete
            ultimate: Whether to remove entirely or to the trashcan.
        """
        return self._send_and_transform_command(
            Alerts.delete_alert(alert_id, ultimate=ultimate)
        )

    def test_alert(self, alert_id: EntityID) -> T:
        """Run an alert

        Invoke a test run of an alert

        Args:
            alert_id: UUID of the alert to be tested
        """
        return self._send_and_transform_command(Alerts.test_alert(alert_id))

    def trigger_alert(
        self,
        alert_id: EntityID,
        report_id: EntityID,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        report_format_id: Optional[Union[EntityID, ReportFormatType]] = None,
        delta_report_id: Optional[EntityID] = None,
    ) -> T:
        """Run an alert by ignoring its event and conditions

        The alert is triggered to run immediately with the provided filtered
        report by ignoring the even and condition settings.

        Args:
            alert_id: UUID of the alert to be run
            report_id: UUID of the report to be provided to the alert
            filter: Filter term to use to filter results in the report
            filter_id: UUID of filter to use to filter results in the report
            report_format_id: UUID of report format to use                              or ReportFormatType (enum)
            delta_report_id: UUID of an existing report to compare report to.
        """
        return self._send_and_transform_command(
            Alerts.trigger_alert(
                alert_id,
                report_id,
                filter_string=filter_string,
                filter_id=filter_id,
                report_format_id=report_format_id,
                delta_report_id=delta_report_id,
            )
        )

    def get_alerts(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> T:
        """Request a list of alerts

        Args:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: True to request the alerts in the trashcan
            tasks: Whether to include the tasks using the alerts
        """
        return self._send_and_transform_command(
            Alerts.get_alerts(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
                tasks=tasks,
            )
        )

    def get_alert(
        self, alert_id: EntityID, *, tasks: Optional[bool] = None
    ) -> T:
        """Request a single alert

        Arguments:
            alert_id: UUID of an existing alert
            tasks: Whether to include the tasks using the alert
        """
        return self._send_and_transform_command(
            Alerts.get_alert(alert_id, tasks=tasks)
        )

    def create_audit(
        self,
        name: str,
        policy_id: EntityID,
        target_id: EntityID,
        scanner_id: EntityID,
        *,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[Union[HostsOrdering, str]] = None,
        schedule_id: Optional[str] = None,
        alert_ids: Optional[list[EntityID]] = None,
        comment: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        observers: Optional[list[EntityID]] = None,
        preferences: Optional[dict[str, str]] = None,
    ) -> T:
        """Create a new audit

        Args:
            name: Name of the new audit
            policy_id: UUID of policy to use by the audit
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: Comment for the audit
            alterable: Whether the task should be alterable
            alert_ids: List of UUIDs for alerts to be applied to the audit
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the audit should be run.
            schedule_periods: A limit to the number of times the audit will be
                scheduled, or 0 for no limit
            observers: List of names or ids of users which should be allowed to
                observe this audit
            preferences: Name/Value pairs of scanner preferences.
        """
        return self._send_and_transform_command(
            Audits.create_audit(
                name,
                policy_id,
                target_id,
                scanner_id,
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

    def modify_audit(
        self,
        audit_id: EntityID,
        *,
        name: Optional[str] = None,
        policy_id: Optional[EntityID] = None,
        target_id: Optional[EntityID] = None,
        scanner_id: Optional[EntityID] = None,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[Union[str, HostsOrdering]] = None,
        schedule_id: Optional[EntityID] = None,
        schedule_periods: Optional[int] = None,
        comment: Optional[str] = None,
        alert_ids: Optional[list[EntityID]] = None,
        observers: Optional[list[EntityID]] = None,
        preferences: Optional[dict[str, str]] = None,
    ) -> T:
        """Modifies an existing audit.

        Args:
            audit_id: UUID of audit to modify.
            name: The name of the audit.
            policy_id: UUID of policy to use by the audit
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: The comment on the audit.
            alert_ids: List of UUIDs for alerts to be applied to the audit
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the audit should be run.
            schedule_periods: A limit to the number of times the audit will be
                scheduled, or 0 for no limit.
            observers: List of names or ids of users which should be allowed to
                observe this audit
            preferences: Name/Value pairs of scanner preferences.
        """
        return self._send_and_transform_command(
            Audits.modify_audit(
                audit_id,
                name=name,
                policy_id=policy_id,
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

    def clone_audit(self, audit_id: EntityID) -> T:
        """Clone an existing audit

        Args:
            audit_id: UUID of the audit to clone
        """
        return self._send_and_transform_command(Audits.clone_audit(audit_id))

    def delete_audit(
        self, audit_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Delete an existing audit

        Args:
            audit_id: UUID of the audit to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_and_transform_command(
            Audits.delete_audit(audit_id, ultimate=ultimate)
        )

    def get_audits(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        schedules_only: Optional[bool] = None,
    ) -> T:
        """Request a list of audits

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan audits instead
            details: Whether to include full audit details
            schedules_only: Whether to only include id, name and schedule
                details
        """
        return self._send_and_transform_command(
            Audits.get_audits(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
                details=details,
                schedules_only=schedules_only,
            )
        )

    def get_audit(self, audit_id: EntityID) -> T:
        """Request a single audit

        Args:
            audit_id: UUID of an existing audit
        """
        return self._send_and_transform_command(Audits.get_audit(audit_id))

    def resume_audit(self, audit_id: EntityID) -> T:
        """Resume an existing stopped audit

        Args:
            audit_id: UUID of the audit to be resumed
        """
        return self._send_and_transform_command(Audits.resume_audit(audit_id))

    def start_audit(self, audit_id: EntityID) -> T:
        """Start an existing audit

        Args:
            audit_id: UUID of the audit to be started
        """
        return self._send_and_transform_command(Audits.start_audit(audit_id))

    def stop_audit(self, audit_id: EntityID) -> T:
        """Stop an existing running audit

        Args:
            audit_id: UUID of the audit to be stopped
        """
        return self._send_and_transform_command(Audits.stop_audit(audit_id))

    def clone_credential(self, credential_id: EntityID) -> T:
        """Clone an existing credential

        Args:
            credential_id: UUID of the credential to clone
        """
        return self._send_and_transform_command(
            Credentials.clone_credential(credential_id)
        )

    def create_credential(
        self,
        name: str,
        credential_type: Union[CredentialType, str],
        *,
        comment: Optional[str] = None,
        allow_insecure: Optional[bool] = None,
        certificate: Optional[str] = None,
        key_phrase: Optional[str] = None,
        private_key: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        auth_algorithm: Optional[Union[SnmpAuthAlgorithm, str]] = None,
        community: Optional[str] = None,
        privacy_algorithm: Optional[Union[SnmpPrivacyAlgorithm, str]] = None,
        privacy_password: Optional[str] = None,
        public_key: Optional[str] = None,
    ) -> T:
        """Create a new credential

        Create a new credential e.g. to be used in the method of an alert.

        Currently the following credential types are supported:

            - Username + Password
            - Username + SSH-Key
            - Client Certificates
            - SNMPv1 or SNMPv2c protocol
            - S/MIME Certificate
            - OpenPGP Key
            - Password only

        Args:
            name: Name of the new credential
            credential_type: The credential type.
            comment: Comment for the credential
            allow_insecure: Whether to allow insecure use of the credential
            certificate: Certificate for the credential.
                Required for client-certificate and smime credential types.
            key_phrase: Key passphrase for the private key.
                Used for the username+ssh-key credential type.
            private_key: Private key to use for login. Required
                for usk credential type. Also used for the cc credential type.
                The supported key types (dsa, rsa, ecdsa, ...) and formats (PEM,
                PKC#12, OpenSSL, ...) depend on your installed GnuTLS version.
            login: Username for the credential. Required for username+password,
                username+ssh-key and snmp credential type.
            password: Password for the credential. Used for username+password
                and snmp credential types.
            community: The SNMP community
            auth_algorithm: The SNMP authentication algorithm. Required for snmp
                credential type.
            privacy_algorithm: The SNMP privacy algorithm
            privacy_password: The SNMP privacy password
            public_key: PGP public key in *armor* plain text format. Required
                for pgp credential type.

        Examples:
            Creating a Username + Password credential

            .. code-block:: python

                gmp.create_credential(
                    name='UP Credential',
                    credential_type=CredentialType.USERNAME_PASSWORD,
                    login='foo',
                    password='bar',
                )

            Creating a Username + SSH Key credential

            .. code-block:: python

                with open('path/to/private-ssh-key') as f:
                    key = f.read()

                gmp.create_credential(
                    name='USK Credential',
                    credential_type=CredentialType.USERNAME_SSH_KEY,
                    login='foo',
                    key_phrase='foobar',
                    private_key=key,
                )

            Creating a PGP credential

            .. note::

                A compatible public pgp key file can be exported with GnuPG via
                ::

                    $ gpg --armor --export alice@cyb.org > alice.asc

            .. code-block:: python

                with open('path/to/pgp.key.asc') as f:
                    key = f.read()

                gmp.create_credential(
                    name='PGP Credential',
                    credential_type=CredentialType.PGP_ENCRYPTION_KEY,
                    public_key=key,
                )

            Creating a S/MIME credential

            .. code-block:: python

                with open('path/to/smime-cert') as f:
                    cert = f.read()

                gmp.create_credential(
                    name='SMIME Credential',
                    credential_type=CredentialType.SMIME_CERTIFICATE,
                    certificate=cert,
                )

            Creating a Password-Only credential

            .. code-block:: python

                gmp.create_credential(
                    name='Password-Only Credential',
                    credential_type=CredentialType.PASSWORD_ONLY,
                    password='foo',
                )
        """
        return self._send_and_transform_command(
            Credentials.create_credential(
                name,
                credential_type,
                comment=comment,
                allow_insecure=allow_insecure,
                certificate=certificate,
                key_phrase=key_phrase,
                private_key=private_key,
                login=login,
                password=password,
                auth_algorithm=auth_algorithm,
                community=community,
                privacy_algorithm=privacy_algorithm,
                privacy_password=privacy_password,
                public_key=public_key,
            )
        )

    def delete_credential(
        self, credential_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Delete an existing credential

        Args:
            credential_id: UUID of the credential to delete
            ultimate: Whether to remove entirely or to the trashcan.
        """
        return self._send_and_transform_command(
            Credentials.delete_credential(credential_id, ultimate=ultimate)
        )

    def get_credentials(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        scanners: Optional[bool] = None,
        trash: Optional[bool] = None,
        targets: Optional[bool] = None,
    ) -> T:
        """Request a list of credentials

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            scanners: Whether to include a list of scanners using the
                credentials
            trash: Whether to get the trashcan credentials instead
            targets: Whether to include a list of targets using the credentials
        """
        return self._send_and_transform_command(
            Credentials.get_credentials(
                filter_string=filter_string,
                filter_id=filter_id,
                scanners=scanners,
                trash=trash,
                targets=targets,
            )
        )

    def get_credential(
        self,
        credential_id: str,
        *,
        scanners: Optional[bool] = None,
        targets: Optional[bool] = None,
        credential_format: Optional[Union[CredentialFormat, str]] = None,
    ) -> T:
        """Request a single credential

        Args:
            credential_id: UUID of an existing credential
            scanners: Whether to include a list of scanners using the
                credentials
            targets: Whether to include a list of targets using the credentials
            credential_format: One of "key", "rpm", "deb", "exe" or "pem"
        """
        return self._send_and_transform_command(
            Credentials.get_credential(
                credential_id,
                scanners=scanners,
                targets=targets,
                credential_format=credential_format,
            )
        )

    def modify_credential(
        self,
        credential_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        allow_insecure: Optional[bool] = None,
        certificate: Optional[str] = None,
        key_phrase: Optional[str] = None,
        private_key: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        auth_algorithm: Optional[Union[SnmpAuthAlgorithm, str]] = None,
        community: Optional[str] = None,
        privacy_algorithm: Optional[Union[SnmpPrivacyAlgorithm, str]] = None,
        privacy_password: Optional[str] = None,
        public_key: Optional[str] = None,
    ) -> T:
        """Modifies an existing credential.

        Args:
            credential_id: UUID of the credential
            name: Name of the credential
            comment: Comment for the credential
            allow_insecure: Whether to allow insecure use of the credential
            certificate: Certificate for the credential
            key_phrase: Key passphrase for the private key
            private_key: Private key to use for login
            login: Username for the credential
            password: Password for the credential
            auth_algorithm: The authentication algorithm for SNMP
            community: The SNMP community
            privacy_algorithm: The privacy algorithm for SNMP
            privacy_password: The SNMP privacy password
            public_key: PGP public key in *armor* plain text format
        """
        return self._send_and_transform_command(
            Credentials.modify_credential(
                credential_id,
                name=name,
                comment=comment,
                allow_insecure=allow_insecure,
                certificate=certificate,
                key_phrase=key_phrase,
                private_key=private_key,
                login=login,
                password=password,
                auth_algorithm=auth_algorithm,
                community=community,
                privacy_algorithm=privacy_algorithm,
                privacy_password=privacy_password,
                public_key=public_key,
            )
        )

    def clone_filter(self, filter_id: EntityID) -> T:
        """Clone a filter

        Args:
            filter_id: ID of the filter to clone
        """
        return self._send_and_transform_command(Filters.clone_filter(filter_id))

    def create_filter(
        self,
        name: str,
        *,
        filter_type: Optional[FilterType] = None,
        comment: Optional[str] = None,
        term: Optional[str] = None,
    ) -> T:
        """Create a new filter

        Args:
            name: Name of the new filter
            filter_type: Filter for entity type
            comment: Comment for the filter
            term: Filter term e.g. 'name=foo'
        """
        return self._send_and_transform_command(
            Filters.create_filter(
                name, filter_type=filter_type, comment=comment, term=term
            )
        )

    def delete_filter(
        self, filter_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Deletes an existing filter

        Args:
            filter_id: UUID of the filter to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_and_transform_command(
            Filters.delete_filter(filter_id, ultimate=ultimate)
        )

    def get_filters(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        alerts: Optional[bool] = None,
    ) -> T:
        """Request a list of filters

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan filters instead
            alerts: Whether to include list of alerts that use the filter.
        """
        return self._send_and_transform_command(
            Filters.get_filters(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
                alerts=alerts,
            )
        )

    def get_filter(
        self, filter_id: EntityID, *, alerts: Optional[bool] = None
    ) -> T:
        """Request a single filter

        Args:
            filter_id: UUID of an existing filter
            alerts: Whether to include list of alerts that use the filter.
        """
        return self._send_and_transform_command(
            Filters.get_filter(filter_id, alerts=alerts)
        )

    def modify_filter(
        self,
        filter_id: EntityID,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        term: Optional[str] = None,
        filter_type: Optional[FilterType] = None,
    ) -> T:
        """Modifies an existing filter.

        Args:
            filter_id: UUID of the filter to be modified
            comment: Comment on filter.
            name: Name of filter.
            term: Filter term.
            filter_type: Resource type filter applies to.
        """
        return self._send_and_transform_command(
            Filters.modify_filter(
                filter_id,
                comment=comment,
                name=name,
                term=term,
                filter_type=filter_type,
            )
        )

    def clone_group(self, group_id: EntityID) -> T:
        """Clone an existing group

        Args:
            group_id: UUID of an existing group to clone from
        """
        return self._send_and_transform_command(Groups.clone_group(group_id))

    def create_group(
        self,
        name: str,
        *,
        comment: Optional[str] = None,
        special: Optional[bool] = False,
        users: Optional[list[str]] = None,
    ) -> T:
        """Create a new group

        Args:
            name: Name of the new group
            comment: Comment for the group
            special: Create permission giving members full access to each
                other's entities
            users: List of user names to be in the group
        """
        return self._send_and_transform_command(
            Groups.create_group(
                name, comment=comment, special=special, users=users
            )
        )

    def delete_group(
        self, group_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Deletes an existing group

        Args:
            group_id: UUID of the group to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_and_transform_command(
            Groups.delete_group(group_id, ultimate=ultimate)
        )

    def get_groups(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
    ) -> T:
        """Request a list of groups

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan groups instead
        """
        return self._send_and_transform_command(
            Groups.get_groups(
                filter_string=filter_string, filter_id=filter_id, trash=trash
            )
        )

    def get_group(self, group_id: EntityID) -> T:
        """Request a single group

        Args:
            group_id: UUID of an existing group
        """
        return self._send_and_transform_command(Groups.get_group(group_id))

    def modify_group(
        self,
        group_id: EntityID,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        users: Optional[list[str]] = None,
    ) -> T:
        """Modifies an existing group.

        Args:
            group_id: UUID of group to modify.
            comment: Comment on group.
            name: Name of group.
            users: List of user names to be in the group
        """
        return self._send_and_transform_command(
            Groups.modify_group(
                group_id, comment=comment, name=name, users=users
            )
        )

    def create_host(self, name: str, *, comment: Optional[str] = None) -> T:
        """Create a new host host

        Args:
            name: Name for the new host host
            comment: Comment for the new host host
        """
        return self._send_and_transform_command(
            Hosts.create_host(name, comment=comment)
        )

    def delete_host(self, host_id: EntityID) -> T:
        """Deletes an existing host

        Args:
            host_id: UUID of the single host to delete.
        """
        return self._send_and_transform_command(Hosts.delete_host(host_id))

    def get_hosts(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
    ) -> T:
        """Request a list of hosts

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include additional information (e.g. tags)
        """
        return self._send_and_transform_command(
            Hosts.get_hosts(
                filter_string=filter_string,
                filter_id=filter_id,
                details=details,
            )
        )

    def get_host(
        self, host_id: EntityID, *, details: Optional[bool] = None
    ) -> T:
        """Request a single host

        Arguments:
            host_id: UUID of an existing host
            details: Whether to include additional information (e.g. tags)
        """
        return self._send_and_transform_command(
            Hosts.get_host(host_id, details=details)
        )

    def modify_host(
        self, host_id: EntityID, *, comment: Optional[str] = None
    ) -> T:
        """Modifies an existing host.

        Args:
            host_id: UUID of the host to be modified.
            comment: Comment for the host. Not passing a comment
                arguments clears the comment for this host.
        """
        return self._send_and_transform_command(
            Hosts.modify_host(host_id, comment=comment)
        )

    def delete_operating_system(
        self,
        operating_system_id: EntityID,
    ) -> T:
        """Deletes an existing operating system

        Args:
            operating_system_id: UUID of the single operating_system to delete.
        """
        return self._send_and_transform_command(
            OperatingSystems.delete_operating_system(operating_system_id)
        )

    def get_operating_systems(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
    ) -> T:
        """Request a list of operating systems

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include additional information (e.g. tags)
        """
        return self._send_and_transform_command(
            OperatingSystems.get_operating_systems(
                filter_string=filter_string,
                filter_id=filter_id,
                details=details,
            )
        )

    def get_operating_system(
        self, operating_system_id: EntityID, *, details: Optional[bool] = None
    ) -> T:
        """Request a single operating system

        Args:
            operating_system_id: UUID of an existing operating_system
            details: Whether to include additional information (e.g. tags)
        """
        return self._send_and_transform_command(
            OperatingSystems.get_operating_system(
                operating_system_id, details=details
            )
        )

    def modify_operating_system(
        self, operating_system_id: EntityID, *, comment: Optional[str] = None
    ) -> T:
        """Modifies an existing operating system.

        Args:
            operating_system_id: UUID of the operating_system to be modified.
            comment: Comment for the operating_system. Not passing a comment
                arguments clears the comment for this operating system.
        """
        return self._send_and_transform_command(
            OperatingSystems.modify_operating_system(
                operating_system_id, comment=comment
            )
        )

    def clone_permission(self, permission_id: EntityID) -> T:
        """Clone an existing permission

        Args:
            permission_id: UUID of an existing permission to clone from
        """
        return self._send_and_transform_command(
            Permissions.clone_permission(permission_id)
        )

    def create_permission(
        self,
        name: str,
        subject_id: EntityID,
        subject_type: Union[PermissionSubjectType, str],
        *,
        resource_id: Optional[str] = None,
        resource_type: Optional[Union[EntityType, str]] = None,
        comment: Optional[str] = None,
    ) -> T:
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
        return self._send_and_transform_command(
            Permissions.create_permission(
                name,
                subject_id,
                subject_type,
                resource_id=resource_id,
                resource_type=resource_type,
                comment=comment,
            )
        )

    def delete_permission(
        self, permission_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Deletes an existing permission

        Args:
            permission_id: UUID of the permission to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_and_transform_command(
            Permissions.delete_permission(permission_id, ultimate=ultimate)
        )

    def get_permissions(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
    ) -> T:
        """Request a list of permissions

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get permissions in the trashcan instead
        """
        return self._send_and_transform_command(
            Permissions.get_permissions(
                filter_string=filter_string, filter_id=filter_id, trash=trash
            )
        )

    def get_permission(self, permission_id: EntityID) -> T:
        """Request a single permission

        Args:
            permission_id: UUID of an existing permission
        """
        return self._send_and_transform_command(
            Permissions.get_permission(permission_id)
        )

    def modify_permission(
        self,
        permission_id: EntityID,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        resource_id: Optional[EntityID] = None,
        resource_type: Optional[Union[EntityType, str]] = None,
        subject_id: Optional[EntityID] = None,
        subject_type: Optional[Union[PermissionSubjectType, str]] = None,
    ) -> T:
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
        return self._send_and_transform_command(
            Permissions.modify_permission(
                permission_id,
                comment=comment,
                name=name,
                resource_id=resource_id,
                resource_type=resource_type,
                subject_id=subject_id,
                subject_type=subject_type,
            )
        )

    def clone_policy(self, policy_id: EntityID) -> T:
        """Clone a policy from an existing one

        Args:
            policy_id: UUID of the existing policy
        """
        return self._send_and_transform_command(
            Policies.clone_policy(policy_id)
        )

    def create_policy(
        self,
        name: str,
        *,
        policy_id: Optional[EntityID] = None,
        comment: Optional[str] = None,
    ) -> T:
        """Create a new policy

        Args:
            name: Name of the new policy
            policy_id: UUID of an existing policy as base. By default the empty
                policy is used.
            comment: A comment on the policy
        """
        return self._send_and_transform_command(
            Policies.create_policy(name, policy_id=policy_id, comment=comment)
        )

    def delete_policy(
        self, policy_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> T:
        """Deletes an existing policy

        Args:
            policy_id: UUID of the policy to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_and_transform_command(
            Policies.delete_policy(policy_id, ultimate=ultimate)
        )

    def get_policies(
        self,
        *,
        audits: Optional[bool] = None,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
        families: Optional[bool] = None,
        preferences: Optional[bool] = None,
        trash: Optional[bool] = None,
    ) -> T:
        """Request a list of policies

        Args:
            audits: Whether to get audits using the policy
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to get  families, preferences, nvt selectors
                and tasks.
            families: Whether to include the families if no details are
                requested
            preferences: Whether to include the preferences if no details are
                requested
            trash: Whether to get the trashcan audits instead
        """
        return self._send_and_transform_command(
            Policies.get_policies(
                audits=audits,
                filter_string=filter_string,
                filter_id=filter_id,
                details=details,
                families=families,
                preferences=preferences,
                trash=trash,
            )
        )

    def get_policy(
        self, policy_id: EntityID, *, audits: Optional[bool] = None
    ) -> T:
        """Request a single policy

        Args:
            policy_id: UUID of an existing policy
            audits: Whether to get audits using this policy
        """
        return self._send_and_transform_command(
            Policies.get_policy(policy_id, audits=audits)
        )

    def import_policy(self, policy: str) -> T:
        """Import a policy from XML

        Args:
            policy: Policy XML as string to import. This XML must
                contain a :code:`<get_configs_response>` root element.
        """
        return self._send_and_transform_command(Policies.import_policy(policy))

    def modify_policy_set_nvt_preference(
        self,
        policy_id: EntityID,
        name: str,
        nvt_oid: str,
        *,
        value: Optional[str] = None,
    ) -> T:
        """Modifies the nvt preferences of an existing policy.

        Args:
            policy_id: UUID of policy to modify.
            name: Name for preference to change.
            nvt_oid: OID of the NVT associated with preference to modify
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        return self._send_and_transform_command(
            Policies.modify_policy_set_nvt_preference(
                policy_id, name, nvt_oid, value=value
            )
        )

    def modify_policy_set_name(self, policy_id: EntityID, name: str) -> T:
        """Modifies the name of an existing policy

        Args:
            policy_id: UUID of policy to modify.
            name: New name for the policy.
        """
        return self._send_and_transform_command(
            Policies.modify_policy_set_name(policy_id, name)
        )

    def modify_policy_set_comment(
        self, policy_id: EntityID, comment: Optional[str] = None
    ) -> T:
        """Modifies the comment of an existing policy

        Args:
            policy_id: UUID of policy to modify.
            comment: Comment to set on a policy. Default is an
                empty comment and the previous comment will be
                removed.
        """
        return self._send_and_transform_command(
            Policies.modify_policy_set_comment(policy_id, comment=comment)
        )

    def modify_policy_set_scanner_preference(
        self, policy_id: EntityID, name: str, *, value: Optional[str] = None
    ) -> T:
        """Modifies the scanner preferences of an existing policy

        Args:
            policy_id: UUID of policy to modify.
            name: Name of the scanner preference to change
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        return self._send_and_transform_command(
            Policies.modify_policy_set_scanner_preference(
                policy_id, name, value=value
            )
        )

    def modify_policy_set_nvt_selection(
        self, policy_id: EntityID, family: str, nvt_oids: Sequence[str]
    ) -> T:
        """Modifies the selected nvts of an existing policy

        The manager updates the given family in the policy to include only the
        given NVTs.

        Args:
            policy_id: UUID of policy to modify.
            family: Name of the NVT family to include NVTs from
            nvt_oids: List of NVTs to select for the family.
        """
        return self._send_and_transform_command(
            Policies.modify_policy_set_nvt_selection(
                policy_id, family, nvt_oids
            )
        )

    def modify_policy_set_family_selection(
        self,
        policy_id: EntityID,
        families: Sequence[tuple[str, bool, bool]],
        *,
        auto_add_new_families: Optional[bool] = True,
    ) -> T:
        """
        Selected the NVTs of a policy at a family level.

        Args:
            policy_id: UUID of policy to modify.
            families: A list of tuples with the first entry being the name
                of the NVT family selected, second entry a boolean indicating
                whether new NVTs should be added to the family automatically,
                and third entry a boolean indicating whether all nvts from
                the family should be included.
            auto_add_new_families: Whether new families should be added to the
                policy automatically. Default: True.
        """
        return self._send_and_transform_command(
            Policies.modify_policy_set_family_selection(
                policy_id, families, auto_add_new_families=auto_add_new_families
            )
        )

    def delete_report(self, report_id: EntityID) -> T:
        """Deletes an existing report

        Args:
            report_id: UUID of the report to be deleted.
        """
        return self._send_and_transform_command(
            Reports.delete_report(report_id)
        )

    def get_report(
        self,
        report_id: EntityID,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        delta_report_id: Optional[EntityID] = None,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        ignore_pagination: Optional[bool] = None,
        details: Optional[bool] = True,
    ) -> T:
        """Request a single report

        Args:
            report_id: UUID of an existing report
            filter_string: Filter term to use to filter results in the report
            filter_id: UUID of filter to use to filter results in the report
            delta_report_id: UUID of an existing report to compare report to.
            report_format_id: UUID of report format to use
                              or ReportFormatType (enum)
            ignore_pagination: Whether to ignore the filter terms "first" and
                "rows".
            details: Request additional report information details
                     defaults to True
        """
        return self._send_and_transform_command(
            Reports.get_report(
                report_id,
                filter_string=filter_string,
                filter_id=filter_id,
                delta_report_id=delta_report_id,
                report_format_id=report_format_id,
                ignore_pagination=ignore_pagination,
                details=details,
            )
        )

    def get_reports(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        note_details: Optional[bool] = None,
        override_details: Optional[bool] = None,
        ignore_pagination: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> T:
        """Request a list of reports

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            note_details: If notes are included, whether to include note details
            override_details: If overrides are included, whether to include
                override details
            ignore_pagination: Whether to ignore the filter terms "first" and
                "rows".
            details: Whether to exclude results
        """
        return self._send_and_transform_command(
            Reports.get_reports(
                filter_string=filter_string,
                filter_id=filter_id,
                note_details=note_details,
                override_details=override_details,
                ignore_pagination=ignore_pagination,
                details=details,
            )
        )

    def import_report(
        self,
        report: str,
        task_id: EntityID,
        *,
        in_assets: Optional[bool] = None,
    ) -> T:
        """Import a Report from XML

        Args:
            report: Report XML as string to import. This XML must contain
                a :code:`<report>` root element.
            task_id: UUID of task to import report to
            in_asset: Whether to create or update assets using the report
        """
        return self._send_and_transform_command(
            Reports.import_report(report, task_id, in_assets=in_assets)
        )
