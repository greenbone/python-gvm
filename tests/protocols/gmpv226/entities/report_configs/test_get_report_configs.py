# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GMPGetReportConfigsTestMixin:
    def test_get_report_configs(self):
        self.gmp.get_report_configs()

        self.connection.send.has_been_called_with(
            b"<get_report_configs/>",
        )

    def test_get_report_configs_with_filter_string(self):
        self.gmp.get_report_configs(filter_string="filter_string")

        self.connection.send.has_been_called_with(
            b'<get_report_configs filter="filter_string"/>',
        )

    def test_get_report_configs_with_filter_id(self):
        self.gmp.get_report_configs(filter_id="filter_id")

        self.connection.send.has_been_called_with(
            b'<get_report_configs filt_id="filter_id"/>',
        )

    def test_get_report_configs_with_details(self):
        self.gmp.get_report_configs(details=True)

        self.connection.send.has_been_called_with(
            b'<get_report_configs details="1"/>',
        )

    def test_get_report_configs_with_trash(self):
        self.gmp.get_report_configs(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_report_configs trash="1"/>',
        )
