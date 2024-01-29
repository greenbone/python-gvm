# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument
from gvm.protocols.gmpv208.entities.report_formats import ReportFormatType


class GmpCloneReportFormatTestMixin:
    def test_clone(self):
        self.gmp.clone_report_format("a1")

        self.connection.send.has_been_called_with(
            "<create_report_format><copy>a1</copy></create_report_format>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_report_format("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_report_format(None)

    def test_clone_with_type(self):
        self.gmp.clone_report_format(ReportFormatType.SVG)

        report_format_id = ReportFormatType.from_string("svg").value

        self.connection.send.has_been_called_with(
            "<create_report_format>"
            f"<copy>{report_format_id}</copy>"
            "</create_report_format>"
        )
