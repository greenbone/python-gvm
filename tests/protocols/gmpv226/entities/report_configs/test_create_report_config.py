# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument
from gvm.protocols.gmp._gmp226 import ReportConfigParameter


class GMPCreateReportConfigTestMixin:
    def test_create_report_config(self):
        self.gmp.create_report_config("r1", "report_format_id")

        self.connection.send.has_been_called_with(
            b"<create_report_config>"
            b"<name>r1</name>"
            b'<report_format id="report_format_id"/>'
            b"</create_report_config>"
        )

    def test_create_report_config_with_comment(self):
        self.gmp.create_report_config("r1", "report_format_id", comment="foo")

        self.connection.send.has_been_called_with(
            b"<create_report_config>"
            b"<name>r1</name>"
            b'<report_format id="report_format_id"/>'
            b"<comment>foo</comment>"
            b"</create_report_config>"
        )

    def test_create_report_config_with_params(self):
        self.gmp.create_report_config(
            "r1",
            "report_format_id",
            params=[
                ReportConfigParameter("name", "value"),
                ReportConfigParameter("name2", "value2", use_default=True),
                ReportConfigParameter("name3", use_default=True),
            ],
        )

        self.connection.send.has_been_called_with(
            b"<create_report_config>"
            b"<name>r1</name>"
            b'<report_format id="report_format_id"/>'
            b'<param><name>name</name><value use_default="0">value</value></param>'
            b'<param><name>name2</name><value use_default="1"/></param>'
            b'<param><name>name3</name><value use_default="1"/></param>'
            b"</create_report_config>",
        )

    def test_create_report_config_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_report_config(None, "report_format_id")

        with self.assertRaises(RequiredArgument):
            self.gmp.create_report_config("", "report_format_id")

    def test_create_report_config_missing_report_format_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_report_config("r1", None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_report_config("r1", "")
