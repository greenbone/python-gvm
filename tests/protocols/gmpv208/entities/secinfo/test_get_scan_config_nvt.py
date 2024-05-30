# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetScanConfigNvtTestMixin:
    def test_get_scan_config_nvt_with_nvt_oid(self):
        self.gmp.get_scan_config_nvt(nvt_oid="nvt_oid")

        self.connection.send.has_been_called_with(
            b'<get_nvts nvt_oid="nvt_oid" details="1" '
            b'preferences="1" preference_count="1"/>'
        )

    def test_get_scan_config_nvt_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_scan_config_nvt(nvt_oid=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_scan_config_nvt(nvt_oid="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_scan_config_nvt("")
