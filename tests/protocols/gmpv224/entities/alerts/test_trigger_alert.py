# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import ReportFormatType


class GmpTriggerAlertTestMixin:
    def test_trigger_alert_without_alert_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.trigger_alert(alert_id=None, report_id="r1")

        with self.assertRaises(RequiredArgument):
            self.gmp.trigger_alert(alert_id="", report_id="r1")

    def test_trigger_alert_without_report_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.trigger_alert(alert_id="a1", report_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.trigger_alert(alert_id="a1", report_id="")

    def test_trigger_alert(self):
        self.gmp.trigger_alert(alert_id="a1", report_id="r1")

        self.connection.send.has_been_called_with(
            b'<get_reports report_id="r1" alert_id="a1"/>'
        )

    def test_trigger_alert_with_filter_string(self):
        self.gmp.trigger_alert(
            alert_id="a1", report_id="r1", filter_string="name=foo"
        )

        self.connection.send.has_been_called_with(
            b'<get_reports report_id="r1" alert_id="a1" filter="name=foo"/>'
        )

    def test_trigger_alert_with_filter_id(self):
        self.gmp.trigger_alert(alert_id="a1", report_id="r1", filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_reports report_id="r1" alert_id="a1" filt_id="f1"/>'
        )

    def test_trigger_alert_with_report_format_id(self):
        self.gmp.trigger_alert(
            alert_id="a1", report_id="r1", report_format_id="bar"
        )

        self.connection.send.has_been_called_with(
            b'<get_reports report_id="r1" alert_id="a1" format_id="bar"/>'
        )

    def test_trigger_alert_with_report_format_type(self):
        self.gmp.trigger_alert(
            alert_id="a1", report_id="r1", report_format_id=ReportFormatType.SVG
        )

        self.connection.send.has_been_called_with(
            b'<get_reports report_id="r1" alert_id="a1" '
            b'format_id="9e5e5deb-879e-4ecc-8be6-a71cd0875cdd"/>'
        )

    def test_trigger_alert_with_delta_report_id(self):
        self.gmp.trigger_alert(
            alert_id="a1", report_id="r1", delta_report_id="r2"
        )

        self.connection.send.has_been_called_with(
            b'<get_reports report_id="r1" alert_id="a1" delta_report_id="r2"/>'
        )
