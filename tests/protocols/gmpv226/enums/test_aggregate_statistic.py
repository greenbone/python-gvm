# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v226 import AggregateStatistic


class GetAggregateStatisticFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            AggregateStatistic.from_string("foo")

    def test_none_or_empty(self):
        ct = AggregateStatistic.from_string(None)
        self.assertIsNone(ct)
        ct = AggregateStatistic.from_string("")
        self.assertIsNone(ct)

    def test_count(self):
        ct = AggregateStatistic.from_string("count")
        self.assertEqual(ct, AggregateStatistic.COUNT)

    def test_c_count(self):
        ct = AggregateStatistic.from_string("c_count")
        self.assertEqual(ct, AggregateStatistic.C_COUNT)

    def test_c_sum(self):
        ct = AggregateStatistic.from_string("c_sum")
        self.assertEqual(ct, AggregateStatistic.C_SUM)

    def test_max(self):
        ct = AggregateStatistic.from_string("max")
        self.assertEqual(ct, AggregateStatistic.MAX)

    def test_mean(self):
        ct = AggregateStatistic.from_string("mean")
        self.assertEqual(ct, AggregateStatistic.MEAN)

    def test_min(self):
        ct = AggregateStatistic.from_string("min")
        self.assertEqual(ct, AggregateStatistic.MIN)

    def test_sum(self):
        ct = AggregateStatistic.from_string("sum")
        self.assertEqual(ct, AggregateStatistic.SUM)

    def test_text(self):
        ct = AggregateStatistic.from_string("text")
        self.assertEqual(ct, AggregateStatistic.TEXT)

    def test_value(self):
        ct = AggregateStatistic.from_string("value")
        self.assertEqual(ct, AggregateStatistic.VALUE)
