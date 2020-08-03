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


class GmpModifySettingTestCase:
    def test_modify_setting(self):
        self.gmp.modify_setting(setting_id='s1', value='bar')

        self.connection.send.has_been_called_with(
            '<modify_setting setting_id="s1">'
            '<value>YmFy</value>'
            '</modify_setting>'
        )

        self.gmp.modify_setting(name='s1', value='bar')

        self.connection.send.has_been_called_with(
            '<modify_setting>'
            '<name>s1</name>'
            '<value>YmFy</value>'
            '</modify_setting>'
        )

        self.gmp.modify_setting(setting_id='s1', value='')

        self.connection.send.has_been_called_with(
            '<modify_setting setting_id="s1">'
            '<value></value>'
            '</modify_setting>'
        )

    def test_modify_setting_missing_setting_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_setting(setting_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_setting(setting_id='')

    def test_modify_setting_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_setting(name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_setting(name='')

    def test_modify_setting_missing_value(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_setting(setting_id='s1', value=None)


if __name__ == '__main__':
    unittest.main()
