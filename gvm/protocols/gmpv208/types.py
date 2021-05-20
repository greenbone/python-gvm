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
    "HostsOrdering",
    "TicketStatus",
    "get_hosts_ordering_from_string",
    "get_ticket_status_from_string",
]


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
