# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetUsersTestMixin:
    def test_get_users(self):
        self.gmp.get_users()

        self.connection.send.has_been_called_with(b"<get_users/>")

    def test_get_users_with_filter_string(self):
        self.gmp.get_users(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_users filter="foo=bar"/>'
        )

    def test_get_users_with_filter_id(self):
        self.gmp.get_users(filter_id="f1")

        self.connection.send.has_been_called_with(b'<get_users filt_id="f1"/>')
