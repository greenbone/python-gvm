# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpDeleteAuditReportTestMixin:
    def test_delete(self):
        self.gmp.delete_report("a1")

        self.connection.send.has_been_called_with(
            b'<delete_report report_id="a1"/>'
        )

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_report(None)

        with self.assertRaises(GvmError):
            self.gmp.delete_report("")
