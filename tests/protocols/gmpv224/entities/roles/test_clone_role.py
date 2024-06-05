# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneRoleTestMixin:
    def test_clone(self):
        self.gmp.clone_role("a1")

        self.connection.send.has_been_called_with(
            b"<create_role><copy>a1</copy></create_role>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_role("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_role(None)
