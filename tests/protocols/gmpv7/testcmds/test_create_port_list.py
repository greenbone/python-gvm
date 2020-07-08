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


class GmpCreatePortListTestCase:
    def test_create_port_list_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_list(name=None, port_range='T:1-1234')

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_list(name='', port_range='T:1-1234')

    def test_create_port_list_missing_port_range(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_list(name='foo', port_range=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_list(name='foo', port_range='')

    def test_create_port_list(self):
        self.gmp.create_port_list(name='foo', port_range='T:1-1234')

        self.connection.send.has_been_called_with(
            '<create_port_list>'
            '<name>foo</name>'
            '<port_range>T:1-1234</port_range>'
            '</create_port_list>'
        )

    def test_create_port_list_with_comment(self):
        self.gmp.create_port_list(
            name='foo', port_range='T:1-1234', comment='lorem'
        )

        self.connection.send.has_been_called_with(
            '<create_port_list>'
            '<name>foo</name>'
            '<port_range>T:1-1234</port_range>'
            '<comment>lorem</comment>'
            '</create_port_list>'
        )


if __name__ == '__main__':
    unittest.main()
