# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from collections import OrderedDict

from gvm.errors import RequiredArgument


class GmpModifyAuthTestMixin:
    def test_modify_auth(self):
        self.gmp.modify_auth(
            "foo", OrderedDict([("foo", "bar"), ("lorem", "ipsum")])
        )

        self.connection.send.has_been_called_with(
            "<modify_auth>"
            '<group name="foo">'
            "<auth_conf_setting>"
            "<key>foo</key>"
            "<value>bar</value>"
            "</auth_conf_setting>"
            "<auth_conf_setting>"
            "<key>lorem</key>"
            "<value>ipsum</value>"
            "</auth_conf_setting>"
            "</group>"
            "</modify_auth>"
        )

    def test_modify_auth_missing_group_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth(
                group_name=None, auth_conf_settings={"foo": "bar"}
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth(
                group_name="", auth_conf_settings={"foo": "bar"}
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth("", auth_conf_settings={"foo": "bar"})

    def test_modify_auth_auth_conf_settings(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth(group_name="foo", auth_conf_settings=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth(group_name="foo", auth_conf_settings="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth("foo", "")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_auth("foo", {})
