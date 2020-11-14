# -*- coding: utf-8 -*-
# Copyright (C) 2018-2020 Greenbone Networks GmbH
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

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmpv7 import (
    ReportFormatType,
    get_report_format_id_from_string,
)


class GmpGetReportTestCase:
    def test_get_report_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_report(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_report('')

    def test_get_report_with_filter(self):
        self.gmp.get_report(report_id='r1', filter='name=foo')

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" filter="name=foo" details="1"/>'
        )

    def test_get_report_with_filter_id(self):
        self.gmp.get_report(report_id='r1', filter_id='f1')

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" filt_id="f1" details="1"/>'
        )

    def test_get_report_with_report_format_id(self):
        self.gmp.get_report(report_id='r1', report_format_id='bar')

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" format_id="bar" details="1"/>'
        )

    def test_get_report_with_report_format_type(self):
        self.gmp.get_report(
            report_id='r1', report_format_id=ReportFormatType.TXT
        )
        report_format_id = get_report_format_id_from_string('txt').value

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" format_id="{}" details="1"/>'.format(
                report_format_id
            )
        )

    def test_get_report_with_delta_report_id(self):
        self.gmp.get_report(report_id='r1', delta_report_id='r2')

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" delta_report_id="r2" details="1"/>'
        )

    def test_get_report_with_ignore_pagination(self):
        self.gmp.get_report(report_id='r1', ignore_pagination=True)

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" ignore_pagination="1" details="1"/>'
        )

        self.gmp.get_report(report_id='r1', ignore_pagination=False)

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" ignore_pagination="0" details="1"/>'
        )

    def test_get_report_with_details(self):
        self.gmp.get_report(report_id='r1', details=True)

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" details="1"/>'
        )

        self.gmp.get_report(report_id='r1', details=False)

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" details="0"/>'
        )


if __name__ == '__main__':
    unittest.main()
