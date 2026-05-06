# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetReportHostsTestMixin:
    def test_get_report_hosts_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_report_hosts(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_report_hosts("")

    def test_get_report_hosts_with_filter_string(self):
        self.gmp.get_report_hosts(report_id="r1", filter_string="name=foo")

        self.connection.send.has_been_called_with(
            b'<get_report_hosts report_id="r1" filter="name=foo" details="1"/>'
        )

    def test_get_report_hosts_with_filter_id(self):
        self.gmp.get_report_hosts(report_id="r1", filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_report_hosts report_id="r1" filt_id="f1" details="1"/>'
        )

    def test_get_report_hosts_with_ignore_pagination(self):
        self.gmp.get_report_hosts(report_id="r1", ignore_pagination=True)

        self.connection.send.has_been_called_with(
            b'<get_report_hosts report_id="r1" ignore_pagination="1" details="1"/>'
        )

        self.gmp.get_report_hosts(report_id="r1", ignore_pagination=False)

        self.connection.send.has_been_called_with(
            b'<get_report_hosts report_id="r1" ignore_pagination="0" details="1"/>'
        )

    def test_get_report_hosts_with_details(self):
        self.gmp.get_report_hosts(report_id="r1", details=True)

        self.connection.send.has_been_called_with(
            b'<get_report_hosts report_id="r1" details="1"/>'
        )

        self.gmp.get_report_hosts(report_id="r1", details=False)

        self.connection.send.has_been_called_with(
            b'<get_report_hosts report_id="r1" details="0"/>'
        )
