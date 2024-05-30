# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpStartAuditTestMixin:
    def test_start_audit(self):
        self.gmp.start_audit("a1")

        self.connection.send.has_been_called_with(b'<start_task task_id="a1"/>')

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.start_audit(None)

        with self.assertRaises(GvmError):
            self.gmp.start_audit("")
