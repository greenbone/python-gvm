# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetUserTestMixin:
    def test_get_user(self):
        self.gmp.get_user("u1")

        self.connection.send.has_been_called_with(b'<get_users user_id="u1"/>')

        self.gmp.get_user(user_id="u1")

        self.connection.send.has_been_called_with(b'<get_users user_id="u1"/>')

    def test_get_user_missing_user_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_user(user_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_user("")
