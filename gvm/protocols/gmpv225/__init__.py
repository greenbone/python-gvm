# -*- coding: utf-8 -*-
# Copyright (C) 2023 Greenbone AG
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
`Greenbone Management Protocol version 22.05`_

.. _Greenbone Management Protocol version 22.05:
    https://docs.greenbone.net/API/GMP/gmp-22.05.html
"""

import logging
from typing import Any, Callable, Optional

from gvm.connections import GvmConnection
from gvm.protocols.base import GvmProtocol
from gvm.protocols.gmpv208.entities.alerts import (
    AlertCondition,
    AlertEvent,
    AlertMethod,
    AlertsMixin,
)
from gvm.protocols.gmpv208.entities.audits import AuditsMixin
from gvm.protocols.gmpv208.entities.credentials import (
    CredentialFormat,
    CredentialsMixin,
    CredentialType,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
)
from gvm.protocols.gmpv208.entities.entities import EntityType
from gvm.protocols.gmpv208.entities.filter import FiltersMixin, FilterType
from gvm.protocols.gmpv208.entities.groups import GroupsMixin
from gvm.protocols.gmpv208.entities.hosts import HostsMixin, HostsOrdering
from gvm.protocols.gmpv208.entities.operating_systems import (
    OperatingSystemsMixin,
)
from gvm.protocols.gmpv208.entities.permissions import (
    PermissionsMixin,
    PermissionSubjectType,
)
from gvm.protocols.gmpv208.entities.policies import PoliciesMixin
from gvm.protocols.gmpv208.entities.port_lists import (
    PortListMixin,
    PortRangeType,
)
from gvm.protocols.gmpv208.entities.report_formats import (
    ReportFormatsMixin,
    ReportFormatType,
)
from gvm.protocols.gmpv208.entities.reports import ReportsMixin
from gvm.protocols.gmpv208.entities.results import ResultsMixin
from gvm.protocols.gmpv208.entities.roles import RolesMixin
from gvm.protocols.gmpv208.entities.schedules import SchedulesMixin
from gvm.protocols.gmpv208.entities.secinfo import InfoType, SecInfoMixin
from gvm.protocols.gmpv208.entities.severity import SeverityLevel
from gvm.protocols.gmpv208.entities.tags import TagsMixin
from gvm.protocols.gmpv208.entities.tasks import TasksMixin
from gvm.protocols.gmpv208.entities.tickets import TicketsMixin, TicketStatus
from gvm.protocols.gmpv208.entities.tls_certificates import TLSCertificateMixin
from gvm.protocols.gmpv208.entities.users import UserAuthType
from gvm.protocols.gmpv208.entities.vulnerabilities import VulnerabilitiesMixin
from gvm.protocols.gmpv208.system.aggregates import (
    AggregatesMixin,
    AggregateStatistic,
    SortOrder,
)
from gvm.protocols.gmpv208.system.authentication import AuthenticationMixin
from gvm.protocols.gmpv208.system.feed import FeedMixin, FeedType
from gvm.protocols.gmpv208.system.help import HelpFormat, HelpMixin
from gvm.protocols.gmpv208.system.system_reports import SystemReportsMixin
from gvm.protocols.gmpv208.system.trashcan import TrashcanMixin
from gvm.protocols.gmpv208.system.user_settings import UserSettingsMixin

# NEW IN 214
from gvm.protocols.gmpv214.entities.notes import NotesMixin
from gvm.protocols.gmpv214.entities.overrides import OverridesMixin
from gvm.protocols.gmpv214.entities.targets import AliveTest, TargetsMixin
from gvm.protocols.gmpv224.entities.scan_configs import ScanConfigsMixin
from gvm.protocols.gmpv224.entities.scanners import ScannersMixin, ScannerType

# NEW IN 224
from gvm.protocols.gmpv224.entities.users import UsersMixin

# NEW IN 225
from gvm.protocols.gmpv225.entities.resourcenames import (
    ResourceNamesMixin,
    ResourceType,
)
from gvm.protocols.gmpv225.system.version import VersionMixin
from gvm.utils import to_dotted_types_dict

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
    ResourceType,
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
    ResourceNamesMixin,
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
    """Python interface for Greenbone Management Protocol

    This class implements the `Greenbone Management Protocol version 22.05`_

    Arguments:
        connection: Connection to use to talk with the gvmd daemon. See
            :mod:`gvm.connections` for possible connection types.
        transform: Optional transform `callable`_ to convert response data.
            After each request the callable gets passed the plain response data
            which can be used to check the data and/or conversion into different
            representations like a xml dom.

            See :mod:`gvm.transforms` for existing transforms.

    .. _Greenbone Management Protocol version 22.05:
        https://docs.greenbone.net/API/GMP/gmp-22.05.html
    .. _callable:
        https://docs.python.org/3/library/functions.html#callable
    """

    def __init__(
        self,
        connection: GvmConnection,
        *,
        transform: Optional[Callable[[str], Any]] = None,
    ):
        self.types = to_dotted_types_dict(_TYPE_FIELDS)

        super().__init__(connection, transform=transform)

        # Is authenticated on gvmd
        self._authenticated = False
