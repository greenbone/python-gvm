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


class GmpGetScannersTestCase:
    def test_get_scanners(self):
        self.gmp.get_scanners()

        self.connection.send.has_been_called_with('<get_scanners/>')

    def test_get_scanners_with_filter(self):
        self.gmp.get_scanners(filter='foo=bar')

        self.connection.send.has_been_called_with(
            '<get_scanners filter="foo=bar"/>'
        )

    def test_get_scanners_with_filter_id(self):
        self.gmp.get_scanners(filter_id='f1')

        self.connection.send.has_been_called_with(
            '<get_scanners filt_id="f1"/>'
        )

    def test_get_scanners_with_trash(self):
        self.gmp.get_scanners(trash=True)

        self.connection.send.has_been_called_with('<get_scanners trash="1"/>')

        self.gmp.get_scanners(trash=False)

        self.connection.send.has_been_called_with('<get_scanners trash="0"/>')

    def test_get_scanners_with_details(self):
        self.gmp.get_scanners(details=True)

        self.connection.send.has_been_called_with('<get_scanners details="1"/>')

        self.gmp.get_scanners(details=False)

        self.connection.send.has_been_called_with('<get_scanners details="0"/>')


if __name__ == '__main__':
    unittest.main()
