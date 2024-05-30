# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetScanConfigsTestMixin:
    def test_get_scan_configs_simple(self):
        self.gmp.get_scan_configs()

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan"/>'
        )

    def test_get_scan_configs_with_filter_string(self):
        self.gmp.get_scan_configs(filter_string="name=foo")

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan" filter="name=foo"/>'
        )

    def test_get_scan_configs_with_filter_id(self):
        self.gmp.get_scan_configs(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan" filt_id="f1"/>'
        )

    def test_get_scan_configs_from_trash(self):
        self.gmp.get_scan_configs(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan" trash="1"/>'
        )

    def test_get_scan_configs_with_details(self):
        self.gmp.get_scan_configs(details=True)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan" details="1"/>'
        )

    def test_get_scan_configs_without_details(self):
        self.gmp.get_scan_configs(details=False)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan" details="0"/>'
        )

    def test_get_scan_configs_with_families(self):
        self.gmp.get_scan_configs(families=True)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan" families="1"/>'
        )

    def test_get_scan_configs_without_families(self):
        self.gmp.get_scan_configs(families=False)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan" families="0"/>'
        )

    def test_get_scan_configs_with_preferences(self):
        self.gmp.get_scan_configs(preferences=True)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan" preferences="1"/>'
        )

    def test_get_scan_configs_without_preferences(self):
        self.gmp.get_scan_configs(preferences=False)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan" preferences="0"/>'
        )

    def test_get_scan_configs_with_tasks(self):
        self.gmp.get_scan_configs(tasks=True)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan" tasks="1"/>'
        )

    def test_get_scan_configs_without_tasks(self):
        self.gmp.get_scan_configs(tasks=False)

        self.connection.send.has_been_called_with(
            b'<get_configs usage_type="scan" tasks="0"/>'
        )
