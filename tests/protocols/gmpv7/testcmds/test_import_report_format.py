# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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

from gvm.errors import RequiredArgument, InvalidArgument


class GmpImportReportFormatTestCase:

    REPORT_FORMAT_XML_STRING = (
        '<get_report_formats_response status="200" status_text="OK">'
        '<report_format id="c4aa21e4-23e6-4064-ae49-c0d425738a98">'
        '<name>Foobar</name>'
        '<comment>Foobar report_format</comment>'
        '<creation_time>2018-11-09T10:48:03Z</creation_time>'
        '<modification_time>2018-11-09T10:48:03Z</modification_time>'
        '</report_format>'
        '</get_report_formats_response>'
    )

    def test_import_report_format(self):
        self.gmp.import_report_format(self.REPORT_FORMAT_XML_STRING)

        self.connection.send.has_been_called_with(
            '<create_report_format>'
            '{report_format}'
            '</create_report_format>'.format(
                report_format=self.REPORT_FORMAT_XML_STRING
            )
        )

    def test_import_missing_report_format_xml(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.import_report_format(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.import_report_format('')

    def test_import_invalid_xml(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.import_report_format('abcdef')


if __name__ == '__main__':
    unittest.main()
