# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateHostTestMixin:
    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_host(name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_host(name="")

    def test_create_host_asset(self):
        self.gmp.create_host(name="ipsum")

        self.connection.send.has_been_called_with(
            "<create_asset>"
            "<asset>"
            "<type>host</type>"
            "<name>ipsum</name>"
            "</asset>"
            "</create_asset>"
        )

    def test_create_asset_with_comment(self):
        self.gmp.create_host(name="ipsum", comment="lorem")

        self.connection.send.has_been_called_with(
            "<create_asset>"
            "<asset>"
            "<type>host</type>"
            "<name>ipsum</name>"
            "<comment>lorem</comment>"
            "</asset>"
            "</create_asset>"
        )
