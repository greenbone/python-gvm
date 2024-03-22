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
    PortList,
    PortRangeType,
    SortOrder,
    SystemReports,
    TrashCan,
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
