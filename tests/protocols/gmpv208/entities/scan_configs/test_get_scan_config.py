# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpGetScanConfigTestMixin:
    def test_get_scan_config(self):
        self.gmp.get_scan_config("a1")

        self.connection.send.has_been_called_with(
            b'<get_configs config_id="a1" usage_type="scan" details="1"/>'
        )

    def test_get_scan_config_with_tasks(self):
        self.gmp.get_scan_config("a1", tasks=True)

        self.connection.send.has_been_called_with(
            b'<get_configs config_id="a1" usage_type="scan" '
            b'tasks="1" details="1"/>'
        )

    def test_get_scan_config_fail_without_scan_config_id(self):
        with self.assertRaises(GvmError):
            self.gmp.get_scan_config(None)

        with self.assertRaises(GvmError):
            self.gmp.get_scan_config("")
