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

# pylint: disable=too-many-lines,redefined-builtin

"""
Module for communication with gvmd in
`Greenbone Management Protocol version 21.04`_

.. _Greenbone Management Protocol version 21.04:
    https://docs.greenbone.net/API/GMP/gmp-21.04.html
"""

import logging
from typing import Any, Callable, Optional

from gvm.protocols.base import GvmProtocol

from gvm.protocols.gmpv208.entities.alerts import (
    AlertCondition,
    AlertEvent,
    AlertMethod,
    AlertsMixin,
    get_alert_condition_from_string,
    get_alert_event_from_string,
    get_alert_method_from_string,
)
from gvm.protocols.gmpv208.entities.audits import AuditsMixin
from gvm.protocols.gmpv208.entities.credentials import (
    CredentialFormat,
    CredentialsMixin,
    CredentialType,
    get_credential_format_from_string,
    get_credential_type_from_string,
    get_snmp_auth_algorithm_from_string,
    get_snmp_privacy_algorithm_from_string,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
)
from gvm.protocols.gmpv208.entities.entities import (
    EntityType,
    get_entity_type_from_string,
)
from gvm.protocols.gmpv208.entities.filter import (
    FiltersMixin,
    FilterType,
    get_filter_type_from_string,
)
from gvm.protocols.gmpv208.entities.groups import GroupsMixin
from gvm.protocols.gmpv208.entities.hosts import (
    HostsMixin,
    HostsOrdering,
    get_hosts_ordering_from_string,
)
from gvm.protocols.gmpv208.entities.operating_systems import (
    OperatingSystemsMixin,
)
from gvm.protocols.gmpv208.entities.permissions import (
    PermissionsMixin,
    PermissionSubjectType,
    get_permission_subject_type_from_string,
)
from gvm.protocols.gmpv208.entities.policies import PoliciesMixin
from gvm.protocols.gmpv208.entities.port_lists import (
    PortListMixin,
    PortRangeType,
    get_port_range_type_from_string,
)
from gvm.protocols.gmpv208.entities.reports import ReportsMixin
from gvm.protocols.gmpv208.entities.report_formats import (
    ReportFormatType,
    ReportFormatsMixin,
    get_report_format_id_from_string,
)
from gvm.protocols.gmpv208.entities.results import ResultsMixin
from gvm.protocols.gmpv208.entities.roles import RolesMixin
from gvm.protocols.gmpv208.entities.scan_configs import ScanConfigsMixin
from gvm.protocols.gmpv208.entities.schedules import SchedulesMixin
from gvm.protocols.gmpv208.entities.secinfo import (
    get_info_type_from_string,
    InfoType,
    SecInfoMixin,
)
from gvm.protocols.gmpv208.entities.severity import (
    SeverityLevel,
    get_severity_level_from_string,
)
from gvm.protocols.gmpv208.entities.tags import TagsMixin
from gvm.protocols.gmpv208.entities.tasks import TasksMixin
from gvm.protocols.gmpv208.entities.tickets import (
    TicketStatus,
    TicketsMixin,
    get_ticket_status_from_string,
)
from gvm.protocols.gmpv208.entities.tls_certificates import TLSCertificateMixin
from gvm.protocols.gmpv208.entities.users import (
    UserAuthType,
    get_user_auth_type_from_string,
)
from gvm.protocols.gmpv208.entities.vulnerabilities import VulnerabilitiesMixin

from gvm.protocols.gmpv208.system.aggregates import (
    AggregatesMixin,
    AggregateStatistic,
    get_aggregate_statistic_from_string,
    SortOrder,
    get_sort_order_from_string,
)
from gvm.protocols.gmpv208.system.authentication import AuthenticationMixin
from gvm.protocols.gmpv208.system.feed import (
    FeedType,
    FeedMixin,
    get_feed_type_from_string,
)
from gvm.protocols.gmpv208.system.help import (
    HelpFormat,
    HelpMixin,
    get_help_format_from_string,
)
from gvm.protocols.gmpv208.system.system_reports import SystemReportsMixin
from gvm.protocols.gmpv208.system.user_settings import UserSettingsMixin
from gvm.protocols.gmpv208.system.trashcan import TrashcanMixin

# NEW IN 214
from gvm.protocols.gmpv214.entities.notes import NotesMixin
from gvm.protocols.gmpv214.entities.overrides import OverridesMixin
from gvm.protocols.gmpv214.entities.scanners import (
    ScannerType,
    ScannersMixin,
    get_scanner_type_from_string,
)
from gvm.protocols.gmpv214.entities.targets import (
    AliveTest,
    get_alive_test_from_string,
    TargetsMixin,
)
from gvm.protocols.gmpv214.entities.users import UsersMixin

from gvm.protocols.gmpv214.system.version import VersionMixin

from gvm.connections import GvmConnection

logger = logging.getLogger(__name__)

_TYPE_FIELDS = [
    AggregateStatistic,
    AlertCondition,
    AlertEvent,
    AlertMethod,
    AliveTest,
    CredentialFormat,
    CredentialType,
    EntityType,
    FeedType,
    FilterType,
    HostsOrdering,
    InfoType,
    HelpFormat,
    PortRangeType,
    PermissionSubjectType,
    ReportFormatType,
    ScannerType,
    SeverityLevel,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
    SortOrder,
    TicketStatus,
    UserAuthType,
]


class Gmp(
    GvmProtocol,
    AggregatesMixin,
    AlertsMixin,
    AuditsMixin,
    AuthenticationMixin,
    CredentialsMixin,
    FeedMixin,
    FiltersMixin,
    GroupsMixin,
    HelpMixin,
    HostsMixin,
    NotesMixin,
    OperatingSystemsMixin,
    OverridesMixin,
    PermissionsMixin,
    PoliciesMixin,
    PortListMixin,
    ReportFormatsMixin,
    ReportsMixin,
    ResultsMixin,
    RolesMixin,
    TagsMixin,
    TargetsMixin,
    TasksMixin,
    TicketsMixin,
    TLSCertificateMixin,
    TrashcanMixin,
    ScanConfigsMixin,
    ScannersMixin,
    SchedulesMixin,
    SecInfoMixin,
    SystemReportsMixin,
    UserSettingsMixin,
    UsersMixin,
    VersionMixin,
    VulnerabilitiesMixin,
):
    def __init__(
        self,
        connection: GvmConnection,
        *,
        transform: Optional[Callable[[str], Any]] = None,
    ):
        self.types = {}
        for t in _TYPE_FIELDS:
            self.types[t.__name__] = t

        super().__init__(connection, transform=transform)

        # Is authenticated on gvmd
        self._authenticated = False
