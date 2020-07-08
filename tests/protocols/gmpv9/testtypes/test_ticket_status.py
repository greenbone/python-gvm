# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmpv9 import TicketStatus, get_ticket_status_from_string


class GetTicketStatusFromStringTestCase(unittest.TestCase):
    def test_invalid_status(self):
        with self.assertRaises(InvalidArgument):
            get_ticket_status_from_string('foo')

    def test_none_or_empty_type(self):
        ts = get_ticket_status_from_string(None)
        self.assertIsNone(ts)
        ts = get_ticket_status_from_string('')
        self.assertIsNone(ts)

    def test_ticket_status_open(self):
        ts = get_ticket_status_from_string('open')
        self.assertEqual(ts, TicketStatus.OPEN)

    def test_ticket_status_fixed(self):
        ts = get_ticket_status_from_string('fixed')
        self.assertEqual(ts, TicketStatus.FIXED)

    def test_ticket_status_closed(self):
        ts = get_ticket_status_from_string('closed')
        self.assertEqual(ts, TicketStatus.CLOSED)
