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


class GmpGetNvtsTestCase:
    def test_get_nvts_simple(self):
        self.gmp.get_nvts()

        self.connection.send.has_been_called_with('<get_nvts/>')

    def test_get_nvts_with_details(self):
        self.gmp.get_nvts(details=True)

        self.connection.send.has_been_called_with('<get_nvts details="1"/>')

        self.gmp.get_nvts(details=False)

        self.connection.send.has_been_called_with('<get_nvts details="0"/>')

    def test_get_nvts_with_preferences(self):
        self.gmp.get_nvts(preferences=True)

        self.connection.send.has_been_called_with('<get_nvts preferences="1"/>')

        self.gmp.get_nvts(preferences=False)

        self.connection.send.has_been_called_with('<get_nvts preferences="0"/>')

    def test_get_nvts_with_preference_count(self):
        self.gmp.get_nvts(preference_count=True)

        self.connection.send.has_been_called_with(
            '<get_nvts preference_count="1"/>'
        )

    def test_get_nvts_with_timeout(self):
        self.gmp.get_nvts(timeout=True)

        self.connection.send.has_been_called_with('<get_nvts timeout="1"/>')

        self.gmp.get_nvts(timeout=False)

        self.connection.send.has_been_called_with('<get_nvts timeout="0"/>')

    def test_get_nvts_with_config_id(self):
        self.gmp.get_nvts(config_id='config_id')

        self.connection.send.has_been_called_with(
            '<get_nvts config_id="config_id"/>'
        )

    def test_get_nvts_with_preferences_config_id(self):
        self.gmp.get_nvts(preferences_config_id='preferences_config_id')

        self.connection.send.has_been_called_with(
            '<get_nvts preferences_config_id="preferences_config_id"/>'
        )

    def test_get_nvts_with_family(self):
        self.gmp.get_nvts(family='family')

        self.connection.send.has_been_called_with('<get_nvts family="family"/>')

    def test_get_nvts_with_sort_order(self):
        self.gmp.get_nvts(sort_order='sort_order')

        self.connection.send.has_been_called_with(
            '<get_nvts sort_order="sort_order"/>'
        )

    def test_get_nvts_with_sort_field(self):
        self.gmp.get_nvts(sort_field='sort_field')

        self.connection.send.has_been_called_with(
            '<get_nvts sort_field="sort_field"/>'
        )


if __name__ == '__main__':
    unittest.main()
