# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v226 import AuditReports


class AuditReportsTestCase(unittest.TestCase):
    def test_delete_report(self):
        request = AuditReports.delete_report("report_id")
        self.assertEqual(
            bytes(request),
            b'<delete_report report_id="report_id"/>',
        )

    def test_delete_report_missing_report_id(self):
        with self.assertRaises(RequiredArgument):
            AuditReports.delete_report(None)

        with self.assertRaises(RequiredArgument):
            AuditReports.delete_report("")

    def test_get_report(self):
        request = AuditReports.get_report("report_id")
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" usage_type="audit" details="1"/>',
        )

    def test_get_report_with_filter_string(self):
        request = AuditReports.get_report(
            "report_id", filter_string="filter_string"
        )
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" usage_type="audit" filter="filter_string" details="1"/>',
        )

    def test_get_report_with_filter_id(self):
        request = AuditReports.get_report("report_id", filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" usage_type="audit" filt_id="filter_id" details="1"/>',
        )

    def test_get_report_with_delta_report_id(self):
        request = AuditReports.get_report(
            "report_id", delta_report_id="delta_report_id"
        )
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" usage_type="audit" delta_report_id="delta_report_id" details="1"/>',
        )

    def test_get_report_with_report_format_id(self):
        request = AuditReports.get_report(
            "report_id", report_format_id="report_format_id"
        )
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" usage_type="audit" format_id="report_format_id" details="1"/>',
        )

    def test_get_report_with_ignore_pagination(self):
        request = AuditReports.get_report("report_id", ignore_pagination=True)
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" usage_type="audit" ignore_pagination="1" details="1"/>',
        )

    def test_get_report_missing_report_id(self):
        with self.assertRaises(RequiredArgument):
            AuditReports.get_report(None)

        with self.assertRaises(RequiredArgument):
            AuditReports.get_report("")

    def test_get_reports(self):
        request = AuditReports.get_reports()
        self.assertEqual(
            bytes(request),
            b'<get_reports usage_type="audit"/>',
        )

    def test_get_reports_with_filter_string(self):
        request = AuditReports.get_reports(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_reports usage_type="audit" report_filter="filter_string"/>',
        )

    def test_get_reports_with_filter_id(self):
        request = AuditReports.get_reports(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_reports usage_type="audit" report_filt_id="filter_id"/>',
        )

    def test_get_reports_with_note_details(self):
        request = AuditReports.get_reports(note_details=True)
        self.assertEqual(
            bytes(request),
            b'<get_reports usage_type="audit" note_details="1"/>',
        )

        request = AuditReports.get_reports(note_details=False)
        self.assertEqual(
            bytes(request),
            b'<get_reports usage_type="audit" note_details="0"/>',
        )

    def test_get_reports_with_override_details(self):
        request = AuditReports.get_reports(override_details=True)
        self.assertEqual(
            bytes(request),
            b'<get_reports usage_type="audit" override_details="1"/>',
        )

        request = AuditReports.get_reports(override_details=False)
        self.assertEqual(
            bytes(request),
            b'<get_reports usage_type="audit" override_details="0"/>',
        )

    def test_get_reports_with_details(self):
        request = AuditReports.get_reports(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_reports usage_type="audit" details="1"/>',
        )

        request = AuditReports.get_reports(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_reports usage_type="audit" details="0"/>',
        )

    def test_get_reports_with_ignore_pagination(self):
        request = AuditReports.get_reports(ignore_pagination=True)
        self.assertEqual(
            bytes(request),
            b'<get_reports usage_type="audit" ignore_pagination="1"/>',
        )

        request = AuditReports.get_reports(ignore_pagination=False)
        self.assertEqual(
            bytes(request),
            b'<get_reports usage_type="audit" ignore_pagination="0"/>',
        )
