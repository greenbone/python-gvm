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

from gvm.errors import RequiredArgument
from gvm.protocols.gmpv7 import (
    ReportFormatType,
    get_report_format_id_from_string,
)


class GmpTriggerAlertTestCase:
    def test_trigger_alert_without_alert_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.trigger_alert(alert_id=None, report_id='r1')

        with self.assertRaises(RequiredArgument):
            self.gmp.trigger_alert(alert_id='', report_id='r1')

    def test_trigger_alert_without_report_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.trigger_alert(alert_id='a1', report_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.trigger_alert(alert_id='a1', report_id='')

    def test_trigger_alert(self):
        self.gmp.trigger_alert(alert_id='a1', report_id='r1')

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" alert_id="a1"/>'
        )

    def test_trigger_alert_with_filter(self):
        self.gmp.trigger_alert(alert_id='a1', report_id='r1', filter='name=foo')

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" alert_id="a1" filter="name=foo"/>'
        )

    def test_trigger_alert_with_filter_id(self):
        self.gmp.trigger_alert(alert_id="a1", report_id='r1', filter_id='f1')

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" alert_id="a1" filt_id="f1"/>'
        )

    def test_trigger_alert_with_report_format_id(self):
        self.gmp.trigger_alert(
            alert_id="a1", report_id='r1', report_format_id='bar'
        )

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" alert_id="a1" format_id="bar"/>'
        )

    def test_trigger_alert_with_report_format_type(self):
        self.gmp.trigger_alert(
            alert_id="a1", report_id='r1', report_format_id=ReportFormatType.SVG
        )

        report_format_id = get_report_format_id_from_string('svg').value

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" alert_id="a1" '
            'format_id="{}"/>'.format(report_format_id)
        )

    def test_trigger_alert_with_delta_report_id(self):
        self.gmp.trigger_alert(
            alert_id='a1', report_id='r1', delta_report_id='r2'
        )

        self.connection.send.has_been_called_with(
            '<get_reports report_id="r1" alert_id="a1" delta_report_id="r2"/>'
        )


if __name__ == '__main__':
    unittest.main()
