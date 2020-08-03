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


class GmpGetPortListsTestCase:
    def test_get_port_lists(self):
        self.gmp.get_port_lists()

        self.connection.send.has_been_called_with('<get_port_lists/>')

    def test_get_port_lists_with_filter(self):
        self.gmp.get_port_lists(filter='foo=bar')

        self.connection.send.has_been_called_with(
            '<get_port_lists filter="foo=bar"/>'
        )

    def test_get_port_lists_with_filter_id(self):
        self.gmp.get_port_lists(filter_id='f1')

        self.connection.send.has_been_called_with(
            '<get_port_lists filt_id="f1"/>'
        )

    def test_get_port_lists_with_trash(self):
        self.gmp.get_port_lists(trash=True)

        self.connection.send.has_been_called_with('<get_port_lists trash="1"/>')

        self.gmp.get_port_lists(trash=False)

        self.connection.send.has_been_called_with('<get_port_lists trash="0"/>')

    def test_get_port_lists_with_details(self):
        self.gmp.get_port_lists(details=True)

        self.connection.send.has_been_called_with(
            '<get_port_lists details="1"/>'
        )

        self.gmp.get_port_lists(details=False)

        self.connection.send.has_been_called_with(
            '<get_port_lists details="0"/>'
        )

    def test_get_port_lists_with_targets(self):
        self.gmp.get_port_lists(targets=True)

        self.connection.send.has_been_called_with(
            '<get_port_lists targets="1"/>'
        )

        self.gmp.get_port_lists(targets=False)

        self.connection.send.has_been_called_with(
            '<get_port_lists targets="0"/>'
        )


if __name__ == '__main__':
    unittest.main()
