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

from collections import OrderedDict

from gvm.errors import RequiredArgument


class GmpModifyAuthTestCase:
    def test_modify_auth(self):
        self.gmp.modify_auth(
            'foo', OrderedDict([('foo', 'bar'), ('lorem', 'ipsum')])
        )

        self.connection.send.has_been_called_with(
            '<modify_auth>'
            '<group name="foo">'
            '<auth_conf_setting>'
            '<key>foo</key>'
            '<value>bar</value>'
            '</auth_conf_setting>'
            '<auth_conf_setting>'
            '<key>lorem</key>'
            '<value>ipsum</value>'
            '</auth_conf_setting>'
            '</group>'
            '</modify_auth>'
        )

    def test_modify_auth_missing_group_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth(
                group_name=None, auth_conf_settings={'foo': 'bar'}
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth(
                group_name='', auth_conf_settings={'foo': 'bar'}
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth('', auth_conf_settings={'foo': 'bar'})

    def test_modify_auth_auth_conf_settings(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth(group_name='foo', auth_conf_settings=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth(group_name='foo', auth_conf_settings='')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth('foo', '')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth('foo', {})


if __name__ == '__main__':
    unittest.main()
