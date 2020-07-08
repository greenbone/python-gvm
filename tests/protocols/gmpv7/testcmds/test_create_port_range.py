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

from gvm.protocols.gmpv7 import PortRangeType


class GmpCreatePortRangeTestCase:
    def test_create_port_range_missing_port_list_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id=None,
                start=1,
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id='',
                start=1,
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

    def test_create_port_range_missing_start(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id='pl1',
                start=None,
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id='pl1',
                start='',
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

    def test_create_port_range_missing_end(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id='pl1',
                start=1,
                end=None,
                port_range_type=PortRangeType.TCP,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id='pl1',
                start=1,
                end='',
                port_range_type=PortRangeType.TCP,
            )

    def test_create_port_range_missing_port_range_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id='pl1', start=1, end=1234, port_range_type=None
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_range(
                port_list_id='pl1', start=1, end=1234, port_range_type=''
            )

    def test_create_port_range(self):
        self.gmp.create_port_range(
            port_list_id='pl1',
            start=1,
            end=1234,
            port_range_type=PortRangeType.TCP,
        )

        self.connection.send.has_been_called_with(
            '<create_port_range>'
            '<port_list id="pl1"/>'
            '<start>1</start>'
            '<end>1234</end>'
            '<type>TCP</type>'
            '</create_port_range>'
        )

        self.gmp.create_port_range(
            port_list_id='pl1',
            start=1,
            end=1234,
            port_range_type=PortRangeType.UDP,
        )

        self.connection.send.has_been_called_with(
            '<create_port_range>'
            '<port_list id="pl1"/>'
            '<start>1</start>'
            '<end>1234</end>'
            '<type>UDP</type>'
            '</create_port_range>'
        )

        self.gmp.create_port_range(
            port_list_id='pl1',
            start='1',
            end='1234',
            port_range_type=PortRangeType.TCP,
        )

        self.connection.send.has_been_called_with(
            '<create_port_range>'
            '<port_list id="pl1"/>'
            '<start>1</start>'
            '<end>1234</end>'
            '<type>TCP</type>'
            '</create_port_range>'
        )

    def test_create_port_range_with_comment(self):
        self.gmp.create_port_range(
            port_list_id='pl1',
            start=1,
            end=1234,
            port_range_type=PortRangeType.TCP,
            comment='lorem',
        )

        self.connection.send.has_been_called_with(
            '<create_port_range>'
            '<port_list id="pl1"/>'
            '<start>1</start>'
            '<end>1234</end>'
            '<type>TCP</type>'
            '<comment>lorem</comment>'
            '</create_port_range>'
        )


if __name__ == '__main__':
    unittest.main()
