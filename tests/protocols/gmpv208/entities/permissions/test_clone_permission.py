# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpClonePermissionTestMixin:
    def test_clone(self):
        self.gmp.clone_permission("a1")

        self.connection.send.has_been_called_with(
            b"<create_permission><copy>a1</copy></create_permission>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_permission("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_permission(None)
