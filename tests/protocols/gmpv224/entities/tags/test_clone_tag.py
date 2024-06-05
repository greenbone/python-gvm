# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneTagTestMixin:
    def test_clone(self):
        self.gmp.clone_tag("a1")

        self.connection.send.has_been_called_with(
            b"<create_tag><copy>a1</copy></create_tag>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_tag("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_tag(None)
