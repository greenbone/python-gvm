# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import UserSettings


class UserSettingsTestCase(unittest.TestCase):
    def test_get_user_setting(self):
        request = UserSettings.get_user_setting("id")

        self.assertEqual(bytes(request), b'<get_settings setting_id="id"/>')

    def test_get_user_setting_missing_setting_id(self):
        with self.assertRaises(RequiredArgument):
            UserSettings.get_user_setting(setting_id=None)

        with self.assertRaises(RequiredArgument):
            UserSettings.get_user_setting("")

    def test_get_user_settings(self):
        request = UserSettings.get_user_settings()

        self.assertEqual(bytes(request), b"<get_settings/>")

    def test_get_user_settings_with_filter_string(self):
        request = UserSettings.get_user_settings(filter_string="foo=bar")

        self.assertEqual(bytes(request), b'<get_settings filter="foo=bar"/>')

    def test_modify_user_setting(self):
        request = UserSettings.modify_user_setting(
            setting_id="id", value="value"
        )

        self.assertEqual(
            bytes(request),
            b'<modify_setting setting_id="id"><value>dmFsdWU=</value></modify_setting>',
        )

        request = UserSettings.modify_user_setting(name="name", value="value")

        self.assertEqual(
            bytes(request),
            b"<modify_setting><name>name</name><value>dmFsdWU=</value></modify_setting>",
        )

        request = UserSettings.modify_user_setting(name="name", value="")

        self.assertEqual(
            bytes(request),
            b"<modify_setting><name>name</name><value></value></modify_setting>",
        )

    def test_modify_user_setting_missing_setting_id(self):
        with self.assertRaises(RequiredArgument):
            UserSettings.modify_user_setting(setting_id=None, value="value")

        with self.assertRaises(RequiredArgument):
            UserSettings.modify_user_setting(setting_id="", value="value")

    def test_modify_setting_missing_name(self):
        with self.assertRaises(RequiredArgument):
            UserSettings.modify_user_setting(name=None, value="value")

        with self.assertRaises(RequiredArgument):
            UserSettings.modify_user_setting(name="", value="value")

    def test_modify_user_setting_missing_value(self):
        with self.assertRaises(RequiredArgument):
            UserSettings.modify_user_setting(setting_id="id", value=None)
