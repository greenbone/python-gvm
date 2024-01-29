# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpResumeTaskTestMixin:
    def test_resume_task(self):
        self.gmp.resume_task("a1")

        self.connection.send.has_been_called_with('<resume_task task_id="a1"/>')

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.resume_task(None)

        with self.assertRaises(GvmError):
            self.gmp.resume_task("")
