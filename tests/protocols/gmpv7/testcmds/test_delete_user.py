# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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


class GmpDeleteUserTestCase:
    def test_delete_user_with_user_id(self):
        self.gmp.delete_user('a1')

        self.connection.send.has_been_called_with('<delete_user user_id="a1"/>')

        self.gmp.delete_user(user_id='a1')

        self.connection.send.has_been_called_with('<delete_user user_id="a1"/>')

    def test_delete_user_with_inheritor_id(self):
        self.gmp.delete_user('a1', inheritor_id='u1')

        self.connection.send.has_been_called_with(
            '<delete_user user_id="a1" inheritor_id="u1"/>'
        )

    def test_delete_user_with_name(self):
        self.gmp.delete_user(name='foo')

        self.connection.send.has_been_called_with('<delete_user name="foo"/>')

    def test_delete_user_with_inheritor_name(self):
        self.gmp.delete_user('a1', inheritor_name='foo')

        self.connection.send.has_been_called_with(
            '<delete_user user_id="a1" inheritor_name="foo"/>'
        )

    def test_delete_user_missing_user_id_and_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.delete_user(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.delete_user('')

        with self.assertRaises(RequiredArgument):
            self.gmp.delete_user(user_id='', name='')


if __name__ == '__main__':
    unittest.main()
