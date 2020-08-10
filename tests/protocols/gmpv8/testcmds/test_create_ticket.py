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


class GmpCreateTicketTestCase:
    def test_create_ticket(self):
        self.gmp.create_ticket(
            result_id='r1', assigned_to_user_id='u1', note='lorem ipsum'
        )

        self.connection.send.has_been_called_with(
            '<create_ticket>'
            '<result id="r1"/>'
            '<assigned_to>'
            '<user id="u1"/>'
            '</assigned_to>'
            '<open_note>lorem ipsum</open_note>'
            '</create_ticket>'
        )

    def test_create_ticket_with_comment(self):
        self.gmp.create_ticket(
            result_id='r1',
            assigned_to_user_id='u1',
            note='lorem ipsum',
            comment='bar',
        )

        self.connection.send.has_been_called_with(
            '<create_ticket>'
            '<result id="r1"/>'
            '<assigned_to>'
            '<user id="u1"/>'
            '</assigned_to>'
            '<open_note>lorem ipsum</open_note>'
            '<comment>bar</comment>'
            '</create_ticket>'
        )

    def test_create_ticket_missing_result_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_ticket(
                result_id='', assigned_to_user_id='u1', note='lorem ipsum'
            )

    def test_create_ticket_missing_assigned_to_user_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_ticket(
                result_id='r1', assigned_to_user_id='', note='lorem ipsum'
            )

    def test_create_ticket_missing_open_note(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_ticket(
                result_id='r1', assigned_to_user_id='u1', note=''
            )


if __name__ == '__main__':
    unittest.main()
