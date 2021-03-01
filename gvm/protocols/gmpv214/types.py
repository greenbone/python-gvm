# -*- coding: utf-8 -*-
# Copyright (C) 2020-2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from enum import Enum

from typing import Optional

from gvm.errors import InvalidArgument


from gvm.protocols.gmpv208.types import (
    AggregateStatistic,
    AlertCondition,
    AlertEvent,
    AlertMethod,
    AliveTest,
    AssetType,
    CredentialFormat,
    CredentialType,
    EntityType,
    FeedType,
    FilterType,
    HostsOrdering,
    InfoType,
    PermissionSubjectType,
    PortRangeType,
    ReportFormatType,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
    SortOrder,
    TicketStatus,
    TimeUnit,
    UserAuthType,
    get_aggregate_statistic_from_string,
    get_alert_condition_from_string,
    get_alert_event_from_string,
    get_alert_method_from_string,
    get_alive_test_from_string,
    get_asset_type_from_string,
    get_credential_format_from_string,
    get_credential_type_from_string,
    get_entity_type_from_string,
    get_feed_type_from_string,
    get_filter_type_from_string,
    get_hosts_ordering_from_string,
    get_info_type_from_string,
    get_permission_subject_type_from_string,
    get_port_range_type_from_string,
    get_report_format_id_from_string,
    get_snmp_auth_algorithm_from_string,
    get_snmp_privacy_algorithm_from_string,
    get_sort_order_from_string,
    get_ticket_status_from_string,
    get_time_unit_from_string,
    get_user_auth_type_from_string,
)


__all__ = [
    "AggregateStatistic",
    "AlertCondition",
    "AlertEvent",
    "AlertMethod",
    "AliveTest",
    "AssetType",
    "CredentialFormat",
    "CredentialType",
    "EntityType",
    "FeedType",
    "FilterType",
    "HostsOrdering",
    "InfoType",
    "PermissionSubjectType",
    "PortRangeType",
    "ScannerType",
    "SeverityLevel",
    "SnmpAuthAlgorithm",
    "SnmpPrivacyAlgorithm",
    "SortOrder",
    "ReportFormatType",
    "TicketStatus",
    "TimeUnit",
    "UserAuthType",
    "get_aggregate_statistic_from_string",
    "get_alert_condition_from_string",
    "get_alert_event_from_string",
    "get_alert_method_from_string",
    "get_alive_test_from_string",
    "get_asset_type_from_string",
    "get_credential_format_from_string",
    "get_credential_type_from_string",
    "get_entity_type_from_string",
    "get_feed_type_from_string",
    "get_filter_type_from_string",
    "get_hosts_ordering_from_string",
    "get_info_type_from_string",
    "get_permission_subject_type_from_string",
    "get_port_range_type_from_string",
    "get_report_format_id_from_string",
    "get_scanner_type_from_string",
    "get_severity_level_from_string",
    "get_snmp_auth_algorithm_from_string",
    "get_snmp_privacy_algorithm_from_string",
    "get_sort_order_from_string",
    "get_ticket_status_from_string",
    "get_time_unit_from_string",
    "get_user_auth_type_from_string",
]


class SeverityLevel(Enum):
    """ Enum for severity levels """

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOG = "Log"
    ALARM = "Alarm"


def get_severity_level_from_string(
    severity_level: Optional[str],
) -> Optional[SeverityLevel]:
    """ Convert a severity level string into a SeverityLevel instance """
    if not severity_level:
        return None

    try:
        return SeverityLevel[severity_level.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='severity_level',
            function=get_severity_level_from_string.__name__,
        ) from None


class ScannerType(Enum):
    """ Enum for scanner type """

    OSP_SCANNER_TYPE = "1"
    OPENVAS_SCANNER_TYPE = "2"
    CVE_SCANNER_TYPE = "3"
    GREENBONE_SENSOR_SCANNER_TYPE = "5"


def get_scanner_type_from_string(
    scanner_type: Optional[str],
) -> Optional[ScannerType]:
    """Convert a scanner type string to an actual ScannerType instance

    Arguments:
        scanner_type: Scanner type string to convert to a ScannerType
    """
    if not scanner_type:
        return None

    scanner_type = scanner_type.lower()

    if (
        scanner_type == ScannerType.OSP_SCANNER_TYPE.value
        or scanner_type == 'osp'
    ):
        return ScannerType.OSP_SCANNER_TYPE

    if (
        scanner_type == ScannerType.OPENVAS_SCANNER_TYPE.value
        or scanner_type == 'openvas'
    ):
        return ScannerType.OPENVAS_SCANNER_TYPE

    if (
        scanner_type == ScannerType.CVE_SCANNER_TYPE.value
        or scanner_type == 'cve'
    ):
        return ScannerType.CVE_SCANNER_TYPE

    if (
        scanner_type == ScannerType.GREENBONE_SENSOR_SCANNER_TYPE.value
        or scanner_type == 'greenbone'
    ):
        return ScannerType.GREENBONE_SENSOR_SCANNER_TYPE

    raise InvalidArgument(
        argument='scanner_type', function=get_scanner_type_from_string.__name__
    )
