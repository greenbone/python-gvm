# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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
import datetime

from lxml import etree
from gvm.transforms.object.utils import (
    resolve_datetime,
    get_text,
    get_int,
    get_bool,
    get_subelement,
    get_text_from_element,
    get_int_from_element,
    get_bool_from_element,
    get_datetime_from_element,
)


class ObjectTransformUtilsTestCase(unittest.TestCase):
    def test_resolve_datetime(self):
        datetime_string = "2020-03-05T15:35:21Z"

        result1 = resolve_datetime(datetime_string)
        result2 = resolve_datetime(None)
        date = datetime.datetime(2020, 3, 5, 15, 35, 21)

        self.assertEqual(result1, date)
        self.assertEqual(result2, None)

    def test_get_text(self):
        element = etree.Element('test_text')
        element.text = "Test"

        result1 = get_text(element)
        result2 = get_text(None)

        self.assertEqual(result1, "Test")
        self.assertEqual(result2, None)

    def test_get_int(self):
        int_string = "1"
        false_string = "qwe23"

        result1 = get_int(int_string)
        result2 = get_int(false_string)
        result3 = get_int(None)

        self.assertEqual(result1, 1)
        self.assertEqual(result2, None)
        self.assertEqual(result3, None)

    def test_get_bool(self):
        true_string = "1"
        false_string = "0"

        result1 = get_bool(true_string)
        result2 = get_bool(false_string)
        result3 = get_bool(None)

        self.assertEqual(result1, True)
        self.assertEqual(result2, False)
        self.assertEqual(result3, None)

    def test_get_subelement(self):
        element = etree.Element('test_element')
        subelement = etree.Element('subelement')

        element.insert(0, subelement)

        result1 = get_subelement(element, 'subelement')
        result2 = get_subelement(None, '')

        self.assertEqual(subelement, result1)
        self.assertEqual(result2, None)

    def test_get_text_from_element(self):
        element = etree.Element('test_element')
        subelement = etree.Element('subelement')
        subelement.text = 'test'

        element.insert(0, subelement)

        result = get_text_from_element(element, 'subelement')

        self.assertEqual(result, 'test')

    def test_get_int_from_element(self):
        element = etree.Element('test_element')
        subelement = etree.Element('subelement')
        subelement.text = '1'

        element.insert(0, subelement)

        result = get_int_from_element(element, 'subelement')

        self.assertEqual(result, 1)

    def test_get_bool_from_element(self):
        element = etree.Element('test_element')
        subelement = etree.Element('subelement')
        subelement.text = '1'

        element.insert(0, subelement)

        result = get_bool_from_element(element, 'subelement')

        self.assertEqual(result, True)

    def test_get_datetime_from_element(self):
        element = etree.Element('test_element')
        subelement = etree.Element('subelement')
        subelement.text = '2020-03-05T15:35:21Z'

        element.insert(0, subelement)
        date = datetime.datetime(2020, 3, 5, 15, 35, 21)

        result = get_datetime_from_element(element, 'subelement')

        self.assertEqual(result, date)


if __name__ == "__main__":
    unittest.main()
