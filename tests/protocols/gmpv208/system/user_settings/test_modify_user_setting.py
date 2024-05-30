# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyUserSettingTestMixin:
    def test_modify_user_setting(self):
        self.gmp.modify_user_setting(setting_id="s1", value="bar")

        self.connection.send.has_been_called_with(
            b'<modify_setting setting_id="s1">'
            b"<value>YmFy</value>"
            b"</modify_setting>"
        )

        self.gmp.modify_user_setting(name="s1", value="bar")

        self.connection.send.has_been_called_with(
            b"<modify_setting>"
            b"<name>s1</name>"
            b"<value>YmFy</value>"
            b"</modify_setting>"
        )

        self.gmp.modify_user_setting(setting_id="s1", value="")

        self.connection.send.has_been_called_with(
            b'<modify_setting setting_id="s1">'
            b"<value></value>"
            b"</modify_setting>"
        )

    def test_modify_user_setting_missing_setting_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_user_setting(setting_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_user_setting(setting_id="")

    def test_modify_setting_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_user_setting(name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_user_setting(name="")

    def test_modify_user_setting_missing_value(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_user_setting(setting_id="s1", value=None)
