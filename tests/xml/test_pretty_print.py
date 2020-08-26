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

import defusedxml.lxml as secET

from gvm.xml import pretty_print


class PrettyPrintTestCase(unittest.TestCase):
    def test_pretty_print(self):
        xml_str = '<test><this><with id="a">and text</with></this></test>'
        elem = secET.fromstring(xml_str)
        expected_xml_string = (
            '<test>\n'
            '  <this>\n'
            '    <with id="a">and text</with>\n'
            '  </this>\n'
            '</test>\n'
            '\n'
        )

        pretty_print(elem, file='test.file')

        with open('test.file', 'r') as f:
            xml_string = f.read()

        self.assertEqual(xml_string, expected_xml_string)


if __name__ == '__main__':
    unittest.main()
