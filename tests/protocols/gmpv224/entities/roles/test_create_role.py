# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateRoleTestMixin:
    def test_create_role(self):
        self.gmp.create_role(name="foo")

        self.connection.send.has_been_called_with(
            b"<create_role><name>foo</name></create_role>"
        )

    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_role(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_role("")

    def test_create_role_with_comment(self):
        self.gmp.create_role(name="foo", comment="bar")

        self.connection.send.has_been_called_with(
            b"<create_role>"
            b"<name>foo</name>"
            b"<comment>bar</comment>"
            b"</create_role>"
        )

    def test_create_role_with_users(self):
        self.gmp.create_role(name="foo", users=[])

        self.connection.send.has_been_called_with(
            b"<create_role><name>foo</name></create_role>"
        )

        self.gmp.create_role(name="foo", users=["u1", "u2"])

        self.connection.send.has_been_called_with(
            b"<create_role>"
            b"<name>foo</name>"
            b"<users>u1,u2</users>"
            b"</create_role>"
        )
