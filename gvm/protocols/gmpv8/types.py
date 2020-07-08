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

from gvm.protocols.gmpv7.types import (
    AlertCondition,
    AlertEvent,
    AlertMethod,
    AliveTest,
    AssetType,
    CredentialFormat,
    FeedType,
    HostsOrdering,
    InfoType,
    PermissionSubjectType,
    PortRangeType,
    ScannerType,
    SeverityLevel,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
    TimeUnit,
    get_alert_condition_from_string,
    get_alert_event_from_string,
    get_alert_method_from_string,
    get_alive_test_from_string,
    get_asset_type_from_string,
    get_credential_format_from_string,
    get_feed_type_from_string,
    get_hosts_ordering_from_string,
    get_info_type_from_string,
    get_permission_subject_type_from_string,
    get_port_range_type_from_string,
    get_severity_level_from_string,
    get_scanner_type_from_string,
    get_snmp_auth_algorithm_from_string,
    get_snmp_privacy_algorithm_from_string,
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
    USER = "user"

    TICKET = "ticket"
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

    try:
        return FilterType[filter_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='filter_type',
            function=get_filter_type_from_string.__name__,
        )


class CredentialType(Enum):
    """ Enum for credential types """

    CLIENT_CERTIFICATE = 'cc'
    SNMP = 'snmp'
    USERNAME_PASSWORD = 'up'
    USERNAME_SSH_KEY = 'usk'
    SMIME_CERTIFICATE = 'smime'
    PGP_ENCRYPTION_KEY = 'pgp'
    PASSWORD_ONLY = 'pw'


def get_credential_type_from_string(
    credential_type: Optional[str],
) -> Optional[CredentialType]:
    """ Convert a credential type string into a CredentialType instance
    """
    if not credential_type:
        return None

    try:
        return CredentialType[credential_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='credential_type',
            function=get_credential_type_from_string.__name__,
        )


class TicketStatus(Enum):
    """ Enum for ticket status """

    OPEN = 'Open'
    FIXED = 'Fixed'
    CLOSED = 'Closed'


def get_ticket_status_from_string(
    ticket_status: Optional[str],
) -> Optional[TicketStatus]:
    """ Convert a ticket status string into a TicketStatus instance
    """
    if not ticket_status:
        return None

    try:
        return TicketStatus[ticket_status.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='ticket_status',
            function=get_ticket_status_from_string.__name__,
        )
