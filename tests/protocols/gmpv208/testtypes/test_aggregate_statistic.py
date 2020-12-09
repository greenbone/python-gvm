# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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
from gvm.protocols.gmpv208 import (
    AggregateStatistic,
    get_aggregate_statistic_from_string,
)


class GetAggregateStatisticFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            get_aggregate_statistic_from_string('foo')

    def test_none_or_empty(self):
        ct = get_aggregate_statistic_from_string(None)
        self.assertIsNone(ct)
        ct = get_aggregate_statistic_from_string('')
        self.assertIsNone(ct)


class GetAggregateStatisticFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            get_aggregate_statistic_from_string('foo')

    def test_none_or_empty(self):
        ct = get_aggregate_statistic_from_string(None)
        self.assertIsNone(ct)
        ct = get_aggregate_statistic_from_string('')
        self.assertIsNone(ct)

    def test_count(self):
        ct = get_aggregate_statistic_from_string('count')
        self.assertEqual(ct, AggregateStatistic.COUNT)

    def test_c_count(self):
        ct = get_aggregate_statistic_from_string('c_count')
        self.assertEqual(ct, AggregateStatistic.C_COUNT)

    def test_c_sum(self):
        ct = get_aggregate_statistic_from_string('c_sum')
        self.assertEqual(ct, AggregateStatistic.C_SUM)

    def test_max(self):
        ct = get_aggregate_statistic_from_string('max')
        self.assertEqual(ct, AggregateStatistic.MAX)

    def test_mean(self):
        ct = get_aggregate_statistic_from_string('mean')
        self.assertEqual(ct, AggregateStatistic.MEAN)

    def test_min(self):
        ct = get_aggregate_statistic_from_string('min')
        self.assertEqual(ct, AggregateStatistic.MIN)

    def test_sum(self):
        ct = get_aggregate_statistic_from_string('sum')
        self.assertEqual(ct, AggregateStatistic.SUM)

    def test_text(self):
        ct = get_aggregate_statistic_from_string('text')
        self.assertEqual(ct, AggregateStatistic.TEXT)

    def test_value(self):
        ct = get_aggregate_statistic_from_string('value')
        self.assertEqual(ct, AggregateStatistic.VALUE)


if __name__ == '__main__':
    unittest.main()
