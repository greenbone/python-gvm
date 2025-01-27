# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v226 import HelpFormat


class GetHelpFormatFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            HelpFormat.from_string("foo")

    def test_none_or_empty(self):
        ct = HelpFormat.from_string(None)
        self.assertIsNone(ct)
        ct = HelpFormat.from_string("")
        self.assertIsNone(ct)

    def test_task_run_status_changed(self):
        ct = HelpFormat.from_string("HtMl")
        self.assertEqual(ct, HelpFormat.HTML)

    def test_new_secinfo_arrived(self):
        ct = HelpFormat.from_string("rNc")
        self.assertEqual(ct, HelpFormat.RNC)

    def test_updated_secinfo_arrived(self):
        ct = HelpFormat.from_string("tExT")
        self.assertEqual(ct, HelpFormat.TEXT)

    def test_ticket_received(self):
        ct = HelpFormat.from_string("XmL")
        self.assertEqual(ct, HelpFormat.XML)
