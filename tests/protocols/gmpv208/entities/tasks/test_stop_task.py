# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpStopTaskTestMixin:
    def test_stop_task(self):
        self.gmp.stop_task("a1")

        self.connection.send.has_been_called_with(b'<stop_task task_id="a1"/>')

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.stop_task(None)

        with self.assertRaises(GvmError):
            self.gmp.stop_task("")
