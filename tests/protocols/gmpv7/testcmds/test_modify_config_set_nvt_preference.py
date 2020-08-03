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


class GmpModifyConfigSetNvtPreferenceTestCase:
    def test_modify_config_set_nvt_pref(self):
        self.gmp.modify_config_set_nvt_preference(
            config_id='c1', nvt_oid='o1', name='foo'
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<preference>'
            '<nvt oid="o1"/>'
            '<name>foo</name>'
            '</preference>'
            '</modify_config>'
        )

        self.gmp.modify_config_set_nvt_preference('c1', 'foo', 'o1')

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<preference>'
            '<nvt oid="o1"/>'
            '<name>foo</name>'
            '</preference>'
            '</modify_config>'
        )

    def test_modify_config_set_nvt_pref_with_value(self):
        self.gmp.modify_config_set_nvt_preference(
            'c1', 'foo', nvt_oid='o1', value='bar'
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<preference>'
            '<nvt oid="o1"/>'
            '<name>foo</name>'
            '<value>YmFy</value>'
            '</preference>'
            '</modify_config>'
        )

    def test_modify_config_set_nvt_pref_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_nvt_preference(
                'c1', 'foo', nvt_oid=None, value='bar'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_nvt_preference(
                'c1', 'foo', nvt_oid='', value='bar'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_nvt_preference(
                'c1', 'foo', '', value='bar'
            )

    def test_modify_config_nvt_pref_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_nvt_preference(
                'c1', name=None, nvt_oid='o1', value='bar'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_nvt_preference(
                'c1', name='', nvt_oid='o1', value='bar'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_nvt_preference(
                'c1', '', nvt_oid='o1', value='bar'
            )

    def test_modify_config_set_comment_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_nvt_preference(
                config_id=None, name='foo', nvt_oid='o1'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_nvt_preference('', 'foo', 'o1')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_config_set_nvt_preference(
                config_id='', name='foo', nvt_oid='o1'
            )


if __name__ == '__main__':
    unittest.main()
