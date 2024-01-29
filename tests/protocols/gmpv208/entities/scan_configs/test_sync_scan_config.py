# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpSyncScanConfigTestMixin:
    def test_sync_scan_config(self):
        self.gmp.sync_scan_config()

        self.connection.send.has_been_called_with("<sync_config/>")
