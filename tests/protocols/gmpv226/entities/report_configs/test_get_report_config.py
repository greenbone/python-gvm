# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from gvm.errors import RequiredArgument


class GMPGetReportConfigTestMixin:
    def test_get_report_config(self):
        self.gmp.get_report_config("report_config_id")

        self.connection.send.has_been_called_with(
            b'<get_report_configs report_config_id="report_config_id" details="1"/>',
        )

    def test_get_report_config_missing_report_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_report_config(None)
        with self.assertRaises(RequiredArgument):
            self.gmp.get_report_config("")
