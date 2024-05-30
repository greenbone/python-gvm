# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyPolicySetCommentTestMixin:
    def test_modify_policy_set_comment(self):
        self.gmp.modify_policy_set_comment("c1")

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<comment></comment>"
            b"</modify_config>"
        )

        self.gmp.modify_policy_set_comment("c1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<comment>foo</comment>"
            b"</modify_config>"
        )

        self.gmp.modify_policy_set_comment("c1", comment=None)

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<comment></comment>"
            b"</modify_config>"
        )

    def test_modify_policy_set_comment_missing_policy_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_comment(policy_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_comment("")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_comment(policy_id="")
