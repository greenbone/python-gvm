# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument
from gvm.protocols.gmpv208.entities.report_formats import ReportFormatType


class GmpModifyReportFormatTestMixin:
    def test_modify_report_format(self):
        self.gmp.modify_report_format(report_format_id="rf1")

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1"/>'
        )

    def test_modify_report_format_missing_report_format_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_report_format(report_format_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_report_format(report_format_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_report_format("")

    def test_modify_report_format_with_summary(self):
        self.gmp.modify_report_format(report_format_id="rf1", summary="foo")

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<summary>foo</summary>"
            "</modify_report_format>"
        )

    def test_modify_report_format_with_name(self):
        self.gmp.modify_report_format(report_format_id="rf1", name="foo")

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<name>foo</name>"
            "</modify_report_format>"
        )

    def test_modify_report_format_with_name_and_type(self):
        self.gmp.modify_report_format(
            report_format_id=ReportFormatType.XML, name="foo"
        )

        report_format_id = ReportFormatType.from_string("xml").value
        self.connection.send.has_been_called_with(
            f'<modify_report_format report_format_id="{report_format_id}">'
            "<name>foo</name></modify_report_format>"
        )

    def test_modify_report_format_with_active(self):
        self.gmp.modify_report_format(report_format_id="rf1", active=True)

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<active>1</active>"
            "</modify_report_format>"
        )

        self.gmp.modify_report_format(report_format_id="rf1", active=False)

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<active>0</active>"
            "</modify_report_format>"
        )

    def test_modify_report_format_with_param_name(self):
        self.gmp.modify_report_format(report_format_id="rf1", param_name="foo")

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<param>"
            "<name>foo</name>"
            "</param>"
            "</modify_report_format>"
        )

    def test_modify_report_format_with_param_name_and_value(self):
        self.gmp.modify_report_format(
            report_format_id="rf1", param_name="foo", param_value="bar"
        )

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<param>"
            "<name>foo</name>"
            "<value>bar</value>"
            "</param>"
            "</modify_report_format>"
        )

        self.gmp.modify_report_format(
            report_format_id="rf1", param_name="foo", param_value=""
        )

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<param>"
            "<name>foo</name>"
            "<value></value>"
            "</param>"
            "</modify_report_format>"
        )
