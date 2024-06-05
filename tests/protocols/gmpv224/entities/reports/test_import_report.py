# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument


class GmpImportReportTestMixin:
    TASK_ID = "00000000-0000-0000-0000-000000000001"
    REPORT_XML_STRING = (
        '<report id="67a62fb7-b238-4f0e-bc48-59bde8939cdc">'
        '<results max="1" start="1">'
        '<result id="f180b40f-49dd-4856-81ed-8c1195afce80">'
        "<severity>0.0</severity>"
        '<nvt oid="1.3.6.1.4.1.25623.1.0.10330"/>'
        "<host>132.67.253.114</host>"
        "</result></results></report>"
    )

    def test_import_report_with_task_id(self):
        self.gmp.import_report(self.REPORT_XML_STRING, task_id=self.TASK_ID)

        self.connection.send.has_been_called_with(
            "<create_report>"
            f'<task id="{self.TASK_ID}"/>'
            f"{self.REPORT_XML_STRING}"
            "</create_report>".encode("utf-8")
        )

    def test_import_report_missing_report(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.import_report(None, task_id=self.TASK_ID)

        with self.assertRaises(RequiredArgument):
            self.gmp.import_report("", task_id=self.TASK_ID)

    def test_import_report_invalid_xml(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.import_report("Foo", task_id=self.TASK_ID)  # not root tag

        with self.assertRaises(InvalidArgument):
            self.gmp.import_report(
                "<Foo>", task_id=self.TASK_ID  # missing closing tag
            )

    def test_import_report_with_in_assets(self):
        self.gmp.import_report(
            self.REPORT_XML_STRING, task_id=self.TASK_ID, in_assets=False
        )

        self.connection.send.has_been_called_with(
            "<create_report>"
            f'<task id="{self.TASK_ID}"/>'
            "<in_assets>0</in_assets>"
            f"{self.REPORT_XML_STRING}"
            "</create_report>".encode("utf-8")
        )

        self.gmp.import_report(
            self.REPORT_XML_STRING, task_id=self.TASK_ID, in_assets=True
        )

        self.connection.send.has_been_called_with(
            "<create_report>"
            f'<task id="{self.TASK_ID}"/>'
            "<in_assets>1</in_assets>"
            f"{self.REPORT_XML_STRING}"
            "</create_report>".encode("utf-8")
        )
