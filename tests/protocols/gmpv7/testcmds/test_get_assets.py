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

from gvm.errors import InvalidArgumentType

from gvm.protocols.gmpv7 import AssetType


class GmpGetAssetsTestCase:
    def test_get_assets(self):
        self.gmp.get_assets(AssetType.OPERATING_SYSTEM)

        self.connection.send.has_been_called_with('<get_assets type="os"/>')

        self.gmp.get_assets(asset_type=AssetType.OPERATING_SYSTEM)

        self.connection.send.has_been_called_with('<get_assets type="os"/>')

        self.gmp.get_assets(asset_type=AssetType.HOST)

        self.connection.send.has_been_called_with('<get_assets type="host"/>')

    def test_get_assets_invalid_asset_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_assets(asset_type=None)

        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_assets(asset_type='')

        with self.assertRaises(InvalidArgumentType):
            self.gmp.get_assets(asset_type='foo')

    def test_get_assets_with_filter(self):
        self.gmp.get_assets(
            asset_type=AssetType.OPERATING_SYSTEM, filter='foo=bar'
        )

        self.connection.send.has_been_called_with(
            '<get_assets type="os" filter="foo=bar"/>'
        )

    def test_get_assets_with_filter_id(self):
        self.gmp.get_assets(
            asset_type=AssetType.OPERATING_SYSTEM, filter_id='f1'
        )

        self.connection.send.has_been_called_with(
            '<get_assets type="os" filt_id="f1"/>'
        )


if __name__ == '__main__':
    unittest.main()
