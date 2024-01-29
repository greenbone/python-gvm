# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.tickets import (
    GmpCloneTicketTestMixin,
    GmpCreateTicketTestMixin,
    GmpDeleteTicketTestMixin,
    GmpGetTicketsTestMixin,
    GmpGetTicketTestMixin,
    GmpModifyTicketTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteTicketTestCase(GmpDeleteTicketTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetTicketTestCase(GmpGetTicketTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetTicketsTestCase(GmpGetTicketsTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CloneTicketTestCase(GmpCloneTicketTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateTicketTestCase(GmpCreateTicketTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyTicketTestCase(GmpModifyTicketTestMixin, Gmpv225TestCase):
    pass
