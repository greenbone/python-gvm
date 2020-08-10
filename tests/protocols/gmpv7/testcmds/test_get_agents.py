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

from gvm.errors import InvalidArgument


class GmpGetAgentsTestCase:
    def test_get_agents(self):
        self.gmp.get_agents()

        self.connection.send.has_been_called_with('<get_agents/>')

    def test_get_agents_with_trash(self):
        self.gmp.get_agents(trash=True)

        self.connection.send.has_been_called_with('<get_agents trash="1"/>')

        self.gmp.get_agents(trash=False)

        self.connection.send.has_been_called_with('<get_agents trash="0"/>')

    def test_get_agents_with_details(self):
        self.gmp.get_agents(details=True)

        self.connection.send.has_been_called_with('<get_agents details="1"/>')

        self.gmp.get_agents(details=False)

        self.connection.send.has_been_called_with('<get_agents details="0"/>')

    def test_get_agents_with_format(self):
        self.gmp.get_agents(format='installer')

        self.connection.send.has_been_called_with(
            '<get_agents format="installer"/>'
        )

        self.gmp.get_agents(format='howto_install')

        self.connection.send.has_been_called_with(
            '<get_agents format="howto_install"/>'
        )

        self.gmp.get_agents(format='howto_use')

        self.connection.send.has_been_called_with(
            '<get_agents format="howto_use"/>'
        )

    def test_get_agents_invalid_format(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_agents(format='foo')


if __name__ == '__main__':
    unittest.main()
