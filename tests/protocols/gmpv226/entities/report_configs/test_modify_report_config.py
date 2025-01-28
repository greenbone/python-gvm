# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from gvm.errors import RequiredArgument
from gvm.protocols.gmp._gmp226 import ReportConfigParameter


class GMPModifyReportConfigTestMixin:
    def test_modify_report_config(self):
        self.gmp.modify_report_config("report_config_id")

        self.connection.send.has_been_called_with(
            b'<modify_report_config report_config_id="report_config_id"/>',
        )

    def test_modify_report_config_with_name(self):
        self.gmp.modify_report_config("report_config_id", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_report_config report_config_id="report_config_id">'
            b"<name>foo</name>"
            b"</modify_report_config>",
        )

    def test_modify_report_config_with_comment(self):
        self.gmp.modify_report_config("report_config_id", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_report_config report_config_id="report_config_id">'
            b"<comment>foo</comment>"
            b"</modify_report_config>",
        )

    def test_modify_report_config_with_params(self):
        self.gmp.modify_report_config(
            "report_config_id",
            params=[
                ReportConfigParameter("name", "value"),
                ReportConfigParameter("name2", "value2", use_default=True),
                ReportConfigParameter("name3", use_default=True),
            ],
        )

        self.connection.send.has_been_called_with(
            b'<modify_report_config report_config_id="report_config_id">'
            b'<param><name>name</name><value use_default="0">value</value></param>'
            b'<param><name>name2</name><value use_default="1"/></param>'
            b'<param><name>name3</name><value use_default="1"/></param>'
            b"</modify_report_config>",
        )

    def test_modify_report_config_missing_report_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_report_config(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_report_config("")
