# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateScanConfigFromOSPScannerTestMixin:
    def test_create_scan_config_from_osp_scanner(self):
        self.gmp.create_scan_config_from_osp_scanner("a1", "foo")

        self.connection.send.has_been_called_with(
            "<create_config>"
            "<scanner>a1</scanner>"
            "<name>foo</name>"
            "<usage_type>scan</usage_type>"
            "</create_config>"
        )

    def test_create_scan_config_from_osp_scanner_with_comment(self):
        self.gmp.create_scan_config_from_osp_scanner(
            "a1", "foo", comment="comment"
        )

        self.connection.send.has_been_called_with(
            "<create_config>"
            "<comment>comment</comment>"
            "<scanner>a1</scanner>"
            "<name>foo</name>"
            "<usage_type>scan</usage_type>"
            "</create_config>"
        )

    def test_create_scan_config_from_osp_scanner_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scan_config_from_osp_scanner(
                scanner_id="", name="foo"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scan_config_from_osp_scanner(
                scanner_id=None, name="foo"
            )

    def test_create_scan_config_from_osp_scanner_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scan_config_from_osp_scanner(
                scanner_id="c1", name=None
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scan_config_from_osp_scanner(
                scanner_id="c1", name=""
            )
