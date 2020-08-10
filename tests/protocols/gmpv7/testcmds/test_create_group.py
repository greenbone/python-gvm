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


class GmpCreateGroupTestCase:
    def test_create_group(self):
        self.gmp.create_group(name='foo')

        self.connection.send.has_been_called_with(
            '<create_group>' '<name>foo</name>' '</create_group>'
        )

    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_group(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_group('')

    def test_create_group_with_comment(self):
        self.gmp.create_group(name='foo', comment='bar')

        self.connection.send.has_been_called_with(
            '<create_group>'
            '<name>foo</name>'
            '<comment>bar</comment>'
            '</create_group>'
        )

    def test_create_special_group(self):
        self.gmp.create_group(name='foo', special=True)

        self.connection.send.has_been_called_with(
            '<create_group>'
            '<name>foo</name>'
            '<specials>'
            '<full/>'
            '</specials>'
            '</create_group>'
        )

    def test_create_group_with_users(self):
        self.gmp.create_group(name='foo', users=[])

        self.connection.send.has_been_called_with(
            '<create_group>' '<name>foo</name>' '</create_group>'
        )

        self.gmp.create_group(name='foo', users=['u1', 'u2'])

        self.connection.send.has_been_called_with(
            '<create_group>'
            '<name>foo</name>'
            '<users>u1,u2</users>'
            '</create_group>'
        )


if __name__ == '__main__':
    unittest.main()
