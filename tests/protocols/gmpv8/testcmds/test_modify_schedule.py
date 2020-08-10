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


class GmpModifyScheduleTestCase:
    def test_missing_schedule_id(self):
        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.modify_schedule(schedule_id=None)

        ex = cm.exception
        self.assertEqual(ex.argument, "schedule_id")

        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.modify_schedule(schedule_id='')

        ex = cm.exception
        self.assertEqual(ex.argument, "schedule_id")

    def test_modify_schedule_with_name(self):
        self.gmp.modify_schedule(schedule_id='s1', name='foo')

        self.connection.send.has_been_called_with(
            '<modify_schedule schedule_id="s1">'
            "<name>foo</name>"
            "</modify_schedule>"
        )

    def test_modify_schedule_with_comment(self):
        self.gmp.modify_schedule(schedule_id="s1", comment="bar")

        self.connection.send.has_been_called_with(
            '<modify_schedule schedule_id="s1">'
            "<comment>bar</comment>"
            "</modify_schedule>"
        )

    def test_modify_schedule_with_icalendar(self):
        self.gmp.modify_schedule(schedule_id="s1", icalendar=ICAL)

        self.connection.send.has_been_called_with(
            '<modify_schedule schedule_id="s1">'
            '<icalendar>{}</icalendar>'
            "</modify_schedule>".format(ICAL)
        )

    def test_modify_schedule_with_timezone(self):
        self.gmp.modify_schedule(schedule_id="s1", timezone="Europe/Berlin")

        self.connection.send.has_been_called_with(
            '<modify_schedule schedule_id="s1">'
            '<timezone>Europe/Berlin</timezone>'
            "</modify_schedule>"
        )


if __name__ == '__main__':
    unittest.main()
