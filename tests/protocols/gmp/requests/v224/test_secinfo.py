# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import SecInfo


class SecInfoTestCase(unittest.TestCase):
    def test_get_info(self):
        request = SecInfo.get_info("info_id", "NVT")
        self.assertEqual(
            bytes(request),
            b'<get_info info_id="info_id" type="NVT" details="1"/>',
        )

    def test_get_info_missing_info_id(self):
        with self.assertRaises(RequiredArgument):
            SecInfo.get_info(None, "NVT")

        with self.assertRaises(RequiredArgument):
            SecInfo.get_info("", "NVT")

    def test_get_info_missing_info_type(self):
        with self.assertRaises(RequiredArgument):
            SecInfo.get_info("info_id", None)

        with self.assertRaises(RequiredArgument):
            SecInfo.get_info("info_id", "")

    def test_get_info_invalid_info_type(self):
        with self.assertRaises(InvalidArgument):
            SecInfo.get_info("info_id", "invalid")

    def test_get_info_list(self):
        request = SecInfo.get_info_list("nvt")
        self.assertEqual(
            bytes(request),
            b'<get_info type="NVT"/>',
        )

    def test_get_info_list_with_details(self):
        request = SecInfo.get_info_list("nvt", details=True)
        self.assertEqual(
            bytes(request),
            b'<get_info type="NVT" details="1"/>',
        )

        request = SecInfo.get_info_list("nvt", details=False)
        self.assertEqual(
            bytes(request),
            b'<get_info type="NVT" details="0"/>',
        )

    def test_get_info_list_with_filter_string(self):
        request = SecInfo.get_info_list("nvt", filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_info type="NVT" filter="filter_string"/>',
        )

    def test_get_info_list_with_filter_id(self):
        request = SecInfo.get_info_list("nvt", filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_info type="NVT" filt_id="filter_id"/>',
        )

    def test_get_info_list_with_name(self):
        request = SecInfo.get_info_list("nvt", name="name")
        self.assertEqual(
            bytes(request),
            b'<get_info type="NVT" name="name"/>',
        )

    def test_get_info_list_missing_info_type(self):
        with self.assertRaises(RequiredArgument):
            SecInfo.get_info_list(None)

        with self.assertRaises(RequiredArgument):
            SecInfo.get_info_list("")

    def test_get_info_list_invalid_info_type(self):
        with self.assertRaises(InvalidArgument):
            SecInfo.get_info_list("invalid")
