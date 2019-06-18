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

from gvm.errors import RequiredArgument, InvalidArgument

from . import Gmpv7TestCase


class GmpGetAssetTestCase(Gmpv7TestCase):
    def test_get_asset_host(self):
        self.gmp.get_asset('a1', 'host')

        self.connection.send.has_been_called_with(
            '<get_assets asset_id="a1" type="host"/>'
        )

        self.gmp.get_asset(asset_id='a1', asset_type='host')

        self.connection.send.has_been_called_with(
            '<get_assets asset_id="a1" type="host"/>'
        )

    def test_get_asset_os(self):
        self.gmp.get_asset('a1', 'os')

        self.connection.send.has_been_called_with(
            '<get_assets asset_id="a1" type="os"/>'
        )
        self.gmp.get_asset(asset_id='a1', asset_type='os')

        self.connection.send.has_been_called_with(
            '<get_assets asset_id="a1" type="os"/>'
        )

    def test_get_asset_missing_asset_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_asset(asset_id=None, asset_type='host')

        with self.assertRaises(RequiredArgument):
            self.gmp.get_asset(asset_id='', asset_type='os')

    def test_get_asset_invalid_asset_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_asset(asset_id='a1', asset_type='foo')

        with self.assertRaises(InvalidArgument):
            self.gmp.get_asset(asset_id='a1', asset_type=None)

        with self.assertRaises(InvalidArgument):
            self.gmp.get_asset(asset_id='a1', asset_type='')


if __name__ == '__main__':
    unittest.main()
