# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument


class GmpImportScanConfigTestMixin:
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

    def test_import_scan_config(self):
        self.gmp.import_scan_config(self.CONFIG_XML_STRING)

        self.connection.send.has_been_called_with(
            f"<create_config>{self.CONFIG_XML_STRING}</create_config>".encode(
                "utf-8"
            )
        )

    def test_import_missing_scan_config_xml(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.import_scan_config(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.import_scan_config("")

    def test_import_invalid_xml(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.import_scan_config("abcdef")
