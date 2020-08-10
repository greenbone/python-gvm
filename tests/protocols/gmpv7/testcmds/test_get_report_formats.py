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


class GmpGetReportFormatsTestCase:
    def test_get_report_formats(self):
        self.gmp.get_report_formats()

        self.connection.send.has_been_called_with('<get_report_formats/>')

    def test_get_report_formats_with_filter(self):
        self.gmp.get_report_formats(filter='foo=bar')

        self.connection.send.has_been_called_with(
            '<get_report_formats filter="foo=bar"/>'
        )

    def test_get_report_formats_with_filter_id(self):
        self.gmp.get_report_formats(filter_id='f1')

        self.connection.send.has_been_called_with(
            '<get_report_formats filt_id="f1"/>'
        )

    def test_get_report_formats_with_trash(self):
        self.gmp.get_report_formats(trash=True)

        self.connection.send.has_been_called_with(
            '<get_report_formats trash="1"/>'
        )

        self.gmp.get_report_formats(trash=False)

        self.connection.send.has_been_called_with(
            '<get_report_formats trash="0"/>'
        )

    def test_get_report_formats_with_details(self):
        self.gmp.get_report_formats(details=True)

        self.connection.send.has_been_called_with(
            '<get_report_formats details="1"/>'
        )

        self.gmp.get_report_formats(details=False)

        self.connection.send.has_been_called_with(
            '<get_report_formats details="0"/>'
        )

    def test_get_report_formats_with_alerts(self):
        self.gmp.get_report_formats(alerts=True)

        self.connection.send.has_been_called_with(
            '<get_report_formats alerts="1"/>'
        )

        self.gmp.get_report_formats(alerts=False)

        self.connection.send.has_been_called_with(
            '<get_report_formats alerts="0"/>'
        )

    def test_get_report_formats_with_params(self):
        self.gmp.get_report_formats(params=True)

        self.connection.send.has_been_called_with(
            '<get_report_formats params="1"/>'
        )

        self.gmp.get_report_formats(params=False)

        self.connection.send.has_been_called_with(
            '<get_report_formats params="0"/>'
        )


if __name__ == '__main__':
    unittest.main()
