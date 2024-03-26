# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.protocols.core._connection import XmlReader


class XmlReaderTestCase(unittest.TestCase):
    def test_is_end_xml_false(self):
        reader = XmlReader()
        reader.start_xml()

        false = reader.is_end_xml()
        self.assertFalse(false)
