# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import sys
import unittest
from io import StringIO
from unittest.mock import patch

from pontos.testing import temp_directory

from gvm.errors import InvalidArgumentType
from gvm.xml import parse_xml, pretty_print


class PrettyPrintTestCase(unittest.TestCase):
    def test_pretty_print_to_file(self):
        xml_str = '<test><this><with id="a">and text</with></this></test>'
        elem = parse_xml(xml_str)
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
        elem = parse_xml(xml_str)
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
        elem = parse_xml(xml_str)
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
        elem = parse_xml(xml_str)
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
        elem = parse_xml(xml_str)
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
        elem = parse_xml(xml_str)

        with self.assertRaises(TypeError):
            pretty_print(elem, file="string")


if __name__ == "__main__":
    unittest.main()
