# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
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
from ...gmpv214 import Gmpv214TestCase


class Gmpv214DeleteTicketTestCase(GmpDeleteTicketTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetTicketTestCase(GmpGetTicketTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetTicketsTestCase(GmpGetTicketsTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CloneTicketTestCase(GmpCloneTicketTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateTicketTestCase(GmpCreateTicketTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyTicketTestCase(GmpModifyTicketTestMixin, Gmpv214TestCase):
    pass
