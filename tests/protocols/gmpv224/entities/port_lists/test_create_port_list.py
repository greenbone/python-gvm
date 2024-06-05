# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreatePortListTestMixin:
    def test_create_port_list_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_list(name=None, port_range="T:1-1234")

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_list(name="", port_range="T:1-1234")

    def test_create_port_list_missing_port_range(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_list(name="foo", port_range=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_port_list(name="foo", port_range="")

    def test_create_port_list(self):
        self.gmp.create_port_list(name="foo", port_range="T:1-1234")

        self.connection.send.has_been_called_with(
            b"<create_port_list>"
            b"<name>foo</name>"
            b"<port_range>T:1-1234</port_range>"
            b"</create_port_list>"
        )

    def test_create_port_list_with_comment(self):
        self.gmp.create_port_list(
            name="foo", port_range="T:1-1234", comment="lorem"
        )

        self.connection.send.has_been_called_with(
            b"<create_port_list>"
            b"<name>foo</name>"
            b"<port_range>T:1-1234</port_range>"
            b"<comment>lorem</comment>"
            b"</create_port_list>"
        )
