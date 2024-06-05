# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError
from gvm.protocols.gmp.requests.v224 import ReportFormatType


class GmpDeleteReportFormatTestMixin:
    def test_delete(self):
        self.gmp.delete_report_format("a1")

        self.connection.send.has_been_called_with(
            b'<delete_report_format report_format_id="a1" ultimate="0"/>'
        )

    def test_delete_ultimate(self):
        self.gmp.delete_report_format("a1", ultimate=True)

        self.connection.send.has_been_called_with(
            b'<delete_report_format report_format_id="a1" ultimate="1"/>'
        )

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_report_format(None)

        with self.assertRaises(GvmError):
            self.gmp.delete_report_format("")

    def test_delete_with_type(self):
        self.gmp.delete_report_format(ReportFormatType.SVG)

        report_format_id = ReportFormatType.from_string("svg").value
        self.connection.send.has_been_called_with(
            "<delete_report_format "
            f'report_format_id="{report_format_id}" ultimate="0"/>'.encode(
                "utf-8"
            )
        )
