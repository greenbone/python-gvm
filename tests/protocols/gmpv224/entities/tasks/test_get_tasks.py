# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetTasksTestMixin:
    def test_get_tasks_simple(self):
        self.gmp.get_tasks()

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="scan"/>'
        )

    def test_get_tasks_with_filter_string(self):
        self.gmp.get_tasks(filter_string="name=foo")

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="scan" filter="name=foo"/>'
        )

    def test_get_tasks_with_filter_id(self):
        self.gmp.get_tasks(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="scan" filt_id="f1"/>'
        )

    def test_get_tasks_from_trash(self):
        self.gmp.get_tasks(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="scan" trash="1"/>'
        )

    def test_get_tasks_with_details(self):
        self.gmp.get_tasks(details=True)

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="scan" details="1"/>'
        )

    def test_get_tasks_without_details(self):
        self.gmp.get_tasks(details=False)

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="scan" details="0"/>'
        )

    def test_get_tasks_with_schedules_only(self):
        self.gmp.get_tasks(schedules_only=True)

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="scan" schedules_only="1"/>'
        )

    def test_get_tasks_with_ignore_pagination(self):
        self.gmp.get_tasks(ignore_pagination=True)

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="scan" ignore_pagination="1"/>'
        )

        self.gmp.get_tasks(ignore_pagination=False)

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="scan" ignore_pagination="0"/>'
        )
