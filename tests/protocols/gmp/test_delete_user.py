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

from gvm.errors import GvmError
from gvm.protocols.gmpv7 import Gmp

from .. import MockConnection


class GmpDeleteUserTestCase(unittest.TestCase):

    def setUp(self):
        self.connection = MockConnection()
        self.gmp = Gmp(self.connection)

    def test_delete(self):
        self.gmp.delete_user('a1', inheritor_id='u1')

        self.connection.send.has_been_called_with(
            '<delete_user user_id="a1" inheritor_id="u1"/>')

    def test_delete_with_name(self):
        self.gmp.delete_user('a1', name='foo', inheritor_id='u1')

        self.connection.send.has_been_called_with(
            '<delete_user user_id="a1" name="foo" inheritor_id="u1"/>')

    def test_delete_with_inheritor_name(self):
        self.gmp.delete_user('a1', inheritor_name='foo')

        self.connection.send.has_been_called_with(
            '<delete_user user_id="a1" inheritor_name="foo"/>')

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_user(None, inheritor_id='u1')

        with self.assertRaises(GvmError):
            self.gmp.delete_user('', inheritor_id='u1')

    def test_missing_inheritor(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_user('u1')


if __name__ == '__main__':
    unittest.main()
