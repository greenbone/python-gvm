# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpExportScanReportTestMixin:
    def test_export_scan_report_without_report_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.export_scan_report(None, format_id="f1")

        with self.assertRaises(RequiredArgument):
            self.gmp.export_scan_report("", format_id="f1")

    def test_export_scan_report(self):
        self.gmp.export_scan_report(
            report_id="r1",
            format_id="f1",
        )

        self.connection.send.has_been_called_with(
            b'<export_scan_report report_id="r1" format_id="f1" '
            b'ignore_pagination="0" lean="0" notes_details="0" '
            b'overrides_details="0" result_tags="0"/>'
        )

    def test_export_scan_report_with_config_id(self):
        self.gmp.export_scan_report(
            report_id="r1",
            format_id="f1",
            config_id="c1",
        )

        self.connection.send.has_been_called_with(
            b'<export_scan_report report_id="r1" format_id="f1" '
            b'config_id="c1" ignore_pagination="0" lean="0" '
            b'notes_details="0" overrides_details="0" result_tags="0"/>'
        )

    def test_export_scan_report_with_filter_string(self):
        self.gmp.export_scan_report(
            report_id="r1",
            format_id="f1",
            filter_string="levels=hml",
        )

        self.connection.send.has_been_called_with(
            b'<export_scan_report report_id="r1" format_id="f1" '
            b'filter="levels=hml" ignore_pagination="0" lean="0" '
            b'notes_details="0" overrides_details="0" result_tags="0"/>'
        )

    def test_export_scan_report_with_ignore_pagination(self):
        self.gmp.export_scan_report(
            report_id="r1",
            format_id="f1",
            ignore_pagination=True,
        )

        self.connection.send.has_been_called_with(
            b'<export_scan_report report_id="r1" format_id="f1" '
            b'ignore_pagination="1" lean="0" notes_details="0" '
            b'overrides_details="0" result_tags="0"/>'
        )

    def test_export_scan_report_with_lean(self):
        self.gmp.export_scan_report(
            report_id="r1",
            format_id="f1",
            lean=True,
        )

        self.connection.send.has_been_called_with(
            b'<export_scan_report report_id="r1" format_id="f1" '
            b'ignore_pagination="0" lean="1" notes_details="0" '
            b'overrides_details="0" result_tags="0"/>'
        )

    def test_export_scan_report_with_notes_details(self):
        self.gmp.export_scan_report(
            report_id="r1",
            format_id="f1",
            notes_details=True,
        )

        self.connection.send.has_been_called_with(
            b'<export_scan_report report_id="r1" format_id="f1" '
            b'ignore_pagination="0" lean="0" notes_details="1" '
            b'overrides_details="0" result_tags="0"/>'
        )

    def test_export_scan_report_with_overrides_details(self):
        self.gmp.export_scan_report(
            report_id="r1",
            format_id="f1",
            overrides_details=True,
        )

        self.connection.send.has_been_called_with(
            b'<export_scan_report report_id="r1" format_id="f1" '
            b'ignore_pagination="0" lean="0" notes_details="0" '
            b'overrides_details="1" result_tags="0"/>'
        )

    def test_export_scan_report_with_result_tags(self):
        self.gmp.export_scan_report(
            report_id="r1",
            format_id="f1",
            result_tags=True,
        )

        self.connection.send.has_been_called_with(
            b'<export_scan_report report_id="r1" format_id="f1" '
            b'ignore_pagination="0" lean="0" notes_details="0" '
            b'overrides_details="0" result_tags="1"/>'
        )

    def test_export_scan_report_with_all_arguments(self):
        self.gmp.export_scan_report(
            report_id="r1",
            format_id="f1",
            config_id="c1",
            filter_string="levels=hml",
            ignore_pagination=True,
            lean=True,
            notes_details=True,
            overrides_details=True,
            result_tags=True,
        )

        self.connection.send.has_been_called_with(
            b'<export_scan_report report_id="r1" format_id="f1" '
            b'config_id="c1" filter="levels=hml" '
            b'ignore_pagination="1" lean="1" notes_details="1" '
            b'overrides_details="1" result_tags="1"/>'
        )
