# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import ReportFormatType


class GmpGetReportFormatTestMixin:
    def test_get_report_format(self):
        self.gmp.get_report_format("rf1")

        self.connection.send.has_been_called_with(
            b'<get_report_formats report_format_id="rf1" details="1"/>'
        )

        self.gmp.get_report_format(report_format_id="rf1")

        self.connection.send.has_been_called_with(
            b'<get_report_formats report_format_id="rf1" details="1"/>'
        )

    def test_get_report_format_missing_report_format_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_report_format(report_format_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_report_format("")

    def test_get_report_format_type(self):
        self.gmp.get_report_format(ReportFormatType.PDF)
        report_format_id = ReportFormatType.from_string("pdf").value
        self.connection.send.has_been_called_with(
            "<get_report_formats "
            f'report_format_id="{report_format_id}" details="1"/>'.encode(
                "utf-8"
            )
        )

        self.gmp.get_report_format(report_format_id=ReportFormatType.PDF)

        self.connection.send.has_been_called_with(
            "<get_report_formats "
            f'report_format_id="{report_format_id}" details="1"/>'.encode(
                "utf-8"
            )
        )
