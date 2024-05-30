# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpDeleteScanConfigTestMixin:
    def test_delete_scan_config(self):
        self.gmp.delete_scan_config("a1")

        self.connection.send.has_been_called_with(
            b'<delete_config config_id="a1" ultimate="0"/>'
        )

    def test_delete_scan_config_ultimate(self):
        self.gmp.delete_scan_config("a1", ultimate=True)

        self.connection.send.has_been_called_with(
            b'<delete_config config_id="a1" ultimate="1"/>'
        )

    def test_delete_scan_config_missing_scan_config_id(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_scan_config(None)

        with self.assertRaises(GvmError):
            self.gmp.delete_scan_config("")
