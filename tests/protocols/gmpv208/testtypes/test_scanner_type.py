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

from gvm.errors import InvalidArgument
from gvm.protocols.gmpv208 import ScannerType, get_scanner_type_from_string


class GetScannerTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            get_scanner_type_from_string('foo')

    def test_none_or_empty(self):
        ct = get_scanner_type_from_string(None)
        self.assertIsNone(ct)
        ct = get_scanner_type_from_string('')
        self.assertIsNone(ct)

    def test_osp_scanner(self):
        ct = get_scanner_type_from_string('1')
        self.assertEqual(ct, ScannerType.OSP_SCANNER_TYPE)

        ct = get_scanner_type_from_string('osp')
        self.assertEqual(ct, ScannerType.OSP_SCANNER_TYPE)

    def test_openvas_scanner(self):
        ct = get_scanner_type_from_string('2')
        self.assertEqual(ct, ScannerType.OPENVAS_SCANNER_TYPE)

        ct = get_scanner_type_from_string('openvas')
        self.assertEqual(ct, ScannerType.OPENVAS_SCANNER_TYPE)

    def test_cve_scanner(self):
        ct = get_scanner_type_from_string('3')
        self.assertEqual(ct, ScannerType.CVE_SCANNER_TYPE)

        ct = get_scanner_type_from_string('cve')
        self.assertEqual(ct, ScannerType.CVE_SCANNER_TYPE)

    def test_gmp_scanner(self):
        ct = get_scanner_type_from_string('4')
        self.assertEqual(ct, ScannerType.GMP_SCANNER_TYPE)

        ct = get_scanner_type_from_string('gmp')
        self.assertEqual(ct, ScannerType.GMP_SCANNER_TYPE)

    def test_greenbone_sensor_scanner(self):
        ct = get_scanner_type_from_string('5')
        self.assertEqual(ct, ScannerType.GREENBONE_SENSOR_SCANNER_TYPE)

        ct = get_scanner_type_from_string('greenbone')
        self.assertEqual(ct, ScannerType.GREENBONE_SENSOR_SCANNER_TYPE)


if __name__ == '__main__':
    unittest.main()
