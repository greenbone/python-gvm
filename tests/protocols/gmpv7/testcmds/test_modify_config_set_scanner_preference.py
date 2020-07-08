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


class GmpModifyConfigSetScannerPreferenceTestCase:
    def test_modify_config_set_scanner_pref(self):
        self.gmp.modify_config_set_scanner_preference(
            config_id='c1', name='foo'
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<preference>'
            '<name>foo</name>'
            '</preference>'
            '</modify_config>'
        )

        self.gmp.modify_config_set_scanner_preference('c1', 'foo')

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<preference>'
            '<name>foo</name>'
            '</preference>'
            '</modify_config>'
        )

    def test_modify_config_set_scanner_pref_with_value(self):
        self.gmp.modify_config_set_scanner_preference('c1', 'foo', value='bar')

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<preference>'
            '<name>foo</name>'
            '<value>YmFy</value>'
            '</preference>'
            '</modify_config>'
        )

    def test_modify_config_scanner_pref_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_scanner_preference(
                'c1', name=None, value='bar'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_scanner_preference(
                'c1', name='', value='bar'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_scanner_preference('c1', '', value='bar')

    def test_modify_config_set_comment_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_scanner_preference(
                config_id=None, name='foo'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_scanner_preference('', 'foo')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_scanner_preference(
                config_id='', name='foo'
            )


if __name__ == '__main__':
    unittest.main()
