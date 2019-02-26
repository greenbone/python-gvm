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
from gvm.xml import validate_xml_string


class ValidXmlStringTestCase(unittest.TestCase):
    def test_missing_closing_tag(self):
        with self.assertRaises(GvmError):
            validate_xml_string('<foo>')

    def test_invalid_tag(self):
        with self.assertRaises(GvmError):
            validate_xml_string('<foo&bar/>')

    def test_xml_bomb(self):
        xml = (
            '<!DOCTYPE xmlbomb ['
            '<!ENTITY a "1234567890" >'
            '<!ENTITY b "&a;&a;&a;&a;&a;&a;&a;&a;">'
            '<!ENTITY c "&b;&b;&b;&b;&b;&b;&b;&b;">'
            '<!ENTITY d "&c;&c;&c;&c;&c;&c;&c;&c;">'
            ']>'
            '<bomb>&c;</bomb>'
        )
        with self.assertRaises(GvmError):
            validate_xml_string(xml)
