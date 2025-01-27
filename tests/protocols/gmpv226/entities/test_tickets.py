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
from ...gmpv226 import GMPTestCase


class GMPDeleteTicketTestCase(GmpDeleteTicketTestMixin, GMPTestCase):
    pass


class GMPGetTicketTestCase(GmpGetTicketTestMixin, GMPTestCase):
    pass


class GMPGetTicketsTestCase(GmpGetTicketsTestMixin, GMPTestCase):
    pass


class GMPCloneTicketTestCase(GmpCloneTicketTestMixin, GMPTestCase):
    pass


class GMPCreateTicketTestCase(GmpCreateTicketTestMixin, GMPTestCase):
    pass


class GMPModifyTicketTestCase(GmpModifyTicketTestMixin, GMPTestCase):
    pass
