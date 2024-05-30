# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument


class GmpImportReportFormatTestMixin:
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

    def test_import_report_format(self):
        self.gmp.import_report_format(self.REPORT_FORMAT_XML_STRING)

        self.connection.send.has_been_called_with(
            "<create_report_format>"
            f"{self.REPORT_FORMAT_XML_STRING}</create_report_format>".encode(
                "utf-8"
            )
        )

    def test_import_missing_report_format_xml(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.import_report_format(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.import_report_format("")

    def test_import_invalid_xml(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.import_report_format("abcdef")
