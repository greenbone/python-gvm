# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Iterable, Optional, Union

from .._protocol import GvmProtocol, T
from .requests import (
    Aggregates,
    AggregateStatistic,
    Authentication,
    EntityID,
    EntityType,
    Feed,
    FeedType,
    Help,
    HelpFormat,
    Notes,
    Overrides,
    PortList,
    PortRangeType,
    ScanConfigs,
    Scanners,
    ScannerType,
    Severity,
    SortOrder,
    SystemReports,
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
            PortList.clone_port_list(port_list_id)
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
            PortList.create_port_list(name, port_range, comment=comment)
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
            PortList.create_port_range(
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
            PortList.delete_port_list(port_list_id, ultimate=ultimate)
        )

    def delete_port_range(self, port_range_id: EntityID) -> T:
        """Delete an existing port range

        Args:
            port_range_id: UUID of the port range to be deleted.
        """
        return self._send_and_transform_command(
            PortList.delete_port_range(port_range_id)
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
            PortList.get_port_lists(
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
            PortList.get_port_list(port_list_id)
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
            PortList.modify_port_list(port_list_id, comment=comment, name=name)
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
