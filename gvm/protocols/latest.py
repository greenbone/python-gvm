# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""Latest supported protocols, including unstable ones.

This module exposes the latest supported protocols of GVM including versions
not yet released as stable.

The provided Gmp class implements the latest `Greenbone Management Protocol`.
The provided Osp class implements the latest Open Scanner Protocol.

For details about the possible supported protocol versions please take a look at
:py:mod:`gvm.protocols`.

Exports:
  - :py:class:`gvm.protocols.gmpv225.Gmp`
  - :py:class:`gvm.protocols.ospv1.Osp`

.. _Greenbone Management Protocol:
    https://docs.greenbone.net/API/GMP/gmp.html
"""

from .gmpv225 import (
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
    Gmp,
    HelpFormat,
    HostsOrdering,
    InfoType,
    PermissionSubjectType,
    PortRangeType,
    ReportFormatType,
    ResourceType,
    ScannerType,
    SeverityLevel,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
    SortOrder,
    TicketStatus,
    UserAuthType,
)
from .ospv1 import Osp

__all__ = [
    "Gmp",
    "Osp",
    "AggregateStatistic",
    "AlertCondition",
    "AlertEvent",
    "AlertMethod",
    "AliveTest",
    "CredentialType",
    "CredentialFormat",
    "EntityType",
    "FeedType",
    "FilterType",
    "HelpFormat",
    "HostsOrdering",
    "InfoType",
    "PermissionSubjectType",
    "PortRangeType",
    "ReportFormatType",
    "ResourceType",
    "ScannerType",
    "SeverityLevel",
    "SnmpAuthAlgorithm",
    "SnmpPrivacyAlgorithm",
    "SortOrder",
    "TicketStatus",
    "UserAuthType",
]
