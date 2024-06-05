# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetTargetTestMixin:
    def test_get_target(self):
        self.gmp.get_target("t1")

        self.connection.send.has_been_called_with(
            b'<get_targets target_id="t1"/>'
        )

        self.gmp.get_target(target_id="t1")

        self.connection.send.has_been_called_with(
            b'<get_targets target_id="t1"/>'
        )

    def test_get_target_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_target(target_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_target("")

    def test_get_target_with_tasks(self):
        self.gmp.get_target(target_id="t1", tasks=True)

        self.connection.send.has_been_called_with(
            b'<get_targets target_id="t1" tasks="1"/>'
        )

        self.gmp.get_target(target_id="t1", tasks=False)

        self.connection.send.has_been_called_with(
            b'<get_targets target_id="t1" tasks="0"/>'
        )
