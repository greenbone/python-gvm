# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument
from gvm.protocols.gmpv208.entities.report_formats import ReportFormatType


class GmpGetReportTestMixin:
    def test_get_report_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_report(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_report("")

    def test_get_report_with_filter_string(self):
        self.gmp.get_report(report_id="r1", filter_string="name=foo")

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" filter="name=foo" details="1"/>'
        )

    def test_get_report_with_filter_id(self):
        self.gmp.get_report(report_id="r1", filter_id="f1")

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" filt_id="f1" details="1"/>'
        )

    def test_get_report_with_report_format_id(self):
        self.gmp.get_report(report_id="r1", report_format_id="bar")

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" format_id="bar" details="1"/>'
        )

    def test_get_report_with_report_format_type(self):
        self.gmp.get_report(
            report_id="r1", report_format_id=ReportFormatType.TXT
        )
        report_format_id = ReportFormatType.from_string("txt").value

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" format_id='
            f'"{report_format_id}" details="1"/>'
        )

    def test_get_report_with_delta_report_id(self):
        self.gmp.get_report(report_id="r1", delta_report_id="r2")

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" delta_report_id="r2" details="1"/>'
        )

    def test_get_report_with_ignore_pagination(self):
        self.gmp.get_report(report_id="r1", ignore_pagination=True)

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" ignore_pagination="1" details="1"/>'
        )

        self.gmp.get_report(report_id="r1", ignore_pagination=False)

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" ignore_pagination="0" details="1"/>'
        )

    def test_get_report_with_details(self):
        self.gmp.get_report(report_id="r1", details=True)

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" details="1"/>'
        )

        self.gmp.get_report(report_id="r1", details=False)

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" details="0"/>'
        )
