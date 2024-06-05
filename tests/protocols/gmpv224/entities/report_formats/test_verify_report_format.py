# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError
from gvm.protocols.gmp.requests.v224 import ReportFormatType


class GmpVerifyReportFormatTestMixin:
    def test_verify(self):
        self.gmp.verify_report_format("a1")

        self.connection.send.has_been_called_with(
            b'<verify_report_format report_format_id="a1"/>'
        )

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.verify_report_format(None)

        with self.assertRaises(GvmError):
            self.gmp.verify_report_format("")

    def test_verify_with_type(self):
        self.gmp.verify_report_format(ReportFormatType.SVG)

        report_format_id = ReportFormatType.from_string("svg").value
        self.connection.send.has_been_called_with(
            f'<verify_report_format report_format_id="{report_format_id}"/>'.encode(
                "utf-8"
            )
        )
