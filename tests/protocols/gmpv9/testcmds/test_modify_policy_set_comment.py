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

from gvm.errors import RequiredArgument


class GmpModifyPolicySetCommentTestCase:
    def test_modify_policy_set_comment(self):
        self.gmp.modify_policy_set_comment('c1')

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<comment></comment>'
            '</modify_config>'
        )

        self.gmp.modify_policy_set_comment('c1', 'foo')

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            '<comment>foo</comment>'
            '</modify_config>'
        )

        self.gmp.modify_policy_set_comment('c1', comment=None)

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">' '<comment/>' '</modify_config>'
        )

    def test_modify_policy_set_comment_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_comment(policy_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_comment('')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_comment(policy_id='')


if __name__ == '__main__':
    unittest.main()
