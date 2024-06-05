# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyPolicySetNameTestMixin:
    def test_modify_policy_set_name(self):
        self.gmp.modify_policy_set_name("c1", "foo")

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<name>foo</name>"
            b"</modify_config>"
        )

    def test_modify_policy_set_name_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_name(policy_id=None, name="name")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_name("", name="name")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_name(policy_id="", name="name")

    def test_modify_policy_set_name_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_name(policy_id="c", name="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_name(policy_id="c", name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_name("c", "")
