# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Greenbone Networks GmbH
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

# pylint: disable=too-many-lines

from enum import Enum

from typing import Optional

from gvm.errors import InvalidArgument

__all__ = [
    "AggregateStatistic",
    "EntityType",
    "FeedType",
    "FilterType",
    "HostsOrdering",
    "PermissionSubjectType",
    "ScannerType",
    "SortOrder",
    "TicketStatus",
    "TimeUnit",
    "UserAuthType",
    "get_aggregate_statistic_from_string",
    "get_entity_type_from_string",
    "get_feed_type_from_string",
    "get_filter_type_from_string",
    "get_hosts_ordering_from_string",
    "get_permission_subject_type_from_string",
    "get_scanner_type_from_string",
    "get_sort_order_from_string",
    "get_ticket_status_from_string",
    "get_time_unit_from_string",
    "get_user_auth_type_from_string",
]


class EntityType(Enum):
    """Enum for entity types"""

    ALERT = "alert"
    ASSET = "asset"
    AUDIT = "audit"
    CERT_BUND_ADV = "cert_bund_adv"
    CPE = "cpe"
    CREDENTIAL = "credential"
    CVE = "cve"
    DFN_CERT_ADV = "dfn_cert_adv"
    FILTER = "filter"
    GROUP = "group"
    HOST = "host"
    INFO = "info"
    NOTE = "note"
    NVT = "nvt"
    OPERATING_SYSTEM = "os"
    OVALDEF = "ovaldef"
    OVERRIDE = "override"
    PERMISSION = "permission"
    POLICY = "policy"
    PORT_LIST = "port_list"
    REPORT = "report"
    REPORT_FORMAT = "report_format"
    RESULT = "result"
    ROLE = "role"
    SCAN_CONFIG = "config"
    SCANNER = "scanner"
    SCHEDULE = "schedule"
    TAG = "tag"
    TARGET = "target"
    TASK = "task"
    TICKET = "ticket"
    TLS_CERTIFICATE = "tls_certificate"
    USER = "user"
    VULNERABILITY = "vuln"


def get_entity_type_from_string(
    entity_type: Optional[str],
) -> Optional[EntityType]:
    """Convert a entity type string to an actual EntityType instance

    Arguments:
        entity_type: Entity type string to convert to a EntityType
    """
    if not entity_type:
        return None

    if entity_type == 'vuln':
        return EntityType.VULNERABILITY

    if entity_type == 'os':
        return EntityType.OPERATING_SYSTEM

    if entity_type == 'config':
        return EntityType.SCAN_CONFIG

    if entity_type == 'tls_certificate':
        return EntityType.TLS_CERTIFICATE

    try:
        return EntityType[entity_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='entity_type',
            function=get_entity_type_from_string.__name__,
        ) from None


class FeedType(Enum):
    """Enum for feed types"""

    NVT = "NVT"
    CERT = "CERT"
    SCAP = "SCAP"
    GVMD_DATA = "GVMD_DATA"


def get_feed_type_from_string(feed_type: Optional[str]) -> Optional[FeedType]:
    """Convert a feed type string into a FeedType instance"""
    if not feed_type:
        return None

    try:
        return FeedType[feed_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='feed_type', function=get_feed_type_from_string.__name__
        ) from None


class FilterType(Enum):
    """Enum for filter types"""

    ALERT = "alert"
    ASSET = "asset"
    SCAN_CONFIG = "config"
    CREDENTIAL = "credential"
    FILTER = "filter"
    GROUP = "group"
    HOST = "host"
    NOTE = "note"
    OPERATING_SYSTEM = "os"
    OVERRIDE = "override"
    PERMISSION = "permission"
    PORT_LIST = "port_list"
    REPORT = "report"
    REPORT_FORMAT = "report_format"
    RESULT = "result"
    ROLE = "role"
    SCHEDULE = "schedule"
    ALL_SECINFO = "secinfo"
    TAG = "tag"
    TARGET = "target"
    TASK = "task"
    TICKET = "ticket"
    TLS_CERTIFICATE = "tls_certificate"
    USER = "user"
    VULNERABILITY = "vuln"


def get_filter_type_from_string(
    filter_type: Optional[str],
) -> Optional[FilterType]:
    """Convert a filter type string to an actual FilterType instance

    Arguments:
        filter_type (str): Filter type string to convert to a FilterType
    """
    if not filter_type:
        return None

    if filter_type == 'vuln':
        return FilterType.VULNERABILITY

    if filter_type == 'os':
        return FilterType.OPERATING_SYSTEM

    if filter_type == 'config':
        return FilterType.SCAN_CONFIG

    if filter_type == 'secinfo':
        return FilterType.ALL_SECINFO

    if filter_type == 'tls_certificate':
        return FilterType.TLS_CERTIFICATE

    try:
        return FilterType[filter_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='filter_type',
            function=get_filter_type_from_string.__name__,
        ) from None


class AggregateStatistic(Enum):
    """Enum for aggregate statistic types"""

    COUNT = "count"  # Number of items
    C_COUNT = "c_count"  # Cumulative number of items
    C_SUM = "c_sum"  # Cumulative sum of values
    MAX = "max"  # Maximum value
    MEAN = "mean"  # Arithmetic mean of values
    MIN = "min"  # Minimum value
    SUM = "sum"  # Sum of values
    TEXT = "text"  # Text column value
    VALUE = "value"  # Group or subgroup column value


def get_aggregate_statistic_from_string(
    aggregate_statistic: Optional[str],
) -> Optional[AggregateStatistic]:
    """
    Convert a aggregate statistic string to an actual AggregateStatistic
    instance.

    Arguments:
        aggregate_statistic: Aggregate statistic string to convert to a
            AggregateStatistic
    """
    if not aggregate_statistic:
        return None

    try:
        return AggregateStatistic[aggregate_statistic.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='aggregate_statistic',
            function=get_aggregate_statistic_from_string.__name__,
        ) from None


class ScannerType(Enum):
    """Enum for scanner type"""

    OSP_SCANNER_TYPE = "1"
    OPENVAS_SCANNER_TYPE = "2"
    CVE_SCANNER_TYPE = "3"
    GMP_SCANNER_TYPE = "4"  # formerly slave scanner
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
        scanner_type == ScannerType.GMP_SCANNER_TYPE.value
        or scanner_type == 'gmp'
    ):
        return ScannerType.GMP_SCANNER_TYPE

    if (
        scanner_type == ScannerType.GREENBONE_SENSOR_SCANNER_TYPE.value
        or scanner_type == 'greenbone'
    ):
        return ScannerType.GREENBONE_SENSOR_SCANNER_TYPE

    raise InvalidArgument(
        argument='scanner_type', function=get_scanner_type_from_string.__name__
    )


class SortOrder(Enum):
    """Enum for sort order"""

    ASCENDING = "ascending"
    DESCENDING = "descending"


def get_sort_order_from_string(
    sort_order: Optional[str],
) -> Optional[SortOrder]:
    """
    Convert a sort order string to an actual SortOrder instance.

    Arguments:
        sort_order: Sort order string to convert to a SortOrder
    """
    if not sort_order:
        return None

    try:
        return SortOrder[sort_order.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='sort_order', function=get_sort_order_from_string.__name__
        ) from None


class TicketStatus(Enum):
    """Enum for ticket status"""

    OPEN = 'Open'
    FIXED = 'Fixed'
    CLOSED = 'Closed'


def get_ticket_status_from_string(
    ticket_status: Optional[str],
) -> Optional[TicketStatus]:
    """Convert a ticket status string into a TicketStatus instance"""
    if not ticket_status:
        return None

    try:
        return TicketStatus[ticket_status.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='ticket_status',
            function=get_ticket_status_from_string.__name__,
        ) from None


class HostsOrdering(Enum):
    """Enum for host ordering during scans"""

    SEQUENTIAL = "sequential"
    RANDOM = "random"
    REVERSE = "reverse"


def get_hosts_ordering_from_string(
    hosts_ordering: Optional[str],
) -> Optional[HostsOrdering]:
    """Convert a hosts ordering string to an actual HostsOrdering instance

    Arguments:
        hosts_ordering: Host ordering string to convert to a HostsOrdering
    """
    if not hosts_ordering:
        return None
    try:
        return HostsOrdering[hosts_ordering.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='hosts_ordering',
            function=get_hosts_ordering_from_string.__name__,
        ) from None


class PermissionSubjectType(Enum):
    """Enum for permission subject type"""

    USER = 'user'
    GROUP = 'group'
    ROLE = 'role'


def get_permission_subject_type_from_string(
    subject_type: Optional[str],
) -> Optional[PermissionSubjectType]:
    """Convert a permission subject type string to an actual
    PermissionSubjectType instance

    Arguments:
        subject_type: Permission subject type string to convert to a
            PermissionSubjectType
    """
    if not subject_type:
        return None

    try:
        return PermissionSubjectType[subject_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='subject_type',
            function=get_permission_subject_type_from_string.__name__,
        ) from None


class TimeUnit(Enum):
    """Enum for time units"""

    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    DECADE = "decade"


def get_time_unit_from_string(time_unit: Optional[str]) -> Optional[TimeUnit]:
    """Convert a time unit string into a TimeUnit instance"""
    if not time_unit:
        return None

    try:
        return TimeUnit[time_unit.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='severity_level',
            function=get_time_unit_from_string.__name__,
        ) from None


class UserAuthType(Enum):
    """Enum for Sources allowed for authentication for the user"""

    FILE = 'file'
    LDAP_CONNECT = 'ldap_connect'
    RADIUS_CONNECT = 'radius_connect'


def get_user_auth_type_from_string(
    user_auth_type: Optional[str],
) -> Optional[UserAuthType]:
    """Convert a user auth type string into a UserAuthType instance"""
    if not user_auth_type:
        return None

    try:
        return UserAuthType[user_auth_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='user_auth_type',
            function=get_user_auth_type_from_string.__name__,
        ) from None
