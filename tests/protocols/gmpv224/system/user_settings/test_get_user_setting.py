# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetUserSettingTestMixin:
    def test_get_setting_simple(self):
        self.gmp.get_user_setting("id")

        self.connection.send.has_been_called_with(
            b'<get_settings setting_id="id"/>'
        )

    def test_get_setting_missing_setting_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_user_setting(setting_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_user_setting("")
