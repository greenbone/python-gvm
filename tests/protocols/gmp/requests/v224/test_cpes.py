# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import Cpes


class CpesTestCase(unittest.TestCase):
    def test_get_cpes(self):
        request = Cpes.get_cpes()
        self.assertEqual(
            bytes(request),
            b'<get_info type="CPE"/>',
        )

    def test_get_cpes_with_filter_string(self):
        request = Cpes.get_cpes(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_info type="CPE" filter="filter_string"/>',
        )

    def test_get_cpes_with_filter_id(self):
        request = Cpes.get_cpes(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_info type="CPE" filt_id="filter_id"/>',
        )

    def test_get_cpes_with_name(self):
        request = Cpes.get_cpes(name="name")
        self.assertEqual(
            bytes(request),
            b'<get_info type="CPE" name="name"/>',
        )

    def test_get_cpes_with_details(self):
        request = Cpes.get_cpes(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_info type="CPE" details="1"/>',
        )

        request = Cpes.get_cpes(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_info type="CPE" details="0"/>',
        )

    def test_get_cpe(self):
        request = Cpes.get_cpe("cpe_id")
        self.assertEqual(
            bytes(request),
            b'<get_info info_id="cpe_id" type="CPE" details="1"/>',
        )

    def test_get_cpe_missing_cpe_id(self):
        with self.assertRaises(RequiredArgument):
            Cpes.get_cpe(None)

        with self.assertRaises(RequiredArgument):
            Cpes.get_cpe("")
