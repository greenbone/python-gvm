# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgumentType, RequiredArgument


class GmpModifyPolicySetNvtSelectionTestMixin:
    def test_modify_policy_set_nvt_selection(self):
        self.gmp.modify_policy_set_nvt_selection(
            policy_id="c1", family="foo", nvt_oids=["o1"]
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<nvt_selection>"
            "<family>foo</family>"
            '<nvt oid="o1"/>'
            "</nvt_selection>"
            "</modify_config>"
        )

        self.gmp.modify_policy_set_nvt_selection(
            policy_id="c1", family="foo", nvt_oids=["o1", "o2"]
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<nvt_selection>"
            "<family>foo</family>"
            '<nvt oid="o1"/>'
            '<nvt oid="o2"/>'
            "</nvt_selection>"
            "</modify_config>"
        )

        self.gmp.modify_policy_set_nvt_selection("c1", "foo", ["o1"])

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<nvt_selection>"
            "<family>foo</family>"
            '<nvt oid="o1"/>'
            "</nvt_selection>"
            "</modify_config>"
        )

        self.gmp.modify_policy_set_nvt_selection("c1", "foo", ("o1", "o2"))

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<nvt_selection>"
            "<family>foo</family>"
            '<nvt oid="o1"/>'
            '<nvt oid="o2"/>'
            "</nvt_selection>"
            "</modify_config>"
        )

        self.gmp.modify_policy_set_nvt_selection(
            policy_id="c1", family="foo", nvt_oids=[]
        )

        self.connection.send.has_been_called_with(
            '<modify_config config_id="c1">'
            "<nvt_selection>"
            "<family>foo</family>"
            "</nvt_selection>"
            "</modify_config>"
        )

    def test_modify_policy_set_nvt_selection_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id=None, family="foo", nvt_oids=["o1"]
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id="", family="foo", nvt_oids=["o1"]
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection("", "foo", ["o1"])

    def test_modify_policy_set_nvt_selection_missing_family(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id="c1", family=None, nvt_oids=["o1"]
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id="c1", family="", nvt_oids=["o1"]
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_policy_set_nvt_selection("c1", "", ["o1"])

    def test_modify_policy_set_nvt_selection_invalid_nvt_oids(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id="c1", family="foo", nvt_oids=None
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_nvt_selection(
                policy_id="c1", family="foo", nvt_oids=""
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_policy_set_nvt_selection("c1", "foo", "")
