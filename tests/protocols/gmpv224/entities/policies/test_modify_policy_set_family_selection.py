# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyPolicySetFamilySelectionTestMixin:
    def test_modify_policy_set_family_selection(self):
        self.gmp.modify_policy_set_family_selection(
            policy_id="c1", families=[("foo", True, True)]
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>"
        )

        self.gmp.modify_policy_set_family_selection(
            policy_id="c1", families=(("foo", True, True), ("bar", True, True))
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"<family>"
            b"<name>bar</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>"
        )

        self.gmp.modify_policy_set_family_selection(
            policy_id="c1",
            families=[("foo", True, False), ("bar", False, True)],
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>0</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"<family>"
            b"<name>bar</name>"
            b"<all>1</all>"
            b"<growing>0</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>"
        )

    def test_modify_policy_set_family_selection_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_family_selection(
                policy_id=None, families=[("foo", True, True)]
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_family_selection(
                policy_id="", families=[("foo", True, True)]
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_family_selection(
                "", [("foo", True, True)]
            )

    def test_modify_policy_set_family_selection_invalid_families(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_family_selection(
                policy_id="c1", families=None
            )

    def test_modify_policy_set_family_selection_with_auto_add_new_families(
        self,
    ):
        self.gmp.modify_policy_set_family_selection(
            policy_id="c1",
            families=[("foo", True, True)],
            auto_add_new_families=True,
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>"
        )

        self.gmp.modify_policy_set_family_selection(
            policy_id="c1",
            families=[("foo", True, True)],
            auto_add_new_families=False,
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>0</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>"
        )

    def test_modify_policy_set_family_selection_with_auto_add_new_nvts(self):
        self.gmp.modify_policy_set_family_selection(
            policy_id="c1", families=[("foo", True, True)]
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>"
        )

        self.gmp.modify_policy_set_family_selection(
            policy_id="c1", families=[("foo", False, True)]
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>0</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>"
        )

        self.gmp.modify_policy_set_family_selection(
            policy_id="c1",
            families=[("foo", False, True), ("bar", True, False)],
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>0</growing>"
            b"</family>"
            b"<family>"
            b"<name>bar</name>"
            b"<all>0</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>"
        )
