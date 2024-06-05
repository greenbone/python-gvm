# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import Nvts


class NvtsTestCase(unittest.TestCase):
    def test_get_nvt_families(self):
        request = Nvts.get_nvt_families()
        self.assertEqual(
            bytes(request),
            b"<get_nvt_families/>",
        )

    def test_get_nvt_families_with_sort_order(self):
        request = Nvts.get_nvt_families(sort_order="sort_order")
        self.assertEqual(
            bytes(request),
            b'<get_nvt_families sort_order="sort_order"/>',
        )

    def test_get_scan_config_nvts(self):
        request = Nvts.get_scan_config_nvts()
        self.assertEqual(
            bytes(request),
            b"<get_nvts/>",
        )

    def test_get_scan_config_nvts_with_details(self):
        request = Nvts.get_scan_config_nvts(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_nvts details="1"/>',
        )

        request = Nvts.get_scan_config_nvts(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_nvts details="0"/>',
        )

    def test_get_scan_config_nvts_with_preferences(self):
        request = Nvts.get_scan_config_nvts(preferences=True)
        self.assertEqual(
            bytes(request),
            b'<get_nvts preferences="1"/>',
        )

        request = Nvts.get_scan_config_nvts(preferences=False)
        self.assertEqual(
            bytes(request),
            b'<get_nvts preferences="0"/>',
        )

    def test_get_scan_config_nvts_with_preference_count(self):
        request = Nvts.get_scan_config_nvts(preference_count=True)
        self.assertEqual(
            bytes(request),
            b'<get_nvts preference_count="1"/>',
        )

        request = Nvts.get_scan_config_nvts(preference_count=False)
        self.assertEqual(
            bytes(request),
            b'<get_nvts preference_count="0"/>',
        )

    def test_get_scan_config_nvts_with_timeout(self):
        request = Nvts.get_scan_config_nvts(timeout=True)
        self.assertEqual(
            bytes(request),
            b'<get_nvts timeout="1"/>',
        )

        request = Nvts.get_scan_config_nvts(timeout=False)
        self.assertEqual(
            bytes(request),
            b'<get_nvts timeout="0"/>',
        )

    def test_get_scan_config_nvts_with_config_id(self):
        request = Nvts.get_scan_config_nvts(config_id="config_id")
        self.assertEqual(
            bytes(request),
            b'<get_nvts config_id="config_id"/>',
        )

    def test_get_scan_config_nvts_with_preferences_config_id(self):
        request = Nvts.get_scan_config_nvts(
            preferences_config_id="preferences_config_id"
        )
        self.assertEqual(
            bytes(request),
            b'<get_nvts preferences_config_id="preferences_config_id"/>',
        )

    def test_get_scan_config_nvts_with_family(self):
        request = Nvts.get_scan_config_nvts(family="family")
        self.assertEqual(
            bytes(request),
            b'<get_nvts family="family"/>',
        )

    def test_get_scan_config_nvts_with_sort_order(self):
        request = Nvts.get_scan_config_nvts(sort_order="sort_order")
        self.assertEqual(
            bytes(request),
            b'<get_nvts sort_order="sort_order"/>',
        )

    def test_get_scan_config_nvts_with_sort_field(self):
        request = Nvts.get_scan_config_nvts(sort_field="sort_field")
        self.assertEqual(
            bytes(request),
            b'<get_nvts sort_field="sort_field"/>',
        )

    def test_get_scan_config_nvt(self):
        request = Nvts.get_scan_config_nvt("nvt_oid")
        self.assertEqual(
            bytes(request),
            b'<get_nvts nvt_oid="nvt_oid" details="1" preferences="1" preference_count="1"/>',
        )

    def test_get_scan_config_nvt_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            Nvts.get_scan_config_nvt(None)

        with self.assertRaises(RequiredArgument):
            Nvts.get_scan_config_nvt("")

    def test_get_nvts(self):
        request = Nvts.get_nvts()
        self.assertEqual(
            bytes(request),
            b'<get_info type="NVT"/>',
        )

    def test_get_nvts_with_name(self):
        request = Nvts.get_nvts(name="name")
        self.assertEqual(
            bytes(request),
            b'<get_info type="NVT" name="name"/>',
        )

    def test_get_nvts_with_details(self):
        request = Nvts.get_nvts(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_info type="NVT" details="1"/>',
        )

        request = Nvts.get_nvts(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_info type="NVT" details="0"/>',
        )

    def test_get_nvts_with_extended(self):
        request = Nvts.get_nvts(extended=True)
        self.assertEqual(
            bytes(request),
            b"<get_nvts/>",
        )

        request = Nvts.get_nvts(extended=False)
        self.assertEqual(
            bytes(request),
            b'<get_info type="NVT"/>',
        )

        request = Nvts.get_nvts(
            extended=False,
            details=True,
            preferences=True,  # gets ignored
            preference_count=True,  # gets ignored
            timeout=True,  # gets ignored
            config_id="config_id",  # gets ignored
            preferences_config_id="preferences_config_id",  # gets ignored
            family="family",  # gets ignored
            sort_order="sort_order",  # gets ignored
            sort_field="sort_field",  # gets ignored
        )
        self.assertEqual(bytes(request), b'<get_info type="NVT" details="1"/>')

        request = Nvts.get_nvts(
            extended=True,
            details=True,
            preferences=True,
            preference_count=True,
            timeout=True,
            config_id="config_id",
            preferences_config_id="preferences_config_id",
            family="family",
            sort_order="sort_order",
            sort_field="sort_field",
        )
        self.assertEqual(
            bytes(request),
            b'<get_nvts details="1" preferences="1" preference_count="1" timeout="1" config_id="config_id" preferences_config_id="preferences_config_id" family="family" sort_order="sort_order" sort_field="sort_field"/>',
        )

    def test_get_nvt(self):
        request = Nvts.get_nvt("nvt_id")
        self.assertEqual(
            bytes(request),
            b'<get_info info_id="nvt_id" type="NVT" details="1"/>',
        )

    def test_get_nvt_with_extended(self):
        request = Nvts.get_nvt("nvt_id", extended=True)
        self.assertEqual(
            bytes(request),
            b'<get_nvts nvt_oid="nvt_id" details="1" preferences="1" preference_count="1"/>',
        )

        request = Nvts.get_nvt("nvt_id", extended=False)
        self.assertEqual(
            bytes(request),
            b'<get_info info_id="nvt_id" type="NVT" details="1"/>',
        )

    def test_get_nvts_missing_nvt_id(self):
        with self.assertRaises(RequiredArgument):
            Nvts.get_nvt(None)

        with self.assertRaises(RequiredArgument):
            Nvts.get_nvt("")

    def test_get_nvt_preferences(self):
        request = Nvts.get_nvt_preferences()
        self.assertEqual(
            bytes(request),
            b"<get_preferences/>",
        )

    def test_get_nvt_preferences_with_nvt_oid(self):
        request = Nvts.get_nvt_preferences(nvt_oid="nvt_oid")
        self.assertEqual(
            bytes(request),
            b'<get_preferences nvt_oid="nvt_oid"/>',
        )

    def test_get_nvt_preference(self):
        request = Nvts.get_nvt_preference("preference")
        self.assertEqual(
            bytes(request),
            b'<get_preferences preference="preference"/>',
        )

    def test_get_nvt_preference_with_nvt_oid(self):
        request = Nvts.get_nvt_preference("preference", nvt_oid="nvt_oid")
        self.assertEqual(
            bytes(request),
            b'<get_preferences preference="preference" nvt_oid="nvt_oid"/>',
        )

    def test_get_nvt_preference_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Nvts.get_nvt_preference(None)

        with self.assertRaises(RequiredArgument):
            Nvts.get_nvt_preference("")
