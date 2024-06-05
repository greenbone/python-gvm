# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpMoveTaskTestMixin:
    def test_move_task(self):
        self.gmp.move_task("a1")

        self.connection.send.has_been_called_with(b'<move_task task_id="a1"/>')

    def test_move_task_to_slave(self):
        self.gmp.move_task("a1", slave_id="s1")

        self.connection.send.has_been_called_with(
            b'<move_task task_id="a1" slave_id="s1"/>'
        )

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.move_task(None)

        with self.assertRaises(GvmError):
            self.gmp.move_task("")
