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
from gvm.protocols.gmpv208 import AlertCondition


class GetAlertConditionFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            AlertCondition.from_string("foo")

    def test_none_or_empty(self):
        ct = AlertCondition.from_string(None)
        self.assertIsNone(ct)
        ct = AlertCondition.from_string("")
        self.assertIsNone(ct)

    def test_always(self):
        ct = AlertCondition.from_string("always")
        self.assertEqual(ct, AlertCondition.ALWAYS)

    def test_filter_count_at_least(self):
        ct = AlertCondition.from_string("filter count at least")
        self.assertEqual(ct, AlertCondition.FILTER_COUNT_AT_LEAST)

    def test_filter_count_changed(self):
        ct = AlertCondition.from_string("filter count changed")
        self.assertEqual(ct, AlertCondition.FILTER_COUNT_CHANGED)

    def test_severity_at_least(self):
        ct = AlertCondition.from_string("severity at least")
        self.assertEqual(ct, AlertCondition.SEVERITY_AT_LEAST)

    def test_severity_changed(self):
        ct = AlertCondition.from_string("severity changed")
        self.assertEqual(ct, AlertCondition.SEVERITY_CHANGED)

    def test_error(self):
        ct = AlertCondition.from_string("error")
        self.assertEqual(ct, AlertCondition.ERROR)


if __name__ == "__main__":
    unittest.main()
