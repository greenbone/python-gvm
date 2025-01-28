# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GMPCloneReportConfigTestMixin:
    def test_clone_report_config(self):
        self.gmp.clone_report_config("report_config_id")

        self.connection.send.has_been_called_with(
            b"<create_report_config>"
            b"<copy>report_config_id</copy>"
            b"</create_report_config>",
        )

    def test_clone_report_config_missing_report_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_report_config(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_report_config("")
