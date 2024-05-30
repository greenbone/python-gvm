# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpResumeAuditTestMixin:
    def test_resume_audit(self):
        self.gmp.resume_audit("a1")

        self.connection.send.has_been_called_with(
            b'<resume_task task_id="a1"/>'
        )

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.resume_audit(None)

        with self.assertRaises(GvmError):
            self.gmp.resume_audit("")
