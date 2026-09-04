# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
from gvm.errors import RequiredArgument


class GmpGetReportExportTestMixin:
    def test_get_report_export_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_report_export(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_report_export("")

    def test_get_report_export_with_id(self):
        self.gmp.get_report_export(report_export_id="e1")

        self.connection.send.has_been_called_with(
            b'<get_report_exports report_export_id="e1"/>'
        )
