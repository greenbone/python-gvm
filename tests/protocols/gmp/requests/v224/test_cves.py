# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import Cves


class CvesTestCase(unittest.TestCase):
    def test_get_cves(self):
        request = Cves.get_cves()
        self.assertEqual(
            bytes(request),
            b'<get_info type="CVE"/>',
        )

    def test_get_cves_with_filter_string(self):
        request = Cves.get_cves(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_info type="CVE" filter="filter_string"/>',
        )

    def test_get_cves_with_filter_id(self):
        request = Cves.get_cves(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_info type="CVE" filt_id="filter_id"/>',
        )

    def test_get_cves_with_name(self):
        request = Cves.get_cves(name="name")
        self.assertEqual(
            bytes(request),
            b'<get_info type="CVE" name="name"/>',
        )

    def test_get_cves_with_details(self):
        request = Cves.get_cves(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_info type="CVE" details="1"/>',
        )

        request = Cves.get_cves(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_info type="CVE" details="0"/>',
        )

    def test_get_cve(self):
        request = Cves.get_cve("cve_id")
        self.assertEqual(
            bytes(request),
            b'<get_info info_id="cve_id" type="CVE" details="1"/>',
        )

    def test_get_cve_missing_cve_id(self):
        with self.assertRaises(RequiredArgument):
            Cves.get_cve(None)

        with self.assertRaises(RequiredArgument):
            Cves.get_cve("")
