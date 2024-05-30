# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyScanConfigSetScannerPreferenceTestMixin:
    def test_modify_scan_config_set_scanner_pref(self):
        self.gmp.modify_scan_config_set_scanner_preference(
            config_id="c1", name="foo"
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<preference>"
            b"<name>foo</name>"
            b"</preference>"
            b"</modify_config>"
        )

        self.gmp.modify_scan_config_set_scanner_preference("c1", "foo")

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<preference>"
            b"<name>foo</name>"
            b"</preference>"
            b"</modify_config>"
        )

    def test_modify_scan_config_set_scanner_pref_with_value(self):
        self.gmp.modify_scan_config_set_scanner_preference(
            "c1", "foo", value="bar"
        )

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<preference>"
            b"<name>foo</name>"
            b"<value>YmFy</value>"
            b"</preference>"
            b"</modify_config>"
        )

    def test_modify_scan_config_scanner_pref_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_scanner_preference(
                "c1", name=None, value="bar"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_scanner_preference(
                "c1", name="", value="bar"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_scanner_preference(
                "c1", "", value="bar"
            )

    def test_modify_scan_config_set_comment_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_scanner_preference(
                config_id=None, name="foo"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_scanner_preference("", "foo")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_scanner_preference(
                config_id="", name="foo"
            )
