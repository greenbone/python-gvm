# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument


class GmpModifyPolicySetFamilySelectionTestMixin:
    def test_modify_policy_set_family_selection(self):
        self.gmp.modify_policy_set_family_selection(
            policy_id="c1", families=[("foo", True, True)]
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<family_selection>"
            "<growing>1</growing>"
            "<family>"
            "<name>foo</name>"
            "<all>1</all>"
            "<growing>1</growing>"
            "</family>"
            "</family_selection>"
            "</modify_config>"
        )

        self.gmp.modify_policy_set_family_selection(
            policy_id="c1", families=(("foo", True, True), ("bar", True, True))
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<family_selection>"
            "<growing>1</growing>"
            "<family>"
            "<name>foo</name>"
            "<all>1</all>"
            "<growing>1</growing>"
            "</family>"
            "<family>"
            "<name>bar</name>"
            "<all>1</all>"
            "<growing>1</growing>"
            "</family>"
            "</family_selection>"
            "</modify_config>"
        )

        self.gmp.modify_policy_set_family_selection(
            policy_id="c1",
            families=[("foo", True, False), ("bar", False, True)],
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<family_selection>"
            "<growing>1</growing>"
            "<family>"
            "<name>foo</name>"
            "<all>0</all>"
            "<growing>1</growing>"
            "</family>"
            "<family>"
            "<name>bar</name>"
            "<all>1</all>"
            "<growing>0</growing>"
            "</family>"
            "</family_selection>"
            "</modify_config>"
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
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_family_selection(
                policy_id="c1", families=None
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_family_selection(
                policy_id="c1", families=""
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_family_selection("c1", "")

    def test_modify_policy_set_family_selection_with_auto_add_new_families(
        self,
    ):
        self.gmp.modify_policy_set_family_selection(
            policy_id="c1",
            families=[("foo", True, True)],
            auto_add_new_families=True,
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<family_selection>"
            "<growing>1</growing>"
            "<family>"
            "<name>foo</name>"
            "<all>1</all>"
            "<growing>1</growing>"
            "</family>"
            "</family_selection>"
            "</modify_config>"
        )

        self.gmp.modify_policy_set_family_selection(
            policy_id="c1",
            families=[("foo", True, True)],
            auto_add_new_families=False,
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<family_selection>"
            "<growing>0</growing>"
            "<family>"
            "<name>foo</name>"
            "<all>1</all>"
            "<growing>1</growing>"
            "</family>"
            "</family_selection>"
            "</modify_config>"
        )

    def test_modify_policy_set_family_selection_with_auto_add_new_nvts(self):
        self.gmp.modify_policy_set_family_selection(
            policy_id="c1", families=[("foo", True, True)]
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<family_selection>"
            "<growing>1</growing>"
            "<family>"
            "<name>foo</name>"
            "<all>1</all>"
            "<growing>1</growing>"
            "</family>"
            "</family_selection>"
            "</modify_config>"
        )

        self.gmp.modify_policy_set_family_selection(
            policy_id="c1", families=[("foo", False, True)]
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<family_selection>"
            "<growing>1</growing>"
            "<family>"
            "<name>foo</name>"
            "<all>1</all>"
            "<growing>0</growing>"
            "</family>"
            "</family_selection>"
            "</modify_config>"
        )

        self.gmp.modify_policy_set_family_selection(
            policy_id="c1",
            families=[("foo", False, True), ("bar", True, False)],
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<family_selection>"
            "<growing>1</growing>"
            "<family>"
            "<name>foo</name>"
            "<all>1</all>"
            "<growing>0</growing>"
            "</family>"
            "<family>"
            "<name>bar</name>"
            "<all>0</all>"
            "<growing>1</growing>"
            "</family>"
            "</family_selection>"
            "</modify_config>"
        )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_family_selection(
                policy_id="c1", families=[("foo", "False", "True")]
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_family_selection(
                policy_id="c1", families=[("foo", True, None)]
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_family_selection(
                policy_id="c1", families=[("foo", "True", False)]
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_policy_set_family_selection(
                policy_id="c1", families=[("foo",)]
            )
