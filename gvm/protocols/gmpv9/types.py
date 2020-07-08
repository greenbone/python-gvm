# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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

from gvm.protocols.gmpv8.types import (
    AlertCondition,
    AlertEvent,
    AlertMethod,
    AliveTest,
    AssetType,
    CredentialFormat,
    CredentialType,
    FeedType,
    HostsOrdering,
    InfoType,
    PermissionSubjectType,
    PortRangeType,
    SeverityLevel,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
    TicketStatus,
    TimeUnit,
    get_alert_condition_from_string,
    get_alert_event_from_string,
    get_alert_method_from_string,
    get_alive_test_from_string,
    get_asset_type_from_string,
    get_credential_format_from_string,
    get_credential_type_from_string,
    get_feed_type_from_string,
    get_hosts_ordering_from_string,
    get_info_type_from_string,
    get_permission_subject_type_from_string,
    get_port_range_type_from_string,
    get_severity_level_from_string,
    get_snmp_auth_algorithm_from_string,
    get_snmp_privacy_algorithm_from_string,
    get_ticket_status_from_string,
    get_time_unit_from_string,
)


__all__ = [
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
    "TicketStatus",
    "TimeUnit",
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
    "get_scanner_type_from_string",
    "get_severity_level_from_string",
    "get_snmp_auth_algorithm_from_string",
    "get_snmp_privacy_algorithm_from_string",
    "get_ticket_status_from_string",
    "get_time_unit_from_string",
]


class EntityType(Enum):
    """ Enum for entity types """

    AGENT = "agent"
    ALERT = "alert"
    ASSET = "asset"
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
    """ Convert a entity type string to an actual EntityType instance

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
        )


class FilterType(Enum):
    """ Enum for filter types """

    AGENT = "agent"
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
    """ Convert a filter type string to an actual FilterType instance

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
        )


class ScannerType(Enum):
    """ Enum for scanner type """

    OSP_SCANNER_TYPE = "1"
    OPENVAS_SCANNER_TYPE = "2"
    CVE_SCANNER_TYPE = "3"
    GMP_SCANNER_TYPE = "4"  # formerly slave scanner
    GREENBONE_SENSOR_SCANNER_TYPE = "5"


def get_scanner_type_from_string(
    scanner_type: Optional[str],
) -> Optional[ScannerType]:
    """ Convert a scanner type string to an actual ScannerType instance

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


class _UsageType(Enum):
    """ Enum for usage types """

    AUDIT = "audit"
    POLICY = "policy"
    SCAN = "scan"


def __get_usage_type_from_string(
    usage_type: Optional[str],
) -> Optional[_UsageType]:
    """ Convert a usage type string to an actual _UsageType instance

    Arguments:
        entity_type: Usage type string to convert to a _UsageType
    """
    if not usage_type:
        return None

    try:
        return _UsageType[usage_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='usage_type',
            function=__get_usage_type_from_string.__name__,
        )
