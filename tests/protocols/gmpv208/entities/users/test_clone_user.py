# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneUserTestMixin:
    def test_clone(self):
        self.gmp.clone_user("a1")

        self.connection.send.has_been_called_with(
            b"<create_user><copy>a1</copy></create_user>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_user("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_user(None)
