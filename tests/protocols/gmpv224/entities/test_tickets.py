# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .tickets import (
    GmpCloneTicketTestMixin,
    GmpCreateTicketTestMixin,
    GmpDeleteTicketTestMixin,
    GmpGetTicketsTestMixin,
    GmpGetTicketTestMixin,
    GmpModifyTicketTestMixin,
)


class Gmpv224DeleteTicketTestCase(GmpDeleteTicketTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetTicketTestCase(GmpGetTicketTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetTicketsTestCase(GmpGetTicketsTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CloneTicketTestCase(GmpCloneTicketTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateTicketTestCase(GmpCreateTicketTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyTicketTestCase(GmpModifyTicketTestMixin, Gmpv224TestCase):
    pass
