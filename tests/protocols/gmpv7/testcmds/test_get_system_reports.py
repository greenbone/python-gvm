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

from gvm.errors import InvalidArgument


class GmpGetSystemReportsTestCase:
    def test_get_system_reports(self):
        self.gmp.get_system_reports()

        self.connection.send.has_been_called_with('<get_system_reports/>')

    def test_get_system_reports_with_name(self):
        self.gmp.get_system_reports(name='foo')

        self.connection.send.has_been_called_with(
            '<get_system_reports name="foo"/>'
        )

    def test_get_system_reports_with_slave_id(self):
        self.gmp.get_system_reports(slave_id='s1')

        self.connection.send.has_been_called_with(
            '<get_system_reports slave_id="s1"/>'
        )

    def test_get_system_reports_with_brief(self):
        self.gmp.get_system_reports(brief=True)

        self.connection.send.has_been_called_with(
            '<get_system_reports brief="1"/>'
        )

        self.gmp.get_system_reports(brief=False)

        self.connection.send.has_been_called_with(
            '<get_system_reports brief="0"/>'
        )

    def test_get_system_reports_with_duration(self):
        self.gmp.get_system_reports(duration=3600)

        self.connection.send.has_been_called_with(
            '<get_system_reports duration="3600"/>'
        )

    def test_get_system_reports_with_invalid_duration(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_system_reports(duration='')

    def test_get_system_reports_with_start_time(self):
        self.gmp.get_system_reports(start_time='01-01-2019')

        self.connection.send.has_been_called_with(
            '<get_system_reports start_time="01-01-2019"/>'
        )

    def test_get_system_reports_with_end_time(self):
        self.gmp.get_system_reports(end_time='01-01-2019')

        self.connection.send.has_been_called_with(
            '<get_system_reports end_time="01-01-2019"/>'
        )


if __name__ == '__main__':
    unittest.main()
