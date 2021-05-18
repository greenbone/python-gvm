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
    EntityType,
    FeedType,
    FilterType,
    HostsOrdering,
    PermissionSubjectType,
    SortOrder,
    TicketStatus,
    TimeUnit,
    UserAuthType,
    get_aggregate_statistic_from_string,
    get_entity_type_from_string,
    get_feed_type_from_string,
    get_filter_type_from_string,
    get_hosts_ordering_from_string,
    get_permission_subject_type_from_string,
    get_sort_order_from_string,
    get_ticket_status_from_string,
    get_time_unit_from_string,
    get_user_auth_type_from_string,
)


__all__ = [
    "AggregateStatistic",
    "EntityType",
    "FeedType",
    "FilterType",
    "HostsOrdering",
    "PermissionSubjectType",
    "SeverityLevel",
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
    "get_severity_level_from_string",
    "get_sort_order_from_string",
    "get_ticket_status_from_string",
    "get_time_unit_from_string",
    "get_user_auth_type_from_string",
]

# move this: Severity Level !!!
class SeverityLevel(Enum):
    """Enum for severity levels"""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOG = "Log"
    ALARM = "Alarm"


def get_severity_level_from_string(
    severity_level: Optional[str],
) -> Optional[SeverityLevel]:
    """Convert a severity level string into a SeverityLevel instance"""
    if not severity_level:
        return None

    try:
        return SeverityLevel[severity_level.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='severity_level',
            function=get_severity_level_from_string.__name__,
        ) from None
