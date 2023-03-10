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

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmpv224 import HelpFormat


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


if __name__ == "__main__":
    unittest.main()
