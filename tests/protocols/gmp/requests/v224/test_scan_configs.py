# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.protocols.gmp.requests.v224 import ScanConfigs


class ScanConfigsTestCase(unittest.TestCase):

    def test_clone_scan_config(self):
        request = ScanConfigs.clone_scan_config("a1")

        self.assertEqual(
            bytes(request), b"<create_config><copy>a1</copy></create_config>"
        )

    def test_clone_scan_config_missing_id(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.clone_scan_config("")

        with self.assertRaises(RequiredArgument):
            ScanConfigs.clone_scan_config(None)

    def test_create_scan_config(self):
        request = ScanConfigs.create_scan_config("a1", "foo")

        self.assertEqual(
            bytes(request),
            b"<create_config><copy>a1</copy><name>foo</name>"
            b"<usage_type>scan</usage_type></create_config>",
        )

    def test_create_scan_config_with_comment(self):
        request = ScanConfigs.create_scan_config("a1", "foo", comment="comment")

        self.assertEqual(
            bytes(request),
            b"<create_config><comment>comment</comment><copy>a1</copy>"
            b"<name>foo</name><usage_type>scan</usage_type></create_config>",
        )

    def test_create_scan_config_missing_id(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.create_scan_config("", "foo")

        with self.assertRaises(RequiredArgument):
            ScanConfigs.create_scan_config(None, "foo")

    def test_create_scan_config_missing_name(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.create_scan_config("c1", None)

        with self.assertRaises(RequiredArgument):
            ScanConfigs.create_scan_config("c1", "")

    def test_delete_scan_config(self):
        request = ScanConfigs.delete_scan_config("a1")

        self.assertEqual(
            bytes(request), b'<delete_config config_id="a1" ultimate="0"/>'
        )

    def test_delete_scan_config_ultimate(self):
        request = ScanConfigs.delete_scan_config("a1", ultimate=True)

        self.assertEqual(
            bytes(request), b'<delete_config config_id="a1" ultimate="1"/>'
        )

    def test_delete_scan_config_missing_id(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.delete_scan_config("")

        with self.assertRaises(RequiredArgument):
            ScanConfigs.delete_scan_config(None)

    def test_get_scan_config_preference(self):
        request = ScanConfigs.get_scan_config_preference("foo")

        self.assertEqual(bytes(request), b'<get_preferences preference="foo"/>')

    def test_get_scan_config_preference_missing_name(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.get_scan_config_preference("")

        with self.assertRaises(RequiredArgument):
            ScanConfigs.get_scan_config_preference(None)

    def test_get_scan_config_preference_with_nvt_oid(self):
        request = ScanConfigs.get_scan_config_preference("foo", nvt_oid="oid")

        self.assertEqual(
            bytes(request), b'<get_preferences preference="foo" nvt_oid="oid"/>'
        )

    def test_get_scan_config_preference_with_config_id(self):
        request = ScanConfigs.get_scan_config_preference("foo", config_id="c1")

        self.assertEqual(
            bytes(request),
            b'<get_preferences preference="foo" config_id="c1"/>',
        )

    def test_get_scan_config_preferences(self):
        request = ScanConfigs.get_scan_config_preferences()

        self.assertEqual(bytes(request), b"<get_preferences/>")

    def test_get_scan_config_preferences_with_nvt_oid(self):
        request = ScanConfigs.get_scan_config_preferences(nvt_oid="oid")

        self.assertEqual(bytes(request), b'<get_preferences nvt_oid="oid"/>')

    def test_get_scan_config_preferences_with_config_id(self):
        request = ScanConfigs.get_scan_config_preferences(config_id="c1")

        self.assertEqual(bytes(request), b'<get_preferences config_id="c1"/>')

    def test_get_scan_config(self):
        request = ScanConfigs.get_scan_config("a1")

        self.assertEqual(
            bytes(request),
            b'<get_configs config_id="a1" usage_type="scan" details="1"/>',
        )

    def test_get_scan_config_with_tasks(self):
        request = ScanConfigs.get_scan_config("a1", tasks=True)

        self.assertEqual(
            bytes(request),
            b'<get_configs config_id="a1" usage_type="scan" tasks="1" details="1"/>',
        )

    def test_get_scan_config_without_scan_config_id(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.get_scan_config(None)

        with self.assertRaises(RequiredArgument):
            ScanConfigs.get_scan_config("")

    def test_get_scan_configs(self):
        request = ScanConfigs.get_scan_configs()

        self.assertEqual(bytes(request), b'<get_configs usage_type="scan"/>')

    def test_get_scan_configs_with_filter_string(self):
        request = ScanConfigs.get_scan_configs(filter_string="name=foo")

        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="scan" filter="name=foo"/>',
        )

    def test_get_scan_configs_with_filter_id(self):
        request = ScanConfigs.get_scan_configs(filter_id="f1")

        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="scan" filt_id="f1"/>',
        )

    def test_get_scan_configs_from_trash(self):
        request = ScanConfigs.get_scan_configs(trash=True)

        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="scan" trash="1"/>',
        )

    def test_get_scan_configs_with_details(self):
        request = ScanConfigs.get_scan_configs(details=True)

        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="scan" details="1"/>',
        )

    def test_get_scan_configs_without_details(self):
        request = ScanConfigs.get_scan_configs(details=False)

        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="scan" details="0"/>',
        )

    def test_get_scan_configs_with_families(self):
        request = ScanConfigs.get_scan_configs(families=True)

        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="scan" families="1"/>',
        )

    def test_get_scan_configs_without_families(self):
        request = ScanConfigs.get_scan_configs(families=False)

        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="scan" families="0"/>',
        )

    def test_get_scan_configs_with_preferences(self):
        request = ScanConfigs.get_scan_configs(preferences=True)

        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="scan" preferences="1"/>',
        )

    def test_get_scan_configs_without_preferences(self):
        request = ScanConfigs.get_scan_configs(preferences=False)

        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="scan" preferences="0"/>',
        )

    def test_get_scan_configs_with_tasks(self):
        request = ScanConfigs.get_scan_configs(tasks=True)

        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="scan" tasks="1"/>',
        )

    def test_get_scan_configs_without_tasks(self):
        request = ScanConfigs.get_scan_configs(tasks=False)

        self.assertEqual(
            bytes(request),
            b'<get_configs usage_type="scan" tasks="0"/>',
        )

    def test_import_scan_config(self):
        CONFIG_XML_STRING = (
            '<get_configs_response status="200" status_text="OK">'
            '<config id="c4aa21e4-23e6-4064-ae49-c0d425738a98">'
            "<name>Foobar</name>"
            "<comment>Foobar config</comment>"
            "<creation_time>2018-11-09T10:48:03Z</creation_time>"
            "<modification_time>2018-11-09T10:48:03Z</modification_time>"
            "</config>"
            "</get_configs_response>"
        )
        request = ScanConfigs.import_scan_config(CONFIG_XML_STRING)

        self.assertEqual(
            bytes(request),
            f"<create_config>{CONFIG_XML_STRING}</create_config>".encode(
                encoding="utf-8"
            ),
        )

    def test_import_missing_scan_config_xml(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.import_scan_config(None)

        with self.assertRaises(RequiredArgument):
            ScanConfigs.import_scan_config("")

    def test_import_invalid_xml(self):
        with self.assertRaises(InvalidArgument):
            ScanConfigs.import_scan_config("abcdef")

    def test_modify_scan_config_set_comment(self):
        request = ScanConfigs.modify_scan_config_set_comment("c1")

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1"><comment></comment></modify_config>',
        )

        request = ScanConfigs.modify_scan_config_set_comment(
            "c1", comment="foo"
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1"><comment>foo</comment></modify_config>',
        )

        request = ScanConfigs.modify_scan_config_set_comment("c1", comment=None)

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1"><comment></comment></modify_config>',
        )

    def test_modify_scan_config_set_comment_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_comment(config_id=None)

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_comment("")

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_comment(config_id="")

    def test_modify_scan_config_set_family_selection(self):
        request = ScanConfigs.modify_scan_config_set_family_selection(
            "c1", [("foo", True, True)]
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>",
        )

        request = ScanConfigs.modify_scan_config_set_family_selection(
            "c1", [("foo", True, True), ("bar", True, True)]
        )

        self.assertEqual(
            bytes(request),
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
            b"</modify_config>",
        )

        request = ScanConfigs.modify_scan_config_set_family_selection(
            "c1", (("foo", True, True), ("bar", True, True))
        )

        self.assertEqual(
            bytes(request),
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
            b"</modify_config>",
        )

        request = ScanConfigs.modify_scan_config_set_family_selection(
            "c1", [("foo", True, False), ("bar", False, True)]
        )

        self.assertEqual(
            bytes(request),
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
            b"</modify_config>",
        )

    def test_modify_scan_config_set_family_selection_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_family_selection(
                None, [("foo", True, True)]
            )

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_family_selection(
                "", [("foo", True, True)]
            )

    def test_modify_scan_config_set_family_selection_invalid_families(self):
        with self.assertRaises(InvalidArgumentType):
            ScanConfigs.modify_scan_config_set_family_selection(
                "c1",
                None,
            )

        with self.assertRaises(InvalidArgumentType):
            ScanConfigs.modify_scan_config_set_family_selection(
                "c1",
                "",
            )

    def test_modify_scan_config_set_family_selection_with_auto_add_new_families(
        self,
    ):
        request = ScanConfigs.modify_scan_config_set_family_selection(
            "c1", [("foo", True, True)], auto_add_new_families=True
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>",
        )

        request = ScanConfigs.modify_scan_config_set_family_selection(
            "c1", [("foo", True, True)], auto_add_new_families=False
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>0</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>",
        )

    def test_modify_scan_config_set_family_selection_with_auto_add_new_nvts(
        self,
    ):
        request = ScanConfigs.modify_scan_config_set_family_selection(
            "c1", [("foo", True, True)]
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>",
        )

        request = ScanConfigs.modify_scan_config_set_family_selection(
            "c1", [("foo", False, True)]
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>0</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>",
        )

        request = ScanConfigs.modify_scan_config_set_family_selection(
            "c1",
            [("foo", False, True), ("bar", True, False)],
        )

        self.assertEqual(
            bytes(request),
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
            b"</modify_config>",
        )

    def test_modify_scan_config_set_family_selection_with_invalid_arguments(
        self,
    ):
        with self.assertRaises(InvalidArgumentType):
            ScanConfigs.modify_scan_config_set_family_selection(
                "c1", [("foo", "False", "True")]
            )

        with self.assertRaises(InvalidArgumentType):
            ScanConfigs.modify_scan_config_set_family_selection(
                "c1", [("foo", True, None)]
            )

        with self.assertRaises(InvalidArgumentType):
            ScanConfigs.modify_scan_config_set_family_selection(
                "c1", [("foo", "True", False)]
            )

        with self.assertRaises(InvalidArgument):
            ScanConfigs.modify_scan_config_set_family_selection(
                "c1", [("foo",)]
            )

    def test_modify_scan_config_set_name(self):
        request = ScanConfigs.modify_scan_config_set_name("c1", "foo")

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1"><name>foo</name></modify_config>',
        )

    def test_modify_scan_config_set_name_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_name(None, name="name")

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_name("", name="name")

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_name(config_id="", name="name")

    def test_modify_scan_config_set_name_missing_name(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_name("c1", None)

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_name("c1", "")

    def test_modify_scan_config_set_nvt_preference(self):
        request = ScanConfigs.modify_scan_config_set_nvt_preference(
            "c1", nvt_oid="o1", name="foo"
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<preference>"
            b'<nvt oid="o1"/>'
            b"<name>foo</name>"
            b"</preference>"
            b"</modify_config>",
        )

        request = ScanConfigs.modify_scan_config_set_nvt_preference(
            "c1", "foo", "o1"
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<preference>"
            b'<nvt oid="o1"/>'
            b"<name>foo</name>"
            b"</preference>"
            b"</modify_config>",
        )

    def test_modify_scan_config_set_nvt_pref_with_value(self):
        request = ScanConfigs.modify_scan_config_set_nvt_preference(
            "c1", "foo", nvt_oid="o1", value="bar"
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<preference>"
            b'<nvt oid="o1"/>'
            b"<name>foo</name>"
            b"<value>YmFy</value>"
            b"</preference>"
            b"</modify_config>",
        )

    def test_modify_scan_config_set_nvt_pref_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_nvt_preference(
                "c1", "foo", nvt_oid=None, value="bar"
            )

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_nvt_preference(
                "c1", "foo", nvt_oid="", value="bar"
            )

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_nvt_preference(
                "c1", "foo", "", value="bar"
            )

    def test_modify_scan_config_nvt_pref_missing_name(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_nvt_preference(
                "c1", name=None, nvt_oid="o1", value="bar"
            )

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_nvt_preference(
                "c1", name="", nvt_oid="o1", value="bar"
            )

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_nvt_preference(
                "c1", "", nvt_oid="o1", value="bar"
            )

    def test_modify_scan_config_set_nvt_preference_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_nvt_preference("", "foo", "o1")

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_nvt_preference(None, "foo", "o1")

    def test_modify_scan_config_set_nvt_selection(self):
        request = ScanConfigs.modify_scan_config_set_nvt_selection(
            "c1", "foo", ["o1"]
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<nvt_selection>"
            b"<family>foo</family>"
            b'<nvt oid="o1"/>'
            b"</nvt_selection>"
            b"</modify_config>",
        )

        request = ScanConfigs.modify_scan_config_set_nvt_selection(
            "c1", "foo", ["o1", "o2"]
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<nvt_selection>"
            b"<family>foo</family>"
            b'<nvt oid="o1"/>'
            b'<nvt oid="o2"/>'
            b"</nvt_selection>"
            b"</modify_config>",
        )

        request = ScanConfigs.modify_scan_config_set_nvt_selection(
            "c1", "foo", ("o1", "o2")
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<nvt_selection>"
            b"<family>foo</family>"
            b'<nvt oid="o1"/>'
            b'<nvt oid="o2"/>'
            b"</nvt_selection>"
            b"</modify_config>",
        )

        request = ScanConfigs.modify_scan_config_set_nvt_selection(
            "c1", "foo", []
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<nvt_selection>"
            b"<family>foo</family>"
            b"</nvt_selection>"
            b"</modify_config>",
        )

    def test_modify_scan_config_set_nvt_selection_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_nvt_selection(
                None, "foo", ["o1"]
            )

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_nvt_selection("", "foo", ["o1"])

    def test_modify_scan_config_set_nvt_selection_invalid_nvt_oids(self):
        with self.assertRaises(InvalidArgumentType):
            ScanConfigs.modify_scan_config_set_nvt_selection("c1", "foo", None)

        with self.assertRaises(InvalidArgumentType):
            ScanConfigs.modify_scan_config_set_nvt_selection("c1", "foo", "")

    def test_modify_scan_config_set_scanner_pref(self):
        request = ScanConfigs.modify_scan_config_set_scanner_preference(
            "c1", "foo"
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<preference>"
            b"<name>foo</name>"
            b"</preference>"
            b"</modify_config>",
        )

    def test_modify_scan_config_set_scanner_pref_with_value(self):
        request = ScanConfigs.modify_scan_config_set_scanner_preference(
            "c1", "foo", value="bar"
        )

        self.assertEqual(
            bytes(request),
            b'<modify_config config_id="c1">'
            b"<preference>"
            b"<name>foo</name>"
            b"<value>YmFy</value>"
            b"</preference>"
            b"</modify_config>",
        )

    def test_modify_scan_config_scanner_pref_missing_name(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_scanner_preference(
                "c1", name=None, value="bar"
            )

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_scanner_preference(
                "c1", name="", value="bar"
            )

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_scanner_preference(
                "c1", "", value="bar"
            )

    def test_modify_scan_config_set_scanner_pref_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_scanner_preference(
                None, name="foo"
            )

        with self.assertRaises(RequiredArgument):
            ScanConfigs.modify_scan_config_set_scanner_preference(
                "", name="foo"
            )
