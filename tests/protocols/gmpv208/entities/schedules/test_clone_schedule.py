# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneScheduleTestMixin:
    def test_clone(self):
        self.gmp.clone_schedule("a1")

        self.connection.send.has_been_called_with(
            b"<create_schedule><copy>a1</copy></create_schedule>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_schedule("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_schedule(None)
