# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Greenbone AG
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

import sys
import unittest
from io import StringIO
from unittest.mock import patch

import defusedxml.lxml as secET
from pontos.testing import temp_directory

from gvm.errors import InvalidArgumentType
from gvm.xml import pretty_print


class PrettyPrintTestCase(unittest.TestCase):
    def test_pretty_print_to_file(self):
        xml_str = '<test><this><with id="a">and text</with></this></test>'
        elem = secET.fromstring(xml_str)
        expected_xml_string = (
            "<test>\n"
            "  <this>\n"
            '    <with id="a">and text</with>\n'
            "  </this>\n"
            "</test>\n"
        )

        with temp_directory() as temp_dir:
            test_file = temp_dir / "test.file"
            with test_file.open("w", encoding="utf-8") as f:
                pretty_print(elem, file=f)

            xml_string = test_file.read_text(encoding="utf-8")

        self.assertEqual(xml_string, expected_xml_string)

    def test_pretty_print_to_stringio(self):
        xml_str = '<test><this><with id="a">and text</with></this></test>'
        elem = secET.fromstring(xml_str)
        expected_xml_string = (
            "<test>\n"
            "  <this>\n"
            '    <with id="a">and text</with>\n'
            "  </this>\n"
            "</test>\n"
        )

        stringio = StringIO()
        pretty_print(elem, file=stringio)

        xml_string = stringio.getvalue()

        self.assertEqual(xml_string, expected_xml_string)

    # I don't know why: But this test is only working if sys.stdout is passed.
    # But printing to sys.stdout is working, too using the default argument ...
    @patch("sys.stdout", new_callable=StringIO)
    def test_pretty_print_to_stdout(self, mock_stdout):
        xml_str = '<test><this><with id="a">and text</with></this></test>'
        elem = secET.fromstring(xml_str)
        expected_xml_string = (
            "<test>\n"
            "  <this>\n"
            '    <with id="a">and text</with>\n'
            "  </this>\n"
            "</test>\n"
        )

        pretty_print(elem, sys.stdout)
        xml_string = mock_stdout.getvalue()

        self.assertEqual(xml_string, expected_xml_string)

    def test_pretty_print_with_string(self):
        xml_str = '<test><this><with id="a">and text</with></this></test>'

        expected_xml_string = (
            "<test>\n"
            "  <this>\n"
            '    <with id="a">and text</with>\n'
            "  </this>\n"
            "</test>\n"
        )

        stringio = StringIO()
        pretty_print(xml_str, file=stringio)

        xml_string = stringio.getvalue()

        self.assertEqual(xml_string, expected_xml_string)

    @patch("sys.stdout", new_callable=StringIO)
    def test_pretty_print_with_string_to_stdout(self, mock_stdout):
        xml_str = '<test><this><with id="a">and text</with></this></test>'

        expected_xml_string = (
            "<test>\n"
            "  <this>\n"
            '    <with id="a">and text</with>\n'
            "  </this>\n"
            "</test>\n"
        )

        pretty_print(xml_str, sys.stdout)
        xml_string = mock_stdout.getvalue()

        self.assertEqual(xml_string, expected_xml_string)

    def test_pretty_print_with_dict(self):
        xml_str = '<test><this><with id="a">and text</with></this></test>'
        elem = secET.fromstring(xml_str)
        expected_xml_string = (
            "<test>\n"
            "  <this>\n"
            '    <with id="a">and text</with>\n'
            "  </this>\n"
            "</test>\n"
            "<test>\n"
            "  <this>\n"
            '    <with id="a">and text</with>\n'
            "  </this>\n"
            "</test>\n"
        )

        stringio = StringIO()
        pretty_print([elem, elem], file=stringio)

        xml_string = stringio.getvalue()

        self.assertEqual(xml_string, expected_xml_string)

    def test_pretty_print_with_dict_str(self):
        xml_str = '<test><this><with id="a">and text</with></this></test>'
        no_xml = "</test>"
        elem = secET.fromstring(xml_str)
        expected_xml_string = (
            "<test>\n"
            "  <this>\n"
            '    <with id="a">and text</with>\n'
            "  </this>\n"
            "</test>\n"
            "</test>\n"
        )

        stringio = StringIO()
        pretty_print([elem, no_xml], file=stringio)

        xml_string = stringio.getvalue()

        self.assertEqual(xml_string, expected_xml_string)

    def test_pretty_print_no_xml(self):
        number = 1
        stringio = StringIO()

        with self.assertRaises(InvalidArgumentType):
            pretty_print(number, file=stringio)

    def test_pretty_print_type_error(self):
        xml_str = '<test><this><with id="a">and text</with></this></test>'
        elem = secET.fromstring(xml_str)

        with self.assertRaises(TypeError):
            pretty_print(elem, file="string")


if __name__ == "__main__":
    unittest.main()
