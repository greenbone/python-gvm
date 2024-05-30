# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateUserTestMixin:
    def test_create_user_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_user(name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_user(name="")

    def test_create_user(self):
        self.gmp.create_user(name="foo")

        self.connection.send.has_been_called_with(
            b"<create_user><name>foo</name></create_user>"
        )

    def test_create_user_with_password(self):
        self.gmp.create_user(name="foo", password="bar")

        self.connection.send.has_been_called_with(
            b"<create_user>"
            b"<name>foo</name>"
            b"<password>bar</password>"
            b"</create_user>"
        )

    def test_create_user_with_hosts(self):
        self.gmp.create_user(name="foo", hosts=["h1", "h2"], hosts_allow=True)

        self.connection.send.has_been_called_with(
            b"<create_user>"
            b"<name>foo</name>"
            b'<hosts allow="1">h1,h2</hosts>'
            b"</create_user>"
        )

        self.gmp.create_user(name="foo", hosts=["h1", "h2"])

        self.connection.send.has_been_called_with(
            b"<create_user>"
            b"<name>foo</name>"
            b'<hosts allow="0">h1,h2</hosts>'
            b"</create_user>"
        )

        self.gmp.create_user(name="foo", hosts=["h1", "h2"], hosts_allow=False)

        self.connection.send.has_been_called_with(
            b"<create_user>"
            b"<name>foo</name>"
            b'<hosts allow="0">h1,h2</hosts>'
            b"</create_user>"
        )

    def test_create_user_with_role_ids(self):
        self.gmp.create_user(name="foo", role_ids=["r1", "r2"])

        self.connection.send.has_been_called_with(
            b"<create_user>"
            b"<name>foo</name>"
            b'<role id="r1"/>'
            b'<role id="r2"/>'
            b"</create_user>"
        )
