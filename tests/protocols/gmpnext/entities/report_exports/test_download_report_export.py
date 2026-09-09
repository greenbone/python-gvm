# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
from gvm.errors import RequiredArgument


class GmpDownloadReportExportTestMixin:
    def test_download_report_export_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.download_report_export(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.download_report_export("")

    def test_download_report_export_with_id(self):
        self.gmp.download_report_export(report_export_id="e1")

        self.connection.send.has_been_called_with(
            b'<download_report_export report_export_id="e1"/>'
        )
