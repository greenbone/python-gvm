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


class GmpGetConfigsTestCase:
    def test_get_configs_simple(self):
        self.gmp.get_configs()

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan"/>'
        )

    def test_get_configs_with_filter(self):
        self.gmp.get_configs(filter='name=foo')

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan" filter="name=foo"/>'
        )

    def test_get_configs_with_filter_id(self):
        self.gmp.get_configs(filter_id='f1')

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan" filt_id="f1"/>'
        )

    def test_get_configs_from_trash(self):
        self.gmp.get_configs(trash=True)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan" trash="1"/>'
        )

    def test_get_configs_with_details(self):
        self.gmp.get_configs(details=True)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan" details="1"/>'
        )

    def test_get_configs_without_details(self):
        self.gmp.get_configs(details=False)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan" details="0"/>'
        )

    def test_get_configs_with_families(self):
        self.gmp.get_configs(families=True)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan" families="1"/>'
        )

    def test_get_configs_without_families(self):
        self.gmp.get_configs(families=False)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan" families="0"/>'
        )

    def test_get_configs_with_preferences(self):
        self.gmp.get_configs(preferences=True)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan" preferences="1"/>'
        )

    def test_get_configs_without_preferences(self):
        self.gmp.get_configs(preferences=False)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan" preferences="0"/>'
        )

    def test_get_configs_with_tasks(self):
        self.gmp.get_configs(tasks=True)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan" tasks="1"/>'
        )

    def test_get_configs_without_tasks(self):
        self.gmp.get_configs(tasks=False)

        self.connection.send.has_been_called_with(
            '<get_configs usage_type="scan" tasks="0"/>'
        )


if __name__ == '__main__':
    unittest.main()
