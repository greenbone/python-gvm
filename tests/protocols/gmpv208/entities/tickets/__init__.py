# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_ticket import GmpCloneTicketTestMixin
from .test_create_ticket import GmpCreateTicketTestMixin
from .test_delete_ticket import GmpDeleteTicketTestMixin
from .test_get_ticket import GmpGetTicketTestMixin
from .test_get_tickets import GmpGetTicketsTestMixin
from .test_modify_ticket import GmpModifyTicketTestMixin

__all__ = (
    "GmpCloneTicketTestMixin",
    "GmpCreateTicketTestMixin",
    "GmpDeleteTicketTestMixin",
    "GmpGetTicketTestMixin",
    "GmpGetTicketsTestMixin",
    "GmpModifyTicketTestMixin",
)
