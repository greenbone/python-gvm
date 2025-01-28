# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from gvm.errors import GvmError


class GMPDeleteReportConfigTestMixin:
    def test_delete(self):
        self.gmp.delete_report_config("a1")

        self.connection.send.has_been_called_with(
            b'<delete_report_config report_config_id="a1" ultimate="0"/>'
        )

    def test_delete_with_ultimate(self):
        self.gmp.delete_report_config("a1", ultimate=False)

        self.connection.send.has_been_called_with(
            b'<delete_report_config report_config_id="a1" ultimate="0"/>'
        )

        self.gmp.delete_report_config("a1", ultimate=True)

        self.connection.send.has_been_called_with(
            b'<delete_report_config report_config_id="a1" ultimate="1"/>'
        )

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_report_config(None)

        with self.assertRaises(GvmError):
            self.gmp.delete_report_config("")
