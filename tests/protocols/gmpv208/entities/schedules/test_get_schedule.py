# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetScheduleTestMixin:
    def test_get_schedule(self):
        self.gmp.get_schedule("s1")

        self.connection.send.has_been_called_with(
            b'<get_schedules schedule_id="s1"/>'
        )

        self.gmp.get_schedule(schedule_id="s1")

        self.connection.send.has_been_called_with(
            b'<get_schedules schedule_id="s1"/>'
        )

    def test_get_schedule_missing_schedule_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_schedule(schedule_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_schedule("")

    def test_get_schedules_with_tasks(self):
        self.gmp.get_schedule(schedule_id="s1", tasks=True)

        self.connection.send.has_been_called_with(
            b'<get_schedules schedule_id="s1" tasks="1"/>'
        )

        self.gmp.get_schedule(schedule_id="s1", tasks=False)

        self.connection.send.has_been_called_with(
            b'<get_schedules schedule_id="s1" tasks="0"/>'
        )
