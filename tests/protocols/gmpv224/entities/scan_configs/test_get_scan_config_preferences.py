# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetScanConfigPreferencesTestMixin:
    def test_get_scan_config_preferences(self):
        self.gmp.get_scan_config_preferences()

        self.connection.send.has_been_called_with(b"<get_preferences/>")

    def test_get_scan_config_preferences_with_nvt_oid(self):
        self.gmp.get_scan_config_preferences(nvt_oid="oid")

        self.connection.send.has_been_called_with(
            b'<get_preferences nvt_oid="oid"/>'
        )

    def test_get_scan_config_preferences_with_config_id(self):
        self.gmp.get_scan_config_preferences(config_id="c1")

        self.connection.send.has_been_called_with(
            b'<get_preferences config_id="c1"/>'
        )
