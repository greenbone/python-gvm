# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import Schedules


class SchedulesTestUnit(unittest.TestCase):
    def test_clone_schedule(self):
        request = Schedules.clone_schedule("schedule_id")
        self.assertEqual(
            bytes(request),
            b"<create_schedule><copy>schedule_id</copy></create_schedule>",
        )

    def test_clone_schedule_missing_schedule_id(self):
        with self.assertRaises(RequiredArgument):
            Schedules.clone_schedule(None)

        with self.assertRaises(RequiredArgument):
            Schedules.clone_schedule("")

    def test_create_schedule(self):
        request = Schedules.create_schedule("name", "icalendar", "timezone")
        self.assertEqual(
            bytes(request),
            b"<create_schedule>"
            b"<name>name</name>"
            b"<icalendar>icalendar</icalendar>"
            b"<timezone>timezone</timezone>"
            b"</create_schedule>",
        )

    def test_create_schedule_with_comment(self):
        request = Schedules.create_schedule(
            "name", "icalendar", "timezone", comment="comment"
        )
        self.assertEqual(
            bytes(request),
            b"<create_schedule>"
            b"<name>name</name>"
            b"<icalendar>icalendar</icalendar>"
            b"<timezone>timezone</timezone>"
            b"<comment>comment</comment>"
            b"</create_schedule>",
        )

    def test_create_schedule_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Schedules.create_schedule(None, "icalendar", "timezone")

        with self.assertRaises(RequiredArgument):
            Schedules.create_schedule("", "icalendar", "timezone")

    def test_create_schedule_missing_icalendar(self):
        with self.assertRaises(RequiredArgument):
            Schedules.create_schedule("name", None, "timezone")

        with self.assertRaises(RequiredArgument):
            Schedules.create_schedule("name", "", "timezone")

    def test_create_schedule_missing_timezone(self):
        with self.assertRaises(RequiredArgument):
            Schedules.create_schedule("name", "icalendar", None)

        with self.assertRaises(RequiredArgument):
            Schedules.create_schedule("name", "icalendar", "")

    def test_delete_schedule(self):
        request = Schedules.delete_schedule("schedule_id")
        self.assertEqual(
            bytes(request),
            b'<delete_schedule schedule_id="schedule_id" ultimate="0"/>',
        )

    def test_delete_schedule_with_ultimate(self):
        request = Schedules.delete_schedule("schedule_id", ultimate=True)
        self.assertEqual(
            bytes(request),
            b'<delete_schedule schedule_id="schedule_id" ultimate="1"/>',
        )

        request = Schedules.delete_schedule("schedule_id", ultimate=False)
        self.assertEqual(
            bytes(request),
            b'<delete_schedule schedule_id="schedule_id" ultimate="0"/>',
        )

    def test_delete_schedule_missing_schedule_id(self):
        with self.assertRaises(RequiredArgument):
            Schedules.delete_schedule(None)

        with self.assertRaises(RequiredArgument):
            Schedules.delete_schedule("")

    def test_get_schedules(self):
        request = Schedules.get_schedules()
        self.assertEqual(bytes(request), b"<get_schedules/>")

    def test_get_schedules_with_filter_string(self):
        request = Schedules.get_schedules(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_schedules filter="filter_string"/>',
        )

    def test_get_schedules_with_filter_id(self):
        request = Schedules.get_schedules(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_schedules filt_id="filter_id"/>',
        )

    def test_get_schedules_with_trash(self):
        request = Schedules.get_schedules(trash=True)
        self.assertEqual(
            bytes(request),
            b'<get_schedules trash="1"/>',
        )

        request = Schedules.get_schedules(trash=False)
        self.assertEqual(
            bytes(request),
            b'<get_schedules trash="0"/>',
        )

    def test_get_schedules_with_tasks(self):
        request = Schedules.get_schedules(tasks=True)
        self.assertEqual(
            bytes(request),
            b'<get_schedules tasks="1"/>',
        )

        request = Schedules.get_schedules(tasks=False)
        self.assertEqual(
            bytes(request),
            b'<get_schedules tasks="0"/>',
        )

    def test_get_schedule(self):
        request = Schedules.get_schedule("schedule_id")
        self.assertEqual(
            bytes(request),
            b'<get_schedules schedule_id="schedule_id"/>',
        )

    def test_get_schedule_with_tasks(self):
        request = Schedules.get_schedule("schedule_id", tasks=True)
        self.assertEqual(
            bytes(request),
            b'<get_schedules schedule_id="schedule_id" tasks="1"/>',
        )

        request = Schedules.get_schedule("schedule_id", tasks=False)
        self.assertEqual(
            bytes(request),
            b'<get_schedules schedule_id="schedule_id" tasks="0"/>',
        )

    def test_get_schedule_missing_schedule_id(self):
        with self.assertRaises(RequiredArgument):
            Schedules.get_schedule(None)

        with self.assertRaises(RequiredArgument):
            Schedules.get_schedule("")

    def test_modify_schedule(self):
        request = Schedules.modify_schedule("schedule_id")
        self.assertEqual(
            bytes(request), b'<modify_schedule schedule_id="schedule_id"/>'
        )

    def test_modify_schedule_with_name(self):
        request = Schedules.modify_schedule("schedule_id", name="name")
        self.assertEqual(
            bytes(request),
            b'<modify_schedule schedule_id="schedule_id">'
            b"<name>name</name>"
            b"</modify_schedule>",
        )

    def test_modify_schedule_with_comment(self):
        request = Schedules.modify_schedule("schedule_id", comment="comment")
        self.assertEqual(
            bytes(request),
            b'<modify_schedule schedule_id="schedule_id">'
            b"<comment>comment</comment>"
            b"</modify_schedule>",
        )

    def test_modify_schedule_with_icalendar(self):
        request = Schedules.modify_schedule(
            "schedule_id", icalendar="icalendar"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_schedule schedule_id="schedule_id">'
            b"<icalendar>icalendar</icalendar>"
            b"</modify_schedule>",
        )

    def test_modify_schedule_with_timezone(self):
        request = Schedules.modify_schedule("schedule_id", timezone="timezone")
        self.assertEqual(
            bytes(request),
            b'<modify_schedule schedule_id="schedule_id">'
            b"<timezone>timezone</timezone>"
            b"</modify_schedule>",
        )

    def test_modify_schedule_missing_schedule_id(self):
        with self.assertRaises(RequiredArgument):
            Schedules.modify_schedule(None)

        with self.assertRaises(RequiredArgument):
            Schedules.modify_schedule("")
