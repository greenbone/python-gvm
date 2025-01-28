# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.tickets import (
    GmpCloneTicketTestMixin,
    GmpCreateTicketTestMixin,
    GmpDeleteTicketTestMixin,
    GmpGetTicketsTestMixin,
    GmpGetTicketTestMixin,
    GmpModifyTicketTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225DeleteTicketTestCase(GmpDeleteTicketTestMixin, GMPTestCase):
    pass


class Gmpv225GetTicketTestCase(GmpGetTicketTestMixin, GMPTestCase):
    pass


class Gmpv225GetTicketsTestCase(GmpGetTicketsTestMixin, GMPTestCase):
    pass


class Gmpv225CloneTicketTestCase(GmpCloneTicketTestMixin, GMPTestCase):
    pass


class Gmpv225CreateTicketTestCase(GmpCreateTicketTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyTicketTestCase(GmpModifyTicketTestMixin, GMPTestCase):
    pass
