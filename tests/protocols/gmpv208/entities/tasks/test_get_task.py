# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpGetTaskTestMixin:
    def test_get_task(self):
        self.gmp.get_task("a1")

        self.connection.send.has_been_called_with(
            b'<get_tasks task_id="a1" usage_type="scan" details="1"/>'
        )

    def test_fail_without_task_id(self):
        with self.assertRaises(GvmError):
            self.gmp.get_task(None)

        with self.assertRaises(GvmError):
            self.gmp.get_task("")
