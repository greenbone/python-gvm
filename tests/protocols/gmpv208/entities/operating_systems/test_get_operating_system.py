# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetOperatingSystemTestMixin:
    def test_get_operating_system(self):
        self.gmp.get_operating_system("a1")

        self.connection.send.has_been_called_with(
            b'<get_assets asset_id="a1" type="os"/>'
        )
        self.gmp.get_operating_system(operating_system_id="a1")

        self.connection.send.has_been_called_with(
            b'<get_assets asset_id="a1" type="os"/>'
        )

    def test_get_operating_system_details(self):
        self.gmp.get_operating_system("a1", details=True)

        self.connection.send.has_been_called_with(
            b'<get_assets asset_id="a1" type="os" details="1"/>'
        )
        self.gmp.get_operating_system("a1", details=False)

        self.connection.send.has_been_called_with(
            b'<get_assets asset_id="a1" type="os" details="0"/>'
        )

    def test_get_asset_missing_operating_system_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_operating_system(operating_system_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_operating_system(operating_system_id="")
