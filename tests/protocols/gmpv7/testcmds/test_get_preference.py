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


class GmpGetPreferenceTestCase:
    def test_get_preference(self):
        self.gmp.get_preference(name='foo')

        self.connection.send.has_been_called_with(
            '<get_preferences preference="foo"/>'
        )

    def test_get_preference_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_preference(name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_preference(name='')

        with self.assertRaises(RequiredArgument):
            self.gmp.get_preference('')

    def test_get_preference_with_nvt_oid(self):
        self.gmp.get_preference(name='foo', nvt_oid='oid')

        self.connection.send.has_been_called_with(
            '<get_preferences preference="foo" nvt_oid="oid"/>'
        )

    def test_get_preference_with_config_id(self):
        self.gmp.get_preference(name='foo', config_id='c1')

        self.connection.send.has_been_called_with(
            '<get_preferences preference="foo" config_id="c1"/>'
        )


if __name__ == '__main__':
    unittest.main()
