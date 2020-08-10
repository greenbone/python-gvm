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


class GmpModifyPortListTestCase:
    def test_modify_port_list(self):
        self.gmp.modify_port_list(port_list_id='p1')

        self.connection.send.has_been_called_with(
            '<modify_port_list port_list_id="p1"/>'
        )

    def test_modify_port_list_missing_port_list_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_port_list(port_list_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_port_list(port_list_id='')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_port_list('')

    def test_modify_port_list_with_comment(self):
        self.gmp.modify_port_list(port_list_id='p1', comment='foo')

        self.connection.send.has_been_called_with(
            '<modify_port_list port_list_id="p1">'
            '<comment>foo</comment>'
            '</modify_port_list>'
        )

    def test_modify_port_list_with_name(self):
        self.gmp.modify_port_list(port_list_id='p1', name='foo')

        self.connection.send.has_been_called_with(
            '<modify_port_list port_list_id="p1">'
            '<name>foo</name>'
            '</modify_port_list>'
        )


if __name__ == '__main__':
    unittest.main()
