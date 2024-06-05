# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetSchedulesTestMixin:
    def test_get_schedules(self):
        self.gmp.get_schedules()

        self.connection.send.has_been_called_with(b"<get_schedules/>")

    def test_get_schedules_with_filter_string(self):
        self.gmp.get_schedules(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_schedules filter="foo=bar"/>'
        )

    def test_get_schedules_with_filter_id(self):
        self.gmp.get_schedules(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_schedules filt_id="f1"/>'
        )

    def test_get_schedules_with_trash(self):
        self.gmp.get_schedules(trash=True)

        self.connection.send.has_been_called_with(b'<get_schedules trash="1"/>')

        self.gmp.get_schedules(trash=False)

        self.connection.send.has_been_called_with(b'<get_schedules trash="0"/>')

    def test_get_schedules_with_tasks(self):
        self.gmp.get_schedules(tasks=True)

        self.connection.send.has_been_called_with(b'<get_schedules tasks="1"/>')

        self.gmp.get_schedules(tasks=False)

        self.connection.send.has_been_called_with(b'<get_schedules tasks="0"/>')
