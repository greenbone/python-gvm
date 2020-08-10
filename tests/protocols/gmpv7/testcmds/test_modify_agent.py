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


class GmpModifyAgentTestCase:
    def test_modify_agent(self):
        self.gmp.modify_agent(agent_id='a1')

        self.connection.send.has_been_called_with(
            '<modify_agent agent_id="a1"/>'
        )

    def test_modify_agent_without_agent_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent(agent_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent(agent_id='')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent('')

    def test_modify_agent_with_comment(self):
        self.gmp.modify_agent(agent_id='a1', comment='lorem')

        self.connection.send.has_been_called_with(
            '<modify_agent agent_id="a1">'
            '<comment>lorem</comment>'
            '</modify_agent>'
        )

    def test_modify_agent_with_name(self):
        self.gmp.modify_agent(agent_id='a1', name='lorem')

        self.connection.send.has_been_called_with(
            '<modify_agent agent_id="a1">'
            '<name>lorem</name>'
            '</modify_agent>'
        )


if __name__ == '__main__':
    unittest.main()
