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


class GmpAuthenticateTestCase:
    def test_missing_username(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.authenticate(None, 'foo')

        with self.assertRaises(RequiredArgument):
            self.gmp.authenticate('', 'foo')

    def test_missing_password(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.authenticate('bar', None)

        with self.assertRaises(RequiredArgument):
            self.gmp.authenticate('bar', '')

    def test_authentication_success(self):
        self.assertFalse(self.gmp.is_authenticated())

        self.gmp.authenticate('foo', 'bar')

        self.connection.send.has_been_called_with(
            '<authenticate>'
            '<credentials>'
            '<username>foo</username>'
            '<password>bar</password>'
            '</credentials>'
            '</authenticate>'
        )

        self.assertTrue(self.gmp.is_authenticated())

    def test_authentication_failure(self):
        self.connection.read.return_value(
            '<authentication_response status="400" status_text="Auth failed"/>'
        )

        self.assertFalse(self.gmp.is_authenticated())

        self.gmp.authenticate('foo', 'bar')

        self.connection.send.has_been_called_with(
            '<authenticate>'
            '<credentials>'
            '<username>foo</username>'
            '<password>bar</password>'
            '</credentials>'
            '</authenticate>'
        )

        self.assertFalse(self.gmp.is_authenticated())


if __name__ == '__main__':
    unittest.main()
