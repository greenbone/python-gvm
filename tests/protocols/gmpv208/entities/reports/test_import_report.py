# -*- coding: utf-8 -*-
# Copyright (C) 2018-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
            "</create_report>"
        )

    def test_import_report_missing_report(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.import_report(None, task_id=self.TASK_ID)

        with self.assertRaises(RequiredArgument):
            self.gmp.import_report("", task_id=self.TASK_ID)

    def test_import_report_missing_task(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.import_report(self.REPORT_XML_STRING)

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
            "</create_report>"
        )

        self.gmp.import_report(
            self.REPORT_XML_STRING, task_id=self.TASK_ID, in_assets=True
        )

        self.connection.send.has_been_called_with(
            "<create_report>"
            f'<task id="{self.TASK_ID}"/>'
            "<in_assets>1</in_assets>"
            f"{self.REPORT_XML_STRING}"
            "</create_report>"
        )
