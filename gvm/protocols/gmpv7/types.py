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

__all__ = [
    "AlertCondition",
    "AlertEvent",
    "AlertMethod",
    "AliveTest",
    "AssetType",
    "CredentialType",
    "CredentialFormat",
    "EntityType",
    "FeedType",
    "FilterType",
    "HostsOrdering",
    "InfoType",
    "PermissionSubjectType",
    "PortRangeType",
    "ReportFormatType",
    "ScannerType",
    "SeverityLevel",
    "SnmpAuthAlgorithm",
    "SnmpPrivacyAlgorithm",
    "TimeUnit",
    "get_alive_test_from_string",
    "get_alert_condition_from_string",
    "get_alert_event_from_string",
    "get_alert_method_from_string",
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
    "get_time_unit_from_string",
]


class AlertEvent(Enum):
    """Enum for alert event types """

    TASK_RUN_STATUS_CHANGED = 'Task run status changed'
    UPDATED_SECINFO_ARRIVED = 'Updated SecInfo arrived'
    NEW_SECINFO_ARRIVED = 'New SecInfo arrived'


def get_alert_event_from_string(
    alert_event: Optional[str],
) -> Optional[AlertEvent]:
    """Convert an alert event string into a AlertEvent instance """
    if not alert_event:
        return None

    alert_event = alert_event.lower()

    if alert_event == 'task run status changed':
        return AlertEvent.TASK_RUN_STATUS_CHANGED

    if alert_event == 'updated secinfo arrived':
        return AlertEvent.UPDATED_SECINFO_ARRIVED

    if alert_event == 'new secinfo arrived':
        return AlertEvent.NEW_SECINFO_ARRIVED

    raise InvalidArgument(
        argument='alert_event', function=get_alert_event_from_string.__name__
    )


class AlertCondition(Enum):
    """Enum for alert condition types """

    ALWAYS = 'Always'
    SEVERITY_AT_LEAST = 'Severity at least'
    FILTER_COUNT_CHANGED = 'Filter count changed'
    FILTER_COUNT_AT_LEAST = 'Filter count at least'


def get_alert_condition_from_string(
    alert_condition: Optional[str],
) -> Optional[AlertCondition]:
    """Convert an alert condition string into a AlertCondition instance """
    if not alert_condition:
        return None

    alert_condition = alert_condition.lower()

    if alert_condition == 'always':
        return AlertCondition.ALWAYS

    if alert_condition == 'filter count changed':
        return AlertCondition.FILTER_COUNT_CHANGED

    if alert_condition == 'filter count at least':
        return AlertCondition.FILTER_COUNT_AT_LEAST

    if alert_condition == 'severity at least':
        return AlertCondition.SEVERITY_AT_LEAST

    raise InvalidArgument(
        argument='alert_condition',
        function=get_alert_condition_from_string.__name__,
    )


class AlertMethod(Enum):
    """Enum for alert method type"""

    SCP = "SCP"
    SEND = "Send"
    SMB = "SMB"
    SNMP = "SNMP"
    SYSLOG = "Syslog"
    EMAIL = "Email"
    START_TASK = "Start Task"
    HTTP_GET = "HTTP Get"
    SOURCEFIRE_CONNECTOR = "Sourcefire Connector"
    VERINICE_CONNECTOR = "verinice Connector"


def get_alert_method_from_string(
    alert_method: Optional[str],
) -> Optional[AlertMethod]:
    """Convert an alert method string into a AlertCondition instance """
    if not alert_method:
        return None

    alert_method = alert_method.upper()

    if alert_method == 'START TASK':
        return AlertMethod.START_TASK

    if alert_method == 'HTTP GET':
        return AlertMethod.HTTP_GET

    if alert_method == 'SOURCEFIRE CONNECTOR':
        return AlertMethod.SOURCEFIRE_CONNECTOR

    if alert_method == 'VERINICE CONNECTOR':
        return AlertMethod.VERINICE_CONNECTOR

    try:
        return AlertMethod[alert_method]
    except KeyError:
        raise InvalidArgument(
            argument='alert_method',
            function=get_alert_method_from_string.__name__,
        ) from None


class AliveTest(Enum):
    """Enum for choosing an alive test """

    SCAN_CONFIG_DEFAULT = 'Scan Config Default'
    ICMP_PING = 'ICMP Ping'
    TCP_ACK_SERVICE_PING = 'TCP-ACK Service Ping'
    TCP_SYN_SERVICE_PING = 'TCP-SYN Service Ping'
    ARP_PING = 'ARP Ping'
    APR_PING = 'ARP Ping'  # Alias for ARP_PING
    ICMP_AND_TCP_ACK_SERVICE_PING = 'ICMP & TCP-ACK Service Ping'
    ICMP_AND_ARP_PING = 'ICMP & ARP Ping'
    TCP_ACK_SERVICE_AND_ARP_PING = 'TCP-ACK Service & ARP Ping'
    ICMP_TCP_ACK_SERVICE_AND_ARP_PING = (  # pylint: disable=invalid-name
        'ICMP, TCP-ACK Service & ARP Ping'
    )
    CONSIDER_ALIVE = 'Consider Alive'


def get_alive_test_from_string(
    alive_test: Optional[str],
) -> Optional[AliveTest]:
    """Convert an alive test string into a AliveTest instance """
    if not alive_test:
        return None

    alive_test = alive_test.lower()

    if alive_test == 'scan config default':
        return AliveTest.SCAN_CONFIG_DEFAULT

    if alive_test == 'icmp ping':
        return AliveTest.ICMP_PING

    if alive_test == 'tcp-ack service ping':
        return AliveTest.TCP_ACK_SERVICE_PING

    if alive_test == 'tcp-syn service ping':
        return AliveTest.TCP_SYN_SERVICE_PING

    if alive_test == 'arp ping':
        return AliveTest.ARP_PING

    if alive_test == 'icmp & tcp-ack service ping':
        return AliveTest.ICMP_AND_TCP_ACK_SERVICE_PING

    if alive_test == 'icmp & arp ping':
        return AliveTest.ICMP_AND_ARP_PING

    if alive_test == 'tcp-ack service & arp ping':
        return AliveTest.TCP_ACK_SERVICE_AND_ARP_PING

    if alive_test == 'icmp, tcp-ack service & arp ping':
        return AliveTest.ICMP_TCP_ACK_SERVICE_AND_ARP_PING

    if alive_test == 'consider alive':
        return AliveTest.CONSIDER_ALIVE

    raise InvalidArgument(
        argument='alive_test', function=get_alive_test_from_string.__name__
    )


class AssetType(Enum):
    """"Enum for asset types """

    OPERATING_SYSTEM = 'os'
    HOST = 'host'


def get_asset_type_from_string(
    asset_type: Optional[str],
) -> Optional[AssetType]:
    if not asset_type:
        return None

    if asset_type == 'os':
        return AssetType.OPERATING_SYSTEM

    try:
        return AssetType[asset_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='asset_type', function=get_asset_type_from_string.__name__
        ) from None


class CredentialFormat(Enum):
    """ Enum for credential format """

    KEY = 'key'
    RPM = 'rpm'
    DEB = 'deb'
    EXE = 'exe'
    PEM = 'pem'


def get_credential_format_from_string(
    credential_format: Optional[str],
) -> Optional[CredentialFormat]:
    if not credential_format:
        return None

    try:
        return CredentialFormat[credential_format.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='credential_format',
            function=get_credential_format_from_string.__name__,
        ) from None


class CredentialType(Enum):
    """Enum for credential types """

    CLIENT_CERTIFICATE = 'cc'
    SNMP = 'snmp'
    USERNAME_PASSWORD = 'up'
    USERNAME_SSH_KEY = 'usk'


def get_credential_type_from_string(
    credential_type: Optional[str],
) -> Optional[CredentialType]:
    """Convert a credential type string into a CredentialType instance"""
    if not credential_type:
        return None

    try:
        return CredentialType[credential_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='credential_type',
            function=get_credential_type_from_string.__name__,
        ) from None


class EntityType(Enum):
    """Enum for entity types """

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


def get_entity_type_from_string(
    entity_type: Optional[str],
) -> Optional[EntityType]:
    """Convert a entity type string to an actual EntityType instance

    Arguments:
        entity_type: Resource type string to convert to a EntityType
    """
    if not entity_type:
        return None

    if entity_type == 'config':
        return EntityType.SCAN_CONFIG
    if entity_type == 'os':
        return EntityType.OPERATING_SYSTEM

    try:
        return EntityType[entity_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='entity_type',
            function=get_entity_type_from_string.__name__,
        ) from None


class FeedType(Enum):
    """Enum for feed types """

    NVT = "NVT"
    CERT = "CERT"
    SCAP = "SCAP"


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
    """Enum for filter types """

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
    USER = "user"


def get_filter_type_from_string(
    filter_type: Optional[str],
) -> Optional[FilterType]:
    """Convert a filter type string to an actual FilterType instance

    Arguments:
        filter_type: Filter type string to convert to a FilterType
    """
    if not filter_type:
        return None

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
        ) from None


class HostsOrdering(Enum):
    """ Enum for host ordering during scans """

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


class InfoType(Enum):
    """ Enum for info types """

    CERT_BUND_ADV = "CERT_BUND_ADV"
    CPE = "CPE"
    CVE = "CVE"
    DFN_CERT_ADV = "DFN_CERT_ADV"
    OVALDEF = "OVALDEF"
    NVT = "NVT"
    ALLINFO = "ALLINFO"


def get_info_type_from_string(info_type: Optional[str]) -> Optional[InfoType]:
    """Convert a info type string to an actual InfoType instance

    Arguments:
        info_type: Info type string to convert to a InfoType
    """
    if not info_type:
        return None
    try:
        return InfoType[info_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='info_type', function=get_info_type_from_string.__name__
        ) from None


class PermissionSubjectType(Enum):
    """ Enum for permission subject type """

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


class PortRangeType(Enum):
    """ Enum for port range type """

    TCP = 'TCP'
    UDP = 'UDP'


def get_port_range_type_from_string(
    port_range_type: Optional[str],
) -> Optional[PortRangeType]:
    """Convert a port range type string to an actual PortRangeType instance

    Arguments:
        port_range_type: Port range type string to convert to a PortRangeType
    """
    if not port_range_type:
        return None

    try:
        return PortRangeType[port_range_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='port_range_type',
            function=get_port_range_type_from_string.__name__,
        ) from None


class ReportFormatType(Enum):
    """ Enum for builtin report formats """

    ANONYMOUS_XML = '5057e5cc-b825-11e4-9d0e-28d24461215b'
    ARF = '910200ca-dc05-11e1-954f-406186ea4fc5'
    CPE = '5ceff8ba-1f62-11e1-ab9f-406186ea4fc5'
    CSV_HOSTS = '9087b18c-626c-11e3-8892-406186ea4fc5"'
    CSV_RESULTS = 'c1645568-627a-11e3-a660-406186ea4fc5'
    GCR_PDF = 'dc51a40a-c022-11e9-b02d-3f7ca5bdcb11'
    GSR_HTML = 'ffa123c9-a2d2-409e-bbbb-a6c1385dbeaa'
    GSR_PDF = '35ba7077-dc85-42ef-87c9-b0eda7e903b6'
    GXCR_PDF = 'f0d348de-c022-11e9-bc4c-4bf1d5e1a8ca'
    GXR_PDF = 'ebbc7f34-8ae5-11e1-b07b-001f29eadec8'
    ITG = '77bd6c4a-1f62-11e1-abf0-406186ea4fc5'
    LATEX = 'a684c02c-b531-11e1-bdc2-406186ea4fc5'
    NBE = '9ca6fe72-1f62-11e1-9e7c-406186ea4fc5'
    PDF = 'c402cc3e-b531-11e1-9163-406186ea4fc5'
    SVG = '9e5e5deb-879e-4ecc-8be6-a71cd0875cdd'
    TXT = 'a3810a62-1f62-11e1-9219-406186ea4fc5'
    VERINICE_ISM = 'c15ad349-bd8d-457a-880a-c7056532ee15'
    VERINICE_ITG = '50c9950a-f326-11e4-800c-28d24461215b'
    XML = 'a994b278-1f62-11e1-96ac-406186ea4fc5'


def get_report_format_id_from_string(
    report_format: Optional[str],
) -> Optional[ReportFormatType]:
    """Convert an report format name into a ReportFormatType instance """
    if not report_format:
        return None

    report_format = report_format.lower()

    if report_format == 'anonymous xml':
        return ReportFormatType.ANONYMOUS_XML

    if report_format == 'arf':
        return ReportFormatType.ARF

    if report_format == 'cpe':
        return ReportFormatType.CPE

    if report_format == 'csv hosts':
        return ReportFormatType.CSV_HOSTS

    if report_format == 'csv results':
        return ReportFormatType.CSV_RESULTS

    if report_format == 'gcr pdf':
        return ReportFormatType.GCR_PDF

    if report_format == 'gsr html':
        return ReportFormatType.GSR_HTML

    if report_format == 'gsr pdf':
        return ReportFormatType.GSR_PDF

    if report_format == 'gxcr pdf':
        return ReportFormatType.GXCR_PDF

    if report_format == 'gxr pdf':
        return ReportFormatType.GXR_PDF

    if report_format == 'itg':
        return ReportFormatType.ITG

    if report_format == 'latex':
        return ReportFormatType.LATEX

    if report_format == 'nbe':
        return ReportFormatType.NBE

    if report_format == 'pdf':
        return ReportFormatType.PDF

    if report_format == 'svg':
        return ReportFormatType.SVG

    if report_format == 'txt':
        return ReportFormatType.TXT

    if report_format == 'verinice ism':
        return ReportFormatType.VERINICE_ISM

    if report_format == 'verinice itg':
        return ReportFormatType.VERINICE_ITG

    if report_format == 'xml':
        return ReportFormatType.XML

    raise InvalidArgument(
        argument='report_format',
        function=get_report_format_id_from_string.__name__,
    )


class ScannerType(Enum):
    """ Enum for scanner type """

    OSP_SCANNER_TYPE = "1"
    OPENVAS_SCANNER_TYPE = "2"
    CVE_SCANNER_TYPE = "3"
    GMP_SCANNER_TYPE = "4"  # formerly slave scanner


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

    raise InvalidArgument(
        argument='scanner_type', function=get_scanner_type_from_string.__name__
    )


class SnmpAuthAlgorithm(Enum):
    """ Enum for SNMP auth algorithm """

    SHA1 = 'sha1'
    MD5 = 'md5'


def get_snmp_auth_algorithm_from_string(
    algorithm: Optional[str],
) -> Optional[SnmpAuthAlgorithm]:
    """Convert a SNMP auth algorithm string into a SnmpAuthAlgorithm instance"""
    if not algorithm:
        return None

    try:
        return SnmpAuthAlgorithm[algorithm.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='algorithm',
            function=get_snmp_auth_algorithm_from_string.__name__,
        ) from None


class SnmpPrivacyAlgorithm(Enum):
    """ Enum for SNMP privacy algorithm """

    AES = 'aes'
    DES = 'des'


def get_snmp_privacy_algorithm_from_string(
    algorithm: Optional[str],
) -> Optional[SnmpPrivacyAlgorithm]:
    """Convert a SNMP privacy algorithm string into a SnmpPrivacyAlgorithm
    instance
    """
    if not algorithm:
        return None

    try:
        return SnmpPrivacyAlgorithm[algorithm.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='algorithm',
            function=get_snmp_privacy_algorithm_from_string.__name__,
        ) from None


class SeverityLevel(Enum):
    """ Enum for severity levels """

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOG = "Log"
    ALARM = "Alarm"
    DEBUG = "Debug"


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


class TimeUnit(Enum):
    """ Enum for time units """

    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    DECADE = "decade"


def get_time_unit_from_string(time_unit: Optional[str]) -> Optional[TimeUnit]:
    """ Convert a time unit string into a TimeUnit instance """
    if not time_unit:
        return None

    try:
        return TimeUnit[time_unit.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='severity_level',
            function=get_severity_level_from_string.__name__,
        ) from None
