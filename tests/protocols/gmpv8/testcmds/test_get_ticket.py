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

from gvm.errors import RequiredArgument


class GmpGetTicketTestCase:
    def test_get_ticket(self):
        self.gmp.get_ticket('t1')

        self.connection.send.has_been_called_with(
            '<get_tickets ticket_id="t1"/>'
        )

        self.gmp.get_ticket(ticket_id='t1')

        self.connection.send.has_been_called_with(
            '<get_tickets ticket_id="t1"/>'
        )

    def test_get_ticket_missing_user_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_ticket(ticket_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_ticket('')


if __name__ == '__main__':
    unittest.main()
