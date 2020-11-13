# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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

from gvm.errors import RequiredArgument, InvalidArgumentType


class GmpModifyPolicySetNvtSelectionTestCase:
    def test_modify_policy_set_nvt_selection(self):
        self.gmp.modify_policy_set_nvt_selection(
            policy_id='c1', family='foo', nvt_oids=['o1']
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<nvt_selection>'
            '<family>foo</family>'
            '<nvt oid="o1"/>'
            '</nvt_selection>'
            '</modify_config>'
        )

        self.gmp.modify_policy_set_nvt_selection(
            policy_id='c1', family='foo', nvt_oids=['o1', 'o2']
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<nvt_selection>'
            '<family>foo</family>'
            '<nvt oid="o1"/>'
            '<nvt oid="o2"/>'
            '</nvt_selection>'
            '</modify_config>'
        )

        self.gmp.modify_policy_set_nvt_selection('c1', 'foo', ['o1'])

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<nvt_selection>'
            '<family>foo</family>'
            '<nvt oid="o1"/>'
            '</nvt_selection>'
            '</modify_config>'
        )

        self.gmp.modify_policy_set_nvt_selection('c1', 'foo', ('o1', 'o2'))

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<nvt_selection>'
            '<family>foo</family>'
            '<nvt oid="o1"/>'
            '<nvt oid="o2"/>'
            '</nvt_selection>'
            '</modify_config>'
        )

        self.gmp.modify_policy_set_nvt_selection(
            policy_id='c1', family='foo', nvt_oids=[]
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<nvt_selection>'
            '<family>foo</family>'
            '</nvt_selection>'
            '</modify_config>'
        )

    def test_modify_policy_set_nvt_selection_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id=None, family='foo', nvt_oids=['o1']
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id='', family='foo', nvt_oids=['o1']
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection('', 'foo', ['o1'])

    def test_modify_policy_set_nvt_selection_missing_family(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id='c1', family=None, nvt_oids=['o1']
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id='c1', family='', nvt_oids=['o1']
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection('c1', '', ['o1'])

    def test_modify_policy_set_nvt_selection_invalid_nvt_oids(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id='c1', family='foo', nvt_oids=None
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id='c1', family='foo', nvt_oids=''
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_nvt_selection('c1', 'foo', '')


if __name__ == '__main__':
    unittest.main()
