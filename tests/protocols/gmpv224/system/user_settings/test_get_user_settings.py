# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetUserSettingsTestMixin:
    def test_get_settings(self):
        self.gmp.get_user_settings()

        self.connection.send.has_been_called_with(b"<get_settings/>")

    def test_get_settings_with_filter_string(self):
        self.gmp.get_user_settings(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_settings filter="foo=bar"/>'
        )
