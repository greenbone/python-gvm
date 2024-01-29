# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyPolicySetScannerPreferenceTestMixin:
    def test_modify_policy_set_scanner_pref(self):
        self.gmp.modify_policy_set_scanner_preference(
            policy_id="c1", name="foo"
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<preference>"
            "<name>foo</name>"
            "</preference>"
            "</modify_config>"
        )

        self.gmp.modify_policy_set_scanner_preference("c1", "foo")

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<preference>"
            "<name>foo</name>"
            "</preference>"
            "</modify_config>"
        )

    def test_modify_policy_set_scanner_pref_with_value(self):
        self.gmp.modify_policy_set_scanner_preference("c1", "foo", value="bar")

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<preference>"
            "<name>foo</name>"
            "<value>YmFy</value>"
            "</preference>"
            "</modify_config>"
        )

    def test_modify_policy_scanner_pref_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_scanner_preference(
                "c1", name=None, value="bar"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_scanner_preference(
                "c1", name="", value="bar"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_scanner_preference("c1", "", value="bar")

    def test_modify_policy_set_comment_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_scanner_preference(
                policy_id=None, name="foo"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_scanner_preference("", "foo")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_scanner_preference(
                policy_id="", name="foo"
            )
