# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyScanConfigSetNvtPreferenceTestMixin:
    def test_modify_scan_config_set_nvt_pref(self):
        self.gmp.modify_scan_config_set_nvt_preference(
            config_id="c1", nvt_oid="o1", name="foo"
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<preference>"
            b'<nvt oid="o1"/>'
            b"<name>foo</name>"
            b"</preference>"
            b"</modify_config>"
        )

        self.gmp.modify_scan_config_set_nvt_preference("c1", "foo", "o1")

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<preference>"
            b'<nvt oid="o1"/>'
            b"<name>foo</name>"
            b"</preference>"
            b"</modify_config>"
        )

    def test_modify_scan_config_set_nvt_pref_with_value(self):
        self.gmp.modify_scan_config_set_nvt_preference(
            "c1", "foo", nvt_oid="o1", value="bar"
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<preference>"
            b'<nvt oid="o1"/>'
            b"<name>foo</name>"
            b"<value>YmFy</value>"
            b"</preference>"
            b"</modify_config>"
        )

    def test_modify_scan_config_set_nvt_pref_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_nvt_preference(
                "c1", "foo", nvt_oid=None, value="bar"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_nvt_preference(
                "c1", "foo", nvt_oid="", value="bar"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_nvt_preference(
                "c1", "foo", "", value="bar"
            )

    def test_modify_scan_config_nvt_pref_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_nvt_preference(
                "c1", name=None, nvt_oid="o1", value="bar"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_nvt_preference(
                "c1", name="", nvt_oid="o1", value="bar"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_nvt_preference(
                "c1", "", nvt_oid="o1", value="bar"
            )

    def test_modify_scan_config_set_comment_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_nvt_preference(
                config_id=None, name="foo", nvt_oid="o1"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_nvt_preference("", "foo", "o1")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_nvt_preference(
                config_id="", name="foo", nvt_oid="o1"
            )
