# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest

from gvm.errors import InvalidArgument
from gvm.protocols.gmp.requests.v224 import ScannerType


class GetScannerTypeFromStringTestCase(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(InvalidArgument):
            ScannerType.from_string("foo")

    def test_none_or_empty(self):
        ct = ScannerType.from_string(None)
        self.assertIsNone(ct)
        ct = ScannerType.from_string("")
        self.assertIsNone(ct)

    def test_openvas_scanner(self):
        ct = ScannerType.from_string("2")
        self.assertEqual(ct, ScannerType.OPENVAS_SCANNER_TYPE)

        ct = ScannerType.from_string("openvas")
        self.assertEqual(ct, ScannerType.OPENVAS_SCANNER_TYPE)

    def test_cve_scanner(self):
        ct = ScannerType.from_string("3")
        self.assertEqual(ct, ScannerType.CVE_SCANNER_TYPE)

        ct = ScannerType.from_string("cve")
        self.assertEqual(ct, ScannerType.CVE_SCANNER_TYPE)

    def test_gmp_scanner(self):
        with self.assertRaises(InvalidArgument):
            ScannerType.from_string("4")

        with self.assertRaises(InvalidArgument):
            ScannerType.from_string("gmp")

    def test_greenbone_sensor_scanner(self):
        ct = ScannerType.from_string("5")
        self.assertEqual(ct, ScannerType.GREENBONE_SENSOR_SCANNER_TYPE)

        ct = ScannerType.from_string("greenbone")
        self.assertEqual(ct, ScannerType.GREENBONE_SENSOR_SCANNER_TYPE)


if __name__ == "__main__":
    unittest.main()
