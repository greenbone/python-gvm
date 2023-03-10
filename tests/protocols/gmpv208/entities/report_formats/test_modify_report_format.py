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

from gvm.errors import RequiredArgument
from gvm.protocols.gmpv208.entities.report_formats import ReportFormatType


class GmpModifyReportFormatTestMixin:
    def test_modify_report_format(self):
        self.gmp.modify_report_format(report_format_id="rf1")

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1"/>'
        )

    def test_modify_report_format_missing_report_format_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_report_format(report_format_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_report_format(report_format_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_report_format("")

    def test_modify_report_format_with_summary(self):
        self.gmp.modify_report_format(report_format_id="rf1", summary="foo")

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<summary>foo</summary>"
            "</modify_report_format>"
        )

    def test_modify_report_format_with_name(self):
        self.gmp.modify_report_format(report_format_id="rf1", name="foo")

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<name>foo</name>"
            "</modify_report_format>"
        )

    def test_modify_report_format_with_name_and_type(self):
        self.gmp.modify_report_format(
            report_format_id=ReportFormatType.XML, name="foo"
        )

        report_format_id = ReportFormatType.from_string("xml").value
        self.connection.send.has_been_called_with(
            f'<modify_report_format report_format_id="{report_format_id}">'
            "<name>foo</name></modify_report_format>"
        )

    def test_modify_report_format_with_active(self):
        self.gmp.modify_report_format(report_format_id="rf1", active=True)

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<active>1</active>"
            "</modify_report_format>"
        )

        self.gmp.modify_report_format(report_format_id="rf1", active=False)

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<active>0</active>"
            "</modify_report_format>"
        )

    def test_modify_report_format_with_param_name(self):
        self.gmp.modify_report_format(report_format_id="rf1", param_name="foo")

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<param>"
            "<name>foo</name>"
            "</param>"
            "</modify_report_format>"
        )

    def test_modify_report_format_with_param_name_and_value(self):
        self.gmp.modify_report_format(
            report_format_id="rf1", param_name="foo", param_value="bar"
        )

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<param>"
            "<name>foo</name>"
            "<value>bar</value>"
            "</param>"
            "</modify_report_format>"
        )

        self.gmp.modify_report_format(
            report_format_id="rf1", param_name="foo", param_value=""
        )

        self.connection.send.has_been_called_with(
            '<modify_report_format report_format_id="rf1">'
            "<param>"
            "<name>foo</name>"
            "<value></value>"
            "</param>"
            "</modify_report_format>"
        )
