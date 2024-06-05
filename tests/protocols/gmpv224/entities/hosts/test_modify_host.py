# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyHostTestMixin:
    def test_modify_host(self):
        self.gmp.modify_host(host_id="a1")

        self.connection.send.has_been_called_with(
            b'<modify_asset asset_id="a1">'
            b"<comment></comment>"
            b"</modify_asset>"
        )

    def test_modify_host_without_host_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_host(host_id=None, comment="foo")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_host(host_id="", comment="foo")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_host("", comment="foo")

    def test_modify_host_with_comment(self):
        self.gmp.modify_host("a1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_asset asset_id="a1">'
            b"<comment>foo</comment>"
            b"</modify_asset>"
        )

        self.gmp.modify_host("a1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_asset asset_id="a1">'
            b"<comment>foo</comment>"
            b"</modify_asset>"
        )

        self.gmp.modify_host("a1", comment="")

        self.connection.send.has_been_called_with(
            b'<modify_asset asset_id="a1">'
            b"<comment></comment>"
            b"</modify_asset>"
        )

        self.gmp.modify_host("a1", comment=None)

        self.connection.send.has_been_called_with(
            b'<modify_asset asset_id="a1">'
            b"<comment></comment>"
            b"</modify_asset>"
        )
