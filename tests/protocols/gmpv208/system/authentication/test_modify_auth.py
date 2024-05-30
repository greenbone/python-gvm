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
            b"<modify_auth>"
            b'<group name="foo">'
            b"<auth_conf_setting>"
            b"<key>foo</key>"
            b"<value>bar</value>"
            b"</auth_conf_setting>"
            b"<auth_conf_setting>"
            b"<key>lorem</key>"
            b"<value>ipsum</value>"
            b"</auth_conf_setting>"
            b"</group>"
            b"</modify_auth>"
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
