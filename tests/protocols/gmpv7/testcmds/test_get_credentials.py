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


class GmpGetCredentialsTestCase:
    def test_get_credentials(self):
        self.gmp.get_credentials()

        self.connection.send.has_been_called_with('<get_credentials/>')

    def test_get_credentials_with_filter(self):
        self.gmp.get_credentials(filter='foo=bar')

        self.connection.send.has_been_called_with(
            '<get_credentials filter="foo=bar"/>'
        )

    def test_get_credentials_with_filter_id(self):
        self.gmp.get_credentials(filter_id='f1')

        self.connection.send.has_been_called_with(
            '<get_credentials filt_id="f1"/>'
        )

    def test_get_credentials_with_scanners(self):
        self.gmp.get_credentials(scanners=True)

        self.connection.send.has_been_called_with(
            '<get_credentials scanners="1"/>'
        )

        self.gmp.get_credentials(scanners=False)

        self.connection.send.has_been_called_with(
            '<get_credentials scanners="0"/>'
        )

    def test_get_credentials_with_trash(self):
        self.gmp.get_credentials(trash=True)

        self.connection.send.has_been_called_with(
            '<get_credentials trash="1"/>'
        )

        self.gmp.get_credentials(trash=False)

        self.connection.send.has_been_called_with(
            '<get_credentials trash="0"/>'
        )

    def test_get_credentials_with_targets(self):
        self.gmp.get_credentials(targets=True)

        self.connection.send.has_been_called_with(
            '<get_credentials targets="1"/>'
        )

        self.gmp.get_credentials(targets=False)

        self.connection.send.has_been_called_with(
            '<get_credentials targets="0"/>'
        )


if __name__ == '__main__':
    unittest.main()
