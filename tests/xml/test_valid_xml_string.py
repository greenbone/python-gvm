# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import GvmError
from gvm.xml import validate_xml_string


class ValidXmlStringTestCase(unittest.TestCase):
    def test_missing_closing_tag(self):
        with self.assertRaises(GvmError):
            validate_xml_string("<foo>")

    def test_invalid_tag(self):
        with self.assertRaises(GvmError):
            validate_xml_string("<foo&bar/>")

    def test_xml_bomb(self):
        xml = (
            "<!DOCTYPE xmlbomb ["
            '<!ENTITY a "1234567890" >'
            '<!ENTITY b "&a;&a;&a;&a;&a;&a;&a;&a;">'
            '<!ENTITY c "&b;&b;&b;&b;&b;&b;&b;&b;">'
            '<!ENTITY d "&c;&c;&c;&c;&c;&c;&c;&c;">'
            "]>"
            "<bomb>&c;</bomb>"
        )
        with self.assertRaises(GvmError):
            validate_xml_string(xml)
