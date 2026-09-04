# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetReportExportTestMixin:
    def test_get_report_export_without_id(self):
        self.gmp.get_report_export()

        self.connection.send.has_been_called_with(b"<get_report_exports/>")

    def test_get_report_export_with_id(self):
        self.gmp.get_report_export(report_export_id="e1")

        self.connection.send.has_been_called_with(
            b'<get_report_exports report_export_id="e1"/>'
        )
