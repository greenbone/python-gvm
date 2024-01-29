# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpAuthenticateTestMixin:
    def test_missing_username(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.authenticate(None, "foo")

        with self.assertRaises(RequiredArgument):
            self.gmp.authenticate("", "foo")

    def test_missing_password(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.authenticate("bar", None)

        with self.assertRaises(RequiredArgument):
            self.gmp.authenticate("bar", "")

    def test_authentication_success(self):
        self.assertFalse(self.gmp.is_authenticated())

        self.gmp.authenticate("foo", "bar")

        self.connection.send.has_been_called_with(
            "<authenticate>"
            "<credentials>"
            "<username>foo</username>"
            "<password>bar</password>"
            "</credentials>"
            "</authenticate>"
        )

        self.assertTrue(self.gmp.is_authenticated())

    def test_authentication_failure(self):
        self.connection.read.return_value(
            '<authentication_response status="400" status_text="Auth failed"/>'
        )

        self.assertFalse(self.gmp.is_authenticated())

        self.gmp.authenticate("foo", "bar")

        self.connection.send.has_been_called_with(
            "<authenticate>"
            "<credentials>"
            "<username>foo</username>"
            "<password>bar</password>"
            "</credentials>"
            "</authenticate>"
        )

        self.assertFalse(self.gmp.is_authenticated())
