# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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
from gvm.protocols.gmpv7 import TimeUnit, get_time_unit_from_string


class GetTimeUnitFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            get_time_unit_from_string('foo')

    def test_none_or_empty(self):
        ct = get_time_unit_from_string(None)
        self.assertIsNone(ct)
        ct = get_time_unit_from_string('')
        self.assertIsNone(ct)

    def test_second(self):
        ct = get_time_unit_from_string('second')
        self.assertEqual(ct, TimeUnit.SECOND)

    def test_minute(self):
        ct = get_time_unit_from_string('minute')
        self.assertEqual(ct, TimeUnit.MINUTE)

    def test_hour(self):
        ct = get_time_unit_from_string('hour')
        self.assertEqual(ct, TimeUnit.HOUR)

    def test_day(self):
        ct = get_time_unit_from_string('day')
        self.assertEqual(ct, TimeUnit.DAY)

    def test_week(self):
        ct = get_time_unit_from_string('week')
        self.assertEqual(ct, TimeUnit.WEEK)

    def test_month(self):
        ct = get_time_unit_from_string('month')
        self.assertEqual(ct, TimeUnit.MONTH)

    def test_year(self):
        ct = get_time_unit_from_string('year')
        self.assertEqual(ct, TimeUnit.YEAR)

    def test_decade(self):
        ct = get_time_unit_from_string('decade')
        self.assertEqual(ct, TimeUnit.DECADE)


if __name__ == '__main__':
    unittest.main()
