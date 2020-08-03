# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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

from gvm.errors import RequiredArgument, InvalidArgument, InvalidArgumentType

from gvm.protocols.gmpv7 import TimeUnit


class GmpCreateScheduleTestCase:
    def test_create_schedule(self):
        self.gmp.create_schedule(name='foo')

        self.connection.send.has_been_called_with(
            '<create_schedule>' '<name>foo</name>' '</create_schedule>'
        )

    def test_create_schedule_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_schedule(name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_schedule(name='')

    def test_create_schedule_with_comment(self):
        self.gmp.create_schedule(name='foo', comment='bar')

        self.connection.send.has_been_called_with(
            '<create_schedule>'
            '<name>foo</name>'
            '<comment>bar</comment>'
            '</create_schedule>'
        )

    def test_create_schedule_with_first_time_missing_minute(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_hour=10,
                first_time_day_of_month=1,
                first_time_month=1,
                first_time_year=2020,
            )

    def test_create_schedule_with_first_time_invalid_minute(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute='',
                first_time_hour=1,
                first_time_day_of_month=1,
                first_time_month=1,
                first_time_year=2020,
            )
        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=-1,
                first_time_hour=1,
                first_time_day_of_month=1,
                first_time_month=1,
                first_time_year=2020,
            )

    def test_create_schedule_with_first_time_missing_hour(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=10,
                first_time_day_of_month=1,
                first_time_month=1,
                first_time_year=2020,
            )

    def test_create_schedule_with_first_time_invalid_hour(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=10,
                first_time_hour='',
                first_time_day_of_month=1,
                first_time_month=1,
                first_time_year=2020,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=10,
                first_time_hour=-1,
                first_time_day_of_month=1,
                first_time_month=1,
                first_time_year=2020,
            )

    def test_create_schedule_with_first_time_missing_day_of_month(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_month=1,
                first_time_year=2020,
            )

    def test_create_schedule_with_first_time_invalid_day_of_month(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month='',
                first_time_month=1,
                first_time_year=2020,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month=0,
                first_time_month=1,
                first_time_year=2020,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month=-1,
                first_time_month=1,
                first_time_year=2020,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month=32,
                first_time_month=1,
                first_time_year=2020,
            )

    def test_create_schedule_with_first_time_missing_month(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month=1,
                first_time_year=2020,
            )

    def test_create_schedule_with_first_time_invalid_month(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month=1,
                first_time_month='',
                first_time_year=2020,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month=1,
                first_time_month=0,
                first_time_year=2020,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month=1,
                first_time_month=-1,
                first_time_year=2020,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month=1,
                first_time_month=13,
                first_time_year=2020,
            )

    def test_create_schedule_with_first_time_missing_year(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month=1,
                first_time_month=12,
            )

    def test_create_schedule_with_first_time_invalid_year(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month=1,
                first_time_month=1,
                first_time_year=1,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo',
                first_time_minute=0,
                first_time_hour=0,
                first_time_day_of_month=1,
                first_time_month=0,
                first_time_year=2020,
            )

    def test_create_schedule_with_first_time(self):
        self.gmp.create_schedule(
            name='foo',
            first_time_minute=0,
            first_time_hour=0,
            first_time_day_of_month=1,
            first_time_month=1,
            first_time_year=2020,
        )

        self.connection.send.has_been_called_with(
            '<create_schedule>'
            '<name>foo</name>'
            '<first_time>'
            '<minute>0</minute>'
            '<hour>0</hour>'
            '<day_of_month>1</day_of_month>'
            '<month>1</month>'
            '<year>2020</year>'
            '</first_time>'
            '</create_schedule>'
        )

    def test_create_schedule_invalid_duration(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo', duration='bar', duration_unit=TimeUnit.DAY
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo', duration=0, duration_unit=TimeUnit.DAY
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo', duration=-1, duration_unit=TimeUnit.DAY
            )

    def test_create_schedule_with_duration_missing_unit(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_schedule(name='foo', duration=1)

    def test_create_schedule_with_duration_invalid_unit(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_schedule(
                name='foo', duration=1, duration_unit='foo'
            )

    def test_create_schedule_with_duration(self):
        self.gmp.create_schedule(
            name='foo', duration=1, duration_unit=TimeUnit.DAY
        )

        self.connection.send.has_been_called_with(
            '<create_schedule>'
            '<name>foo</name>'
            '<duration>1'
            '<unit>day</unit>'
            '</duration>'
            '</create_schedule>'
        )

    def test_create_schedule_with_period_missing_unit(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_schedule(name='foo', period=1)

    def test_create_schedule_with_period_invalid_unit(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_schedule(name='foo', period=1, period_unit='foo')

    def test_create_schedule_invalid_period(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo', period='foo', period_unit=TimeUnit.DAY
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo', period=0.5, period_unit=TimeUnit.DAY
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_schedule(
                name='foo', period=-1, period_unit=TimeUnit.DAY
            )

    def test_create_schedule_with_period(self):
        self.gmp.create_schedule(name='foo', period=1, period_unit=TimeUnit.DAY)

        self.connection.send.has_been_called_with(
            '<create_schedule>'
            '<name>foo</name>'
            '<period>1'
            '<unit>day</unit>'
            '</period>'
            '</create_schedule>'
        )

    def test_create_schedule_with_timezone(self):
        self.gmp.create_schedule(name='foo', timezone='foo')

        self.connection.send.has_been_called_with(
            '<create_schedule>'
            '<name>foo</name>'
            '<timezone>foo</timezone>'
            '</create_schedule>'
        )


if __name__ == '__main__':
    unittest.main()
