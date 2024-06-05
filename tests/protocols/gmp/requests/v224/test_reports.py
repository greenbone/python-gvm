# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import Reports

REPORT_XML_STRING = (
    '<report id="67a62fb7-b238-4f0e-bc48-59bde8939cdc">'
    '<results max="1" start="1">'
    '<result id="f180b40f-49dd-4856-81ed-8c1195afce80">'
    "<severity>0.0</severity>"
    '<nvt oid="1.3.6.1.4.1.25623.1.0.10330"/>'
    "<host>132.67.253.114</host>"
    "</result></results></report>"
)


class ReportsTestCase(unittest.TestCase):
    def test_delete_report(self):
        request = Reports.delete_report("report_id")
        self.assertEqual(
            bytes(request),
            b'<delete_report report_id="report_id"/>',
        )

    def test_delete_report_missing_report_id(self):
        with self.assertRaises(RequiredArgument):
            Reports.delete_report(None)

        with self.assertRaises(RequiredArgument):
            Reports.delete_report("")

    def test_get_report(self):
        request = Reports.get_report("report_id")
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" details="1"/>',
        )

    def test_get_report_with_filter_string(self):
        request = Reports.get_report("report_id", filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" filter="filter_string" details="1"/>',
        )

    def test_get_report_with_filter_id(self):
        request = Reports.get_report("report_id", filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" filt_id="filter_id" details="1"/>',
        )

    def test_get_report_with_delta_report_id(self):
        request = Reports.get_report(
            "report_id", delta_report_id="delta_report_id"
        )
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" delta_report_id="delta_report_id" details="1"/>',
        )

    def test_get_report_with_report_format_id(self):
        request = Reports.get_report(
            "report_id", report_format_id="report_format_id"
        )
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" format_id="report_format_id" details="1"/>',
        )

    def test_get_report_with_ignore_pagination(self):
        request = Reports.get_report("report_id", ignore_pagination=True)
        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="report_id" ignore_pagination="1" details="1"/>',
        )

    def test_get_report_missing_report_id(self):
        with self.assertRaises(RequiredArgument):
            Reports.get_report(None)

        with self.assertRaises(RequiredArgument):
            Reports.get_report("")

    def test_get_reports(self):
        request = Reports.get_reports()
        self.assertEqual(
            bytes(request),
            b"<get_reports/>",
        )

    def test_get_reports_with_filter_string(self):
        request = Reports.get_reports(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_reports report_filter="filter_string"/>',
        )

    def test_get_reports_with_filter_id(self):
        request = Reports.get_reports(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_reports report_filt_id="filter_id"/>',
        )

    def test_get_reports_with_note_details(self):
        request = Reports.get_reports(note_details=True)
        self.assertEqual(
            bytes(request),
            b'<get_reports note_details="1"/>',
        )

        request = Reports.get_reports(note_details=False)
        self.assertEqual(
            bytes(request),
            b'<get_reports note_details="0"/>',
        )

    def test_get_reports_with_override_details(self):
        request = Reports.get_reports(override_details=True)
        self.assertEqual(
            bytes(request),
            b'<get_reports override_details="1"/>',
        )

        request = Reports.get_reports(override_details=False)
        self.assertEqual(
            bytes(request),
            b'<get_reports override_details="0"/>',
        )

    def test_get_reports_with_details(self):
        request = Reports.get_reports(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_reports details="1"/>',
        )

        request = Reports.get_reports(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_reports details="0"/>',
        )

    def test_get_reports_with_ignore_pagination(self):
        request = Reports.get_reports(ignore_pagination=True)
        self.assertEqual(
            bytes(request),
            b'<get_reports ignore_pagination="1"/>',
        )

        request = Reports.get_reports(ignore_pagination=False)
        self.assertEqual(
            bytes(request),
            b'<get_reports ignore_pagination="0"/>',
        )

    def test_import_report(self):
        request = Reports.import_report(REPORT_XML_STRING, "task_id")
        self.assertEqual(
            bytes(request),
            b"<create_report>"
            b'<task id="task_id"/>'
            b'<report id="67a62fb7-b238-4f0e-bc48-59bde8939cdc">'
            b'<results max="1" start="1">'
            b'<result id="f180b40f-49dd-4856-81ed-8c1195afce80">'
            b"<severity>0.0</severity>"
            b'<nvt oid="1.3.6.1.4.1.25623.1.0.10330"/>'
            b"<host>132.67.253.114</host>"
            b"</result></results></report>"
            b"</create_report>",
        )

    def test_import_report_with_in_assets(self):
        request = Reports.import_report(
            REPORT_XML_STRING, "task_id", in_assets=False
        )
        self.assertEqual(
            bytes(request),
            b"<create_report>"
            b'<task id="task_id"/>'
            b"<in_assets>0</in_assets>"
            b'<report id="67a62fb7-b238-4f0e-bc48-59bde8939cdc">'
            b'<results max="1" start="1">'
            b'<result id="f180b40f-49dd-4856-81ed-8c1195afce80">'
            b"<severity>0.0</severity>"
            b'<nvt oid="1.3.6.1.4.1.25623.1.0.10330"/>'
            b"<host>132.67.253.114</host>"
            b"</result></results></report>"
            b"</create_report>",
        )

        request = Reports.import_report(
            REPORT_XML_STRING, "task_id", in_assets=True
        )
        self.assertEqual(
            bytes(request),
            b"<create_report>"
            b'<task id="task_id"/>'
            b"<in_assets>1</in_assets>"
            b'<report id="67a62fb7-b238-4f0e-bc48-59bde8939cdc">'
            b'<results max="1" start="1">'
            b'<result id="f180b40f-49dd-4856-81ed-8c1195afce80">'
            b"<severity>0.0</severity>"
            b'<nvt oid="1.3.6.1.4.1.25623.1.0.10330"/>'
            b"<host>132.67.253.114</host>"
            b"</result></results></report>"
            b"</create_report>",
        )

    def test_import_report_missing_report(self):
        with self.assertRaises(RequiredArgument):
            Reports.import_report(None, "task_id")

        with self.assertRaises(RequiredArgument):
            Reports.import_report("", "task_id")

    def test_import_report_missing_task_id(self):
        with self.assertRaises(RequiredArgument):
            Reports.import_report("report", None)

        with self.assertRaises(RequiredArgument):
            Reports.import_report("report", "")
