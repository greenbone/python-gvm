# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v225 import AlertCondition


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
