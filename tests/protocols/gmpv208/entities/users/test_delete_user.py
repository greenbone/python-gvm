# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpDeleteUserTestMixin:
    def test_delete_user_with_user_id(self):
        self.gmp.delete_user("a1")

        self.connection.send.has_been_called_with(
            b'<delete_user user_id="a1"/>'
        )

        self.gmp.delete_user(user_id="a1")

        self.connection.send.has_been_called_with(
            b'<delete_user user_id="a1"/>'
        )

    def test_delete_user_with_inheritor_id(self):
        self.gmp.delete_user("a1", inheritor_id="u1")

        self.connection.send.has_been_called_with(
            b'<delete_user user_id="a1" inheritor_id="u1"/>'
        )

    def test_delete_user_with_name(self):
        self.gmp.delete_user(name="foo")

        self.connection.send.has_been_called_with(b'<delete_user name="foo"/>')

    def test_delete_user_with_inheritor_name(self):
        self.gmp.delete_user("a1", inheritor_name="foo")

        self.connection.send.has_been_called_with(
            b'<delete_user user_id="a1" inheritor_name="foo"/>'
        )

    def test_delete_user_missing_user_id_and_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.delete_user(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.delete_user("")

        with self.assertRaises(RequiredArgument):
            self.gmp.delete_user(user_id="", name="")
