# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneTargetTestMixin:
    TARGET_ID = "00000000-0000-0000-0000-000000000000"

    def test_clone(self):
        self.gmp.clone_target(self.TARGET_ID)

        self.connection.send.has_been_called_with(
            "<create_target>"
            f"<copy>{self.TARGET_ID}</copy>"
            "</create_target>".encode("utf-8")
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_target("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_target(None)
