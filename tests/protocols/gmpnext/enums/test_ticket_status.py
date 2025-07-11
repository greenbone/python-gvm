# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v226 import TicketStatus


class GetTicketStatusFromStringTestCase(unittest.TestCase):
    def test_invalid_status(self):
        with self.assertRaises(InvalidArgument):
            TicketStatus.from_string("foo")

    def test_none_or_empty_type(self):
        ts = TicketStatus.from_string(None)
        self.assertIsNone(ts)
        ts = TicketStatus.from_string("")
        self.assertIsNone(ts)

    def test_ticket_status_open(self):
        ts = TicketStatus.from_string("open")
        self.assertEqual(ts, TicketStatus.OPEN)

    def test_ticket_status_fixed(self):
        ts = TicketStatus.from_string("fixed")
        self.assertEqual(ts, TicketStatus.FIXED)

    def test_ticket_status_closed(self):
        ts = TicketStatus.from_string("closed")
        self.assertEqual(ts, TicketStatus.CLOSED)
