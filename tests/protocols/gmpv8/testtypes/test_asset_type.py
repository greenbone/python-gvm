# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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
from gvm.protocols.gmpv8 import AssetType, get_asset_type_from_string


class GetAssetTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            get_asset_type_from_string('foo')

    def test_none_or_empty(self):
        ct = get_asset_type_from_string(None)
        self.assertIsNone(ct)
        ct = get_asset_type_from_string('')
        self.assertIsNone(ct)

    def test_os(self):
        ct = get_asset_type_from_string('os')
        self.assertEqual(ct, AssetType.OPERATING_SYSTEM)

        ct = get_asset_type_from_string('operating_system')
        self.assertEqual(ct, AssetType.OPERATING_SYSTEM)

    def test_host(self):
        ct = get_asset_type_from_string('host')
        self.assertEqual(ct, AssetType.HOST)


if __name__ == '__main__':
    unittest.main()
