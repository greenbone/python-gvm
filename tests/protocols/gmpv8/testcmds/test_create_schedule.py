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

from gvm.errors import RequiredArgument


ICAL = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Greenbone.net//NONSGML Greenbone Security Manager 8.0.0//EN
BEGIN:VEVENT
UID:c35f82f1-7798-4b84-b2c4-761a33068956
DTSTAMP:20190715T124352Z
DTSTART:20190716T040000Z
END:VEVENT
END:VCALENDAR
"""


class GmpCreateScheduleTestCase:
    def test_missing_name(self):
        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name=None, icalendar=ICAL, timezone='UTC')

        ex = cm.exception
        self.assertEqual(ex.argument, "name")

        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name='', icalendar=ICAL, timezone='UTC')

        ex = cm.exception
        self.assertEqual(ex.argument, "name")

    def test_missing_icalendar(self):
        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name='foo', icalendar=None, timezone='UTC')

        ex = cm.exception
        self.assertEqual(ex.argument, "icalendar")

        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name='foo', icalendar='', timezone='UTC')

        ex = cm.exception
        self.assertEqual(ex.argument, "icalendar")

    def test_missing_timezone(self):
        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name='foo', icalendar=ICAL, timezone=None)

        ex = cm.exception
        self.assertEqual(ex.argument, "timezone")

        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name='foo', icalendar=ICAL, timezone='')

        ex = cm.exception
        self.assertEqual(ex.argument, "timezone")

    def test_create_schedule(self):
        self.gmp.create_schedule(
            name='foo', icalendar=ICAL, timezone='Europe/Berlin'
        )

        self.connection.send.has_been_called_with(
            "<create_schedule>"
            "<name>foo</name>"
            "<icalendar>{}</icalendar>"
            "<timezone>Europe/Berlin</timezone>"
            "</create_schedule>".format(ICAL)
        )

    def test_create_schedule_with_comment(self):
        self.gmp.create_schedule(
            name='foo', icalendar=ICAL, timezone='Europe/Berlin', comment="bar"
        )

        self.connection.send.has_been_called_with(
            "<create_schedule>"
            "<name>foo</name>"
            "<icalendar>{}</icalendar>"
            "<timezone>Europe/Berlin</timezone>"
            "<comment>bar</comment>"
            "</create_schedule>".format(ICAL)
        )


if __name__ == '__main__':
    unittest.main()
