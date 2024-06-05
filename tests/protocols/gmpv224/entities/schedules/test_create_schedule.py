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


class GmpCreateScheduleTestMixin:
    def test_missing_name(self):
        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name=None, icalendar=ICAL, timezone="UTC")

        ex = cm.exception
        self.assertEqual(ex.argument, "name")

        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name="", icalendar=ICAL, timezone="UTC")

        ex = cm.exception
        self.assertEqual(ex.argument, "name")

    def test_missing_icalendar(self):
        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name="foo", icalendar=None, timezone="UTC")

        ex = cm.exception
        self.assertEqual(ex.argument, "icalendar")

        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name="foo", icalendar="", timezone="UTC")

        ex = cm.exception
        self.assertEqual(ex.argument, "icalendar")

    def test_missing_timezone(self):
        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name="foo", icalendar=ICAL, timezone=None)

        ex = cm.exception
        self.assertEqual(ex.argument, "timezone")

        with self.assertRaises(RequiredArgument) as cm:
            self.gmp.create_schedule(name="foo", icalendar=ICAL, timezone="")

        ex = cm.exception
        self.assertEqual(ex.argument, "timezone")

    def test_create_schedule(self):
        self.gmp.create_schedule(
            name="foo", icalendar=ICAL, timezone="Europe/Berlin"
        )

        self.connection.send.has_been_called_with(
            "<create_schedule>"
            "<name>foo</name>"
            f"<icalendar>{ICAL}</icalendar>"
            "<timezone>Europe/Berlin</timezone>"
            "</create_schedule>".encode("utf-8")
        )

    def test_create_schedule_with_comment(self):
        self.gmp.create_schedule(
            name="foo", icalendar=ICAL, timezone="Europe/Berlin", comment="bar"
        )

        self.connection.send.has_been_called_with(
            "<create_schedule>"
            "<name>foo</name>"
            f"<icalendar>{ICAL}</icalendar>"
            "<timezone>Europe/Berlin</timezone>"
            "<comment>bar</comment>"
            "</create_schedule>".encode("utf-8")
        )
