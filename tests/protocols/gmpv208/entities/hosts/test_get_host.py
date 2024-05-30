# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetHostTestMixin:
    def test_get_host(self):
        self.gmp.get_host("a1")

        self.connection.send.has_been_called_with(
            b'<get_assets asset_id="a1" type="host"/>'
        )

        self.gmp.get_host(host_id="a1")

        self.connection.send.has_been_called_with(
            b'<get_assets asset_id="a1" type="host"/>'
        )

    def test_get_host_details(self):
        self.gmp.get_host("a1", details=True)

        self.connection.send.has_been_called_with(
            b'<get_assets asset_id="a1" type="host" details="1"/>'
        )

        self.gmp.get_host("a1", details=False)

        self.connection.send.has_been_called_with(
            b'<get_assets asset_id="a1" type="host" details="0"/>'
        )

    def test_get_host_missing_host_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_host(
                host_id=None,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.get_host(
                host_id="",
            )
