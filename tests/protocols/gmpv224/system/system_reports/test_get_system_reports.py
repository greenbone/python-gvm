# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument


class GmpGetSystemReportsTestMixin:
    def test_get_system_reports(self):
        self.gmp.get_system_reports()

        self.connection.send.has_been_called_with(b"<get_system_reports/>")

    def test_get_system_reports_with_name(self):
        self.gmp.get_system_reports(name="foo")

        self.connection.send.has_been_called_with(
            b'<get_system_reports name="foo"/>'
        )

    def test_get_system_reports_with_slave_id(self):
        self.gmp.get_system_reports(slave_id="s1")

        self.connection.send.has_been_called_with(
            b'<get_system_reports slave_id="s1"/>'
        )

    def test_get_system_reports_with_brief(self):
        self.gmp.get_system_reports(brief=True)

        self.connection.send.has_been_called_with(
            b'<get_system_reports brief="1"/>'
        )

        self.gmp.get_system_reports(brief=False)

        self.connection.send.has_been_called_with(
            b'<get_system_reports brief="0"/>'
        )

    def test_get_system_reports_with_duration(self):
        self.gmp.get_system_reports(duration=3600)

        self.connection.send.has_been_called_with(
            b'<get_system_reports duration="3600"/>'
        )

    def test_get_system_reports_with_invalid_duration(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_system_reports(duration="")

    def test_get_system_reports_with_start_time(self):
        self.gmp.get_system_reports(start_time="01-01-2019")

        self.connection.send.has_been_called_with(
            b'<get_system_reports start_time="01-01-2019"/>'
        )

    def test_get_system_reports_with_end_time(self):
        self.gmp.get_system_reports(end_time="01-01-2019")

        self.connection.send.has_been_called_with(
            b'<get_system_reports end_time="01-01-2019"/>'
        )
