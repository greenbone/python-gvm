# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import OperatingSystems


class OperatingSystemsTestCase(unittest.TestCase):
    def test_delete_operating_system(self):
        request = OperatingSystems.delete_operating_system(
            "operating_system_id"
        )
        self.assertEqual(
            bytes(request),
            b'<delete_asset asset_id="operating_system_id"/>',
        )

    def test_delete_operating_system_missing_operating_system_id(self):
        with self.assertRaises(RequiredArgument):
            OperatingSystems.delete_operating_system(None)

        with self.assertRaises(RequiredArgument):
            OperatingSystems.delete_operating_system("")

    def test_get_operating_systems(self):
        request = OperatingSystems.get_operating_systems()
        self.assertEqual(
            bytes(request),
            b'<get_assets type="os"/>',
        )

    def test_get_operating_systems_with_filter_string(self):
        request = OperatingSystems.get_operating_systems(
            filter_string="filter_string"
        )
        self.assertEqual(
            bytes(request),
            b'<get_assets type="os" filter="filter_string"/>',
        )

    def test_get_operating_systems_with_filter_id(self):
        request = OperatingSystems.get_operating_systems(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_assets type="os" filt_id="filter_id"/>',
        )

    def test_get_operating_systems_with_details(self):
        request = OperatingSystems.get_operating_systems(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_assets type="os" details="1"/>',
        )

        request = OperatingSystems.get_operating_systems(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_assets type="os" details="0"/>',
        )

    def test_get_operating_system(self):
        request = OperatingSystems.get_operating_system("operating_system_id")
        self.assertEqual(
            bytes(request),
            b'<get_assets asset_id="operating_system_id" type="os"/>',
        )

    def test_get_operating_system_with_details(self):
        request = OperatingSystems.get_operating_system(
            "operating_system_id", details=True
        )
        self.assertEqual(
            bytes(request),
            b'<get_assets asset_id="operating_system_id" type="os" details="1"/>',
        )
        request = OperatingSystems.get_operating_system(
            "operating_system_id", details=False
        )
        self.assertEqual(
            bytes(request),
            b'<get_assets asset_id="operating_system_id" type="os" details="0"/>',
        )

    def test_modify_operating_system(self):
        request = OperatingSystems.modify_operating_system(
            "operating_system_id"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_asset asset_id="operating_system_id">'
            b"<comment></comment>"
            b"</modify_asset>",
        )

    def test_modify_operating_system_with_comment(self):
        request = OperatingSystems.modify_operating_system(
            "operating_system_id", comment="comment"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_asset asset_id="operating_system_id">'
            b"<comment>comment</comment>"
            b"</modify_asset>",
        )

    def test_modify_operating_system_missing_operating_system_id(self):
        with self.assertRaises(RequiredArgument):
            OperatingSystems.modify_operating_system(None)

        with self.assertRaises(RequiredArgument):
            OperatingSystems.modify_operating_system("")
