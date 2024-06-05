# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v224 import Help, HelpFormat


class HelpTestCase(unittest.TestCase):
    def test_help(self):
        request = Help.help()

        self.assertEqual(bytes(request), b'<help type=""/>')

    def test_help_type_brief(self):
        request = Help.help(brief=True)

        self.assertEqual(bytes(request), b'<help type="brief"/>')

    def test_invalid_help_format(self):
        with self.assertRaises(InvalidArgument):
            Help.help(help_format="foo")

    def test_html_format(self):
        request = Help.help(help_format=HelpFormat.HTML)

        self.assertEqual(bytes(request), b'<help type="" format="html"/>')
