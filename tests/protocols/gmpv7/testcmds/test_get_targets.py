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


class GmpGetTargetsTestCase:
    def test_get_targets(self):
        self.gmp.get_targets()

        self.connection.send.has_been_called_with('<get_targets/>')

    def test_get_targets_with_filter(self):
        self.gmp.get_targets(filter='foo=bar')

        self.connection.send.has_been_called_with(
            '<get_targets filter="foo=bar"/>'
        )

    def test_get_targets_with_filter_id(self):
        self.gmp.get_targets(filter_id='f1')

        self.connection.send.has_been_called_with('<get_targets filt_id="f1"/>')

    def test_get_targets_with_trash(self):
        self.gmp.get_targets(trash=True)

        self.connection.send.has_been_called_with('<get_targets trash="1"/>')

        self.gmp.get_targets(trash=False)

        self.connection.send.has_been_called_with('<get_targets trash="0"/>')

    def test_get_targets_with_tasks(self):
        self.gmp.get_targets(tasks=True)

        self.connection.send.has_been_called_with('<get_targets tasks="1"/>')

        self.gmp.get_targets(tasks=False)

        self.connection.send.has_been_called_with('<get_targets tasks="0"/>')


if __name__ == '__main__':
    unittest.main()
