# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import ReportFormats, ReportFormatType


class ReportFormatsTestCase(unittest.TestCase):

    def test_clone_report_format(self):
        request = ReportFormats.clone_report_format("report_format_id")
        self.assertEqual(
            bytes(request),
            b"<create_report_format>"
            b"<copy>report_format_id</copy>"
            b"</create_report_format>",
        )

        request = ReportFormats.clone_report_format(ReportFormatType.PDF)
        self.assertEqual(
            bytes(request),
            b"<create_report_format>"
            b"<copy>c402cc3e-b531-11e1-9163-406186ea4fc5</copy>"
            b"</create_report_format>",
        )

    def test_clone_report_format_missing_report_format_id(self):
        with self.assertRaises(RequiredArgument):
            ReportFormats.clone_report_format(None)

        with self.assertRaises(RequiredArgument):
            ReportFormats.clone_report_format("")

    def test_delete_report_format(self):
        request = ReportFormats.delete_report_format("report_format_id")
        self.assertEqual(
            bytes(request),
            b'<delete_report_format report_format_id="report_format_id" ultimate="0"/>',
        )

        request = ReportFormats.delete_report_format(ReportFormatType.PDF)
        self.assertEqual(
            bytes(request),
            b'<delete_report_format report_format_id="c402cc3e-b531-11e1-9163-406186ea4fc5" ultimate="0"/>',
        )

    def test_delete_report_format_with_ultimate(self):
        request = ReportFormats.delete_report_format(
            "report_format_id", ultimate=True
        )
        self.assertEqual(
            bytes(request),
            b'<delete_report_format report_format_id="report_format_id" ultimate="1"/>',
        )

        request = ReportFormats.delete_report_format(
            ReportFormatType.PDF, ultimate=False
        )
        self.assertEqual(
            bytes(request),
            b'<delete_report_format report_format_id="c402cc3e-b531-11e1-9163-406186ea4fc5" ultimate="0"/>',
        )

    def test_delete_report_format_missing_report_format_id(self):
        with self.assertRaises(RequiredArgument):
            ReportFormats.delete_report_format(None)

        with self.assertRaises(RequiredArgument):
            ReportFormats.delete_report_format("")

    def test_get_report_formats(self):
        request = ReportFormats.get_report_formats()
        self.assertEqual(
            bytes(request),
            b"<get_report_formats/>",
        )

    def test_get_report_formats_with_filter_string(self):
        request = ReportFormats.get_report_formats(
            filter_string="filter_string"
        )
        self.assertEqual(
            bytes(request),
            b'<get_report_formats filter="filter_string"/>',
        )

    def test_get_report_formats_with_filter_id(self):
        request = ReportFormats.get_report_formats(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_report_formats filt_id="filter_id"/>',
        )

    def test_get_report_formats_with_details(self):
        request = ReportFormats.get_report_formats(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_report_formats details="1"/>',
        )

        request = ReportFormats.get_report_formats(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_report_formats details="0"/>',
        )

    def test_get_report_formats_with_alerts(self):
        request = ReportFormats.get_report_formats(alerts=True)
        self.assertEqual(
            bytes(request),
            b'<get_report_formats alerts="1"/>',
        )

        request = ReportFormats.get_report_formats(alerts=False)
        self.assertEqual(
            bytes(request),
            b'<get_report_formats alerts="0"/>',
        )

    def test_get_report_formats_with_params(self):
        request = ReportFormats.get_report_formats(params=True)
        self.assertEqual(
            bytes(request),
            b'<get_report_formats params="1"/>',
        )

        request = ReportFormats.get_report_formats(params=False)
        self.assertEqual(
            bytes(request),
            b'<get_report_formats params="0"/>',
        )

    def test_get_report_formats_with_trash(self):
        request = ReportFormats.get_report_formats(trash=True)
        self.assertEqual(
            bytes(request),
            b'<get_report_formats trash="1"/>',
        )

        request = ReportFormats.get_report_formats(trash=False)
        self.assertEqual(
            bytes(request),
            b'<get_report_formats trash="0"/>',
        )

    def test_get_report_format(self):
        request = ReportFormats.get_report_format("report_format_id")
        self.assertEqual(
            bytes(request),
            b'<get_report_formats report_format_id="report_format_id" details="1"/>',
        )

        request = ReportFormats.get_report_format(ReportFormatType.PDF)
        self.assertEqual(
            bytes(request),
            b'<get_report_formats report_format_id="c402cc3e-b531-11e1-9163-406186ea4fc5" details="1"/>',
        )

    def test_get_report_format_missing_report_format_id(self):
        with self.assertRaises(RequiredArgument):
            ReportFormats.get_report_format(None)

        with self.assertRaises(RequiredArgument):
            ReportFormats.get_report_format("")

    def test_import_report_format(self):
        REPORT_FORMAT_XML_STRING = (
            '<get_report_formats_response status="200" status_text="OK">'
            '<report_format id="c4aa21e4-23e6-4064-ae49-c0d425738a98">'
            "<name>Foobar</name>"
            "<comment>Foobar report_format</comment>"
            "<creation_time>2018-11-09T10:48:03Z</creation_time>"
            "<modification_time>2018-11-09T10:48:03Z</modification_time>"
            "</report_format>"
            "</get_report_formats_response>"
        )
        request = ReportFormats.import_report_format(REPORT_FORMAT_XML_STRING)
        self.assertEqual(
            bytes(request),
            b"<create_report_format>"
            b'<get_report_formats_response status="200" status_text="OK">'
            b'<report_format id="c4aa21e4-23e6-4064-ae49-c0d425738a98">'
            b"<name>Foobar</name>"
            b"<comment>Foobar report_format</comment>"
            b"<creation_time>2018-11-09T10:48:03Z</creation_time>"
            b"<modification_time>2018-11-09T10:48:03Z</modification_time>"
            b"</report_format>"
            b"</get_report_formats_response>"
            b"</create_report_format>",
        )

    def test_import_report_format_invalid_report_format(self):
        with self.assertRaises(InvalidArgument):
            ReportFormats.import_report_format("invalid_report_format")

    def test_modify_report_format(self):
        request = ReportFormats.modify_report_format("report_format_id")
        self.assertEqual(
            bytes(request),
            b'<modify_report_format report_format_id="report_format_id"/>',
        )

        request = ReportFormats.modify_report_format(ReportFormatType.PDF)
        self.assertEqual(
            bytes(request),
            b'<modify_report_format report_format_id="c402cc3e-b531-11e1-9163-406186ea4fc5"/>',
        )

    def test_modify_report_format_with_active(self):
        request = ReportFormats.modify_report_format(
            "report_format_id", active=True
        )
        self.assertEqual(
            bytes(request),
            b'<modify_report_format report_format_id="report_format_id">'
            b"<active>1</active>"
            b"</modify_report_format>",
        )

        request = ReportFormats.modify_report_format(
            ReportFormatType.PDF, active=False
        )
        self.assertEqual(
            bytes(request),
            b'<modify_report_format report_format_id="c402cc3e-b531-11e1-9163-406186ea4fc5">'
            b"<active>0</active>"
            b"</modify_report_format>",
        )

    def test_modify_report_format_with_name(self):
        request = ReportFormats.modify_report_format(
            "report_format_id", name="Foobar"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_report_format report_format_id="report_format_id">'
            b"<name>Foobar</name>"
            b"</modify_report_format>",
        )

    def test_modify_report_format_with_summary(self):
        request = ReportFormats.modify_report_format(
            "report_format_id", summary="Foobar report_format"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_report_format report_format_id="report_format_id">'
            b"<summary>Foobar report_format</summary>"
            b"</modify_report_format>",
        )

    def test_modify_report_format_with_param_name(self):
        request = ReportFormats.modify_report_format(
            "report_format_id", param_name="Foobar"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_report_format report_format_id="report_format_id">'
            b"<param>"
            b"<name>Foobar</name>"
            b"</param>"
            b"</modify_report_format>",
        )

    def test_modify_report_format_with_param_name_and_value(self):
        request = ReportFormats.modify_report_format(
            "report_format_id", param_name="Foobar", param_value="42"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_report_format report_format_id="report_format_id">'
            b"<param>"
            b"<name>Foobar</name>"
            b"<value>42</value>"
            b"</param>"
            b"</modify_report_format>",
        )

    def test_verify_report_format(self):
        request = ReportFormats.verify_report_format("report_format_id")
        self.assertEqual(
            bytes(request),
            b'<verify_report_format report_format_id="report_format_id"/>',
        )

        request = ReportFormats.verify_report_format(ReportFormatType.PDF)
        self.assertEqual(
            bytes(request),
            b'<verify_report_format report_format_id="c402cc3e-b531-11e1-9163-406186ea4fc5"/>',
        )

    def test_verify_report_format_missing_report_format_id(self):
        with self.assertRaises(RequiredArgument):
            ReportFormats.verify_report_format(None)

        with self.assertRaises(RequiredArgument):
            ReportFormats.verify_report_format("")
