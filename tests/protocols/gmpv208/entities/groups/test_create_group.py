# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateGroupTestMixin:
    def test_create_group(self):
        self.gmp.create_group(name="foo")

        self.connection.send.has_been_called_with(
            "<create_group><name>foo</name></create_group>"
        )

    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_group(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_group("")

    def test_create_group_with_comment(self):
        self.gmp.create_group(name="foo", comment="bar")

        self.connection.send.has_been_called_with(
            "<create_group>"
            "<name>foo</name>"
            "<comment>bar</comment>"
            "</create_group>"
        )

    def test_create_special_group(self):
        self.gmp.create_group(name="foo", special=True)

        self.connection.send.has_been_called_with(
            "<create_group>"
            "<name>foo</name>"
            "<specials>"
            "<full/>"
            "</specials>"
            "</create_group>"
        )

    def test_create_group_with_users(self):
        self.gmp.create_group(name="foo", users=[])

        self.connection.send.has_been_called_with(
            "<create_group><name>foo</name></create_group>"
        )

        self.gmp.create_group(name="foo", users=["u1", "u2"])

        self.connection.send.has_been_called_with(
            "<create_group>"
            "<name>foo</name>"
            "<users>u1,u2</users>"
            "</create_group>"
        )
