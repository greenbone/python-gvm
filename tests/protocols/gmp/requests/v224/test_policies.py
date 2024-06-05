# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import Policies

POLICY_XML_STRING = (
    '<get_configs_response status="200" status_text="OK">'
    '<config id="c4aa21e4-23e6-4064-ae49-c0d425738a98">'
    "<name>Foobar</name>"
    "<comment>Foobar config</comment>"
    "<creation_time>2018-11-09T10:48:03Z</creation_time>"
    "<modification_time>2018-11-09T10:48:03Z</modification_time>"
    "</config>"
    "</get_configs_response>"
)


class PoliciesTestCase(unittest.TestCase):
    def test_clone_policy(self):
        request = Policies.clone_policy("policy_id")
        self.assertEqual(
            bytes(request),
            b"<create_config><copy>policy_id</copy></create_config>",
        )

    def test_clone_policy_missing_policy_id(self):
        with self.assertRaises(RequiredArgument):
            Policies.clone_policy(None)

        with self.assertRaises(RequiredArgument):
            Policies.clone_policy("")

    def test_create_policy(self):
        request = Policies.create_policy("name")
        self.assertEqual(
            bytes(request),
            b"<create_config>"
            b"<copy>085569ce-73ed-11df-83c3-002264764cea</copy>"
            b"<name>name</name>"
            b"<usage_type>policy</usage_type>"
            b"</create_config>",
        )

    def test_create_policy_with_policy_id(self):
        request = Policies.create_policy("name", policy_id="policy_id")
        self.assertEqual(
            bytes(request),
            b"<create_config>"
            b"<copy>policy_id</copy>"
            b"<name>name</name>"
            b"<usage_type>policy</usage_type>"
            b"</create_config>",
        )

    def test_create_policy_with_comment(self):
        request = Policies.create_policy("name", comment="comment")
        self.assertEqual(
            bytes(request),
            b"<create_config>"
            b"<comment>comment</comment>"
            b"<copy>085569ce-73ed-11df-83c3-002264764cea</copy>"
            b"<name>name</name>"
            b"<usage_type>policy</usage_type>"
            b"</create_config>",
        )

    def test_delete_policy(self):
        request = Policies.delete_policy("policy_id")
        self.assertEqual(
            bytes(request),
            b'<delete_config config_id="policy_id" ultimate="0"/>',
        )

    def test_delete_policy_with_ultimate(self):
        request = Policies.delete_policy("policy_id", ultimate=True)
        self.assertEqual(
            bytes(request),
            b'<delete_config config_id="policy_id" ultimate="1"/>',
        )

        request = Policies.delete_policy("policy_id", ultimate=False)
        self.assertEqual(
            bytes(request),
            b'<delete_config config_id="policy_id" ultimate="0"/>',
        )

    def test_get_policies(self):
        request = Policies.get_policies()
        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="policy"/>',
        )

    def test_get_policies_with_trash(self):
        request = Policies.get_policies(trash=True)
        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="policy" trash="1"/>',
        )

        request = Policies.get_policies(trash=False)
        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="policy" trash="0"/>',
        )

    def test_get_policies_with_details(self):
        request = Policies.get_policies(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="policy" details="1"/>',
        )

        request = Policies.get_policies(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="policy" details="0"/>',
        )

    def test_get_policies_with_families(self):
        request = Policies.get_policies(families=True)
        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="policy" families="1"/>',
        )

        request = Policies.get_policies(families=False)
        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="policy" families="0"/>',
        )

    def test_get_policies_with_preferences(self):
        request = Policies.get_policies(preferences=True)
        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="policy" preferences="1"/>',
        )

        request = Policies.get_policies(preferences=False)
        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="policy" preferences="0"/>',
        )

    def test_get_policies_with_audits(self):
        request = Policies.get_policies(audits=True)
        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="policy" tasks="1"/>',
        )

        request = Policies.get_policies(audits=False)
        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="policy" tasks="0"/>',
        )

    def test_get_policy(self):
        request = Policies.get_policy("policy_id")
        self.assertEqual(
            bytes(request),
            b'<get_configs config_id="policy_id" usage_type="policy" details="1"/>',
        )

    def test_get_policy_with_audits(self):
        request = Policies.get_policy("policy_id", audits=True)
        self.assertEqual(
            bytes(request),
            b'<get_configs config_id="policy_id" usage_type="policy" tasks="1" details="1"/>',
        )

        request = Policies.get_policy("policy_id", audits=False)
        self.assertEqual(
            bytes(request),
            b'<get_configs config_id="policy_id" usage_type="policy" tasks="0" details="1"/>',
        )

    def test_get_policy_missing_policy_id(self):
        with self.assertRaises(RequiredArgument):
            Policies.get_policy(None)

        with self.assertRaises(RequiredArgument):
            Policies.get_policy("")

    def test_import_policy(self):
        request = Policies.import_policy(POLICY_XML_STRING)
        self.assertEqual(
            bytes(request),
            b"<create_config>"
            b'<get_configs_response status="200" status_text="OK">'
            b'<config id="c4aa21e4-23e6-4064-ae49-c0d425738a98">'
            b"<name>Foobar</name>"
            b"<comment>Foobar config</comment>"
            b"<creation_time>2018-11-09T10:48:03Z</creation_time>"
            b"<modification_time>2018-11-09T10:48:03Z</modification_time>"
            b"</config>"
            b"</get_configs_response>"
            b"</create_config>",
        )

    def test_import_policy_missing_policy_xml(self):
        with self.assertRaises(RequiredArgument):
            Policies.import_policy(None)

        with self.assertRaises(RequiredArgument):
            Policies.import_policy("")

    def test_import_policy_invalid_xml(self):
        with self.assertRaises(InvalidArgument):
            Policies.import_policy("abcdef")

    def test_modify_policy_set_nvt_preference(self):
        request = Policies.modify_policy_set_nvt_preference(
            "policy_id", "name", "oid"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<preference>"
            b'<nvt oid="oid"/>'
            b"<name>name</name>"
            b"</preference>"
            b"</modify_config>",
        )

    def test_modify_policy_set_nvt_preference_with_value(self):
        request = Policies.modify_policy_set_nvt_preference(
            "policy_id", "name", "oid", value="bar"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<preference>"
            b'<nvt oid="oid"/>'
            b"<name>name</name>"
            b"<value>YmFy</value>"
            b"</preference>"
            b"</modify_config>",
        )

    def test_modify_policy_set_nvt_preference_missing_policy_id(self):
        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_nvt_preference(None, "name", "oid")

        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_nvt_preference("", "name", "oid")

    def test_modify_policy_set_nvt_preference_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_nvt_preference("policy_id", None, "oid")

        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_nvt_preference("policy_id", "", "oid")

    def test_modify_policy_set_nvt_preference_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_nvt_preference("policy_id", "name", None)

        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_nvt_preference("policy_id", "name", "")

    def test_modify_policy_set_name(self):
        request = Policies.modify_policy_set_name("policy_id", "name")
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<name>name</name>"
            b"</modify_config>",
        )

    def test_modify_policy_set_name_missing_policy_id(self):
        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_name(None, "name")

        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_name("", "name")

    def test_modify_policy_set_name_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_name("policy_id", None)

        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_name("policy_id", "")

    def test_modify_policy_set_comment(self):
        request = Policies.modify_policy_set_comment("policy_id", None)
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<comment></comment>"
            b"</modify_config>",
        )

        request = Policies.modify_policy_set_comment("policy_id", "comment")
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<comment>comment</comment>"
            b"</modify_config>",
        )

    def test_modify_policy_set_comment_missing_policy_id(self):
        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_comment(None, "comment")

        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_comment("", "comment")

    def test_modify_policy_set_scanner_preference(self):
        request = Policies.modify_policy_set_scanner_preference(
            "policy_id",
            "name",
        )
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<preference>"
            b"<name>name</name>"
            b"</preference>"
            b"</modify_config>",
        )

    def test_modify_policy_set_scanner_preference_with_value(self):
        request = Policies.modify_policy_set_scanner_preference(
            "policy_id",
            "name",
            value="bar",
        )
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<preference>"
            b"<name>name</name>"
            b"<value>YmFy</value>"
            b"</preference>"
            b"</modify_config>",
        )

    def test_modify_policy_set_scanner_preference_missing_policy_id(self):
        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_scanner_preference(None, "name")

        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_scanner_preference("", "name")

    def test_modify_policy_set_scanner_preference_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_scanner_preference("policy_id", None)

        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_scanner_preference("policy_id", "")

    def test_modify_policy_set_nvt_selection(self):
        request = Policies.modify_policy_set_nvt_selection(
            "policy_id",
            "name",
            ["oid"],
        )
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<nvt_selection>"
            b"<family>name</family>"
            b'<nvt oid="oid"/>'
            b"</nvt_selection>"
            b"</modify_config>",
        )

        request = Policies.modify_policy_set_nvt_selection(
            "policy_id",
            "name",
            ["oid1", "oid2"],
        )
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<nvt_selection>"
            b"<family>name</family>"
            b'<nvt oid="oid1"/>'
            b'<nvt oid="oid2"/>'
            b"</nvt_selection>"
            b"</modify_config>",
        )

    def test_modify_policy_set_nvt_selection_missing_policy_id(self):
        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_nvt_selection(None, "name", ["oid"])

        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_nvt_selection("", "name", ["oid"])

    def test_modify_policy_set_nvt_selection_missing_family(self):
        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_nvt_selection("policy_id", None, ["oid"])

        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_nvt_selection("policy_id", "", ["oid"])

    def test_modify_policy_set_family_selection(self):
        request = Policies.modify_policy_set_family_selection(
            "policy_id",
            [("name", True, True)],
        )
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>name</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>",
        )

        request = Policies.modify_policy_set_family_selection(
            "policy_id",
            [("name1", True, True), ("name2", True, False)],
        )
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>name1</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"<family>"
            b"<name>name2</name>"
            b"<all>0</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>",
        )

    def test_modify_policy_set_family_selection_with_auto_add_new_families(
        self,
    ):
        request = Policies.modify_policy_set_family_selection(
            "policy_id",
            [("name", True, True)],
            auto_add_new_families=True,
        )
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>name</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>",
        )

        request = Policies.modify_policy_set_family_selection(
            "policy_id",
            [("name", True, True)],
            auto_add_new_families=False,
        )
        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="policy_id">'
            b"<family_selection>"
            b"<growing>0</growing>"
            b"<family>"
            b"<name>name</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>",
        )

    def test_modify_policy_set_family_selection_missing_policy_id(self):
        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_family_selection(
                None, [("name", True, True)]
            )

        with self.assertRaises(RequiredArgument):
            Policies.modify_policy_set_family_selection(
                "", [("name", True, True)]
            )

    def test_modify_policy_set_family_selection_invalid_families(self):
        with self.assertRaises(InvalidArgument):
            Policies.modify_policy_set_family_selection(
                "policy_id", [("name", True, True, True)]
            )

        with self.assertRaises(InvalidArgument):
            Policies.modify_policy_set_family_selection(
                "policy_id", [("name", True)]
            )
