# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .tickets import (
    GmpCloneTicketTestMixin,
    GmpCreateTicketTestMixin,
    GmpDeleteTicketTestMixin,
    GmpGetTicketsTestMixin,
    GmpGetTicketTestMixin,
    GmpModifyTicketTestMixin,
)


class Gmpv208DeleteTicketTestCase(GmpDeleteTicketTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetTicketTestCase(GmpGetTicketTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetTicketsTestCase(GmpGetTicketsTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CloneTicketTestCase(GmpCloneTicketTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateTicketTestCase(GmpCreateTicketTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyTicketTestCase(GmpModifyTicketTestMixin, Gmpv208TestCase):
    pass
