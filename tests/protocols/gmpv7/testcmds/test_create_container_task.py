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


class GMPCreateContainerTaskCommandTestCase:
    def test_create_task(self):
        self.gmp.create_container_task(name='foo')

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<target id="0"/>'
            '</create_task>'
        )

    def test_create_task_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_task(name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_task(name='')

    def test_create_task_with_comment(self):
        self.gmp.create_container_task(name='foo', comment='bar')

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<target id="0"/>'
            '<comment>bar</comment>'
            '</create_task>'
        )


if __name__ == '__main__':
    unittest.main()
