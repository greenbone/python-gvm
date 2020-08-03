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

from gvm.errors import RequiredArgument, InvalidArgumentType
from gvm.protocols.gmpv8 import TicketStatus


class GmpModifyTicketTestCase:
    def test_modify_ticket(self):
        self.gmp.modify_ticket('t1')

        self.connection.send.has_been_called_with(
            '<modify_ticket ticket_id="t1"/>'
        )

        self.gmp.modify_ticket(ticket_id='t1')

        self.connection.send.has_been_called_with(
            '<modify_ticket ticket_id="t1"/>'
        )

    def test_missing_ticket_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_ticket('')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_ticket(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_ticket(ticket_id=None)

    def test_modify_ticket_with_comment(self):
        self.gmp.modify_ticket(ticket_id='t1', comment='bar')

        self.connection.send.has_been_called_with(
            '<modify_ticket ticket_id="t1">'
            '<comment>bar</comment>'
            '</modify_ticket>'
        )

    def test_modify_ticket_with_assigned_to_user_id(self):
        self.gmp.modify_ticket(ticket_id='t1', assigned_to_user_id='u1')

        self.connection.send.has_been_called_with(
            '<modify_ticket ticket_id="t1">'
            '<assigned_to>'
            '<user id="u1"/>'
            '</assigned_to>'
            '</modify_ticket>'
        )

    def test_modify_ticket_invalid_status(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_ticket(ticket_id='t1', status='foobar', note='bar')

    def test_modify_ticket_open(self):
        self.gmp.modify_ticket(
            ticket_id='t1', status=TicketStatus.OPEN, note='lorem ipsum'
        )

        self.connection.send.has_been_called_with(
            '<modify_ticket ticket_id="t1">'
            '<status>Open</status>'
            '<open_note>lorem ipsum</open_note>'
            '</modify_ticket>'
        )

    def test_modify_ticket_fixed(self):
        self.gmp.modify_ticket(
            ticket_id='t1', status=TicketStatus.FIXED, note='lorem ipsum'
        )

        self.connection.send.has_been_called_with(
            '<modify_ticket ticket_id="t1">'
            '<status>Fixed</status>'
            '<fixed_note>lorem ipsum</fixed_note>'
            '</modify_ticket>'
        )

    def test_modify_ticket_closed(self):
        self.gmp.modify_ticket(
            ticket_id='t1', status=TicketStatus.CLOSED, note='lorem ipsum'
        )

        self.connection.send.has_been_called_with(
            '<modify_ticket ticket_id="t1">'
            '<status>Closed</status>'
            '<closed_note>lorem ipsum</closed_note>'
            '</modify_ticket>'
        )

    def test_modify_ticket_status_without_note(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_ticket(ticket_id='t1', status=TicketStatus.CLOSED)

    def test_modify_ticket_note_without_status(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_ticket(ticket_id='t1', note='foo')


if __name__ == '__main__':
    unittest.main()
