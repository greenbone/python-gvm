# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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


class GmpModifyScheduleTestMixin:
    def test_missing_schedule_id(self):
        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.modify_schedule(schedule_id=None)

        ex = cm.exception
        self.assertEqual(ex.argument, "schedule_id")

        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.modify_schedule(schedule_id="")

        ex = cm.exception
        self.assertEqual(ex.argument, "schedule_id")

    def test_modify_schedule_with_name(self):
        self.gmp.modify_schedule(schedule_id="s1", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_schedule schedule_id="s1">'
            b"<name>foo</name>"
            b"</modify_schedule>"
        )

    def test_modify_schedule_with_comment(self):
        self.gmp.modify_schedule(schedule_id="s1", comment="bar")

        self.connection.send.has_been_called_with(
            b'<modify_schedule schedule_id="s1">'
            b"<comment>bar</comment>"
            b"</modify_schedule>"
        )

    def test_modify_schedule_with_icalendar(self):
        self.gmp.modify_schedule(schedule_id="s1", icalendar=ICAL)

        self.connection.send.has_been_called_with(
            '<modify_schedule schedule_id="s1">'
            f"<icalendar>{ICAL}</icalendar>"
            "</modify_schedule>".encode("utf-8")
        )

    def test_modify_schedule_with_timezone(self):
        self.gmp.modify_schedule(schedule_id="s1", timezone="Europe/Berlin")

        self.connection.send.has_been_called_with(
            b'<modify_schedule schedule_id="s1">'
            b"<timezone>Europe/Berlin</timezone>"
            b"</modify_schedule>"
        )
