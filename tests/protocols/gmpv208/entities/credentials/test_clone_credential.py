# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneCredentialTestMixin:
    def test_clone(self):
        self.gmp.clone_credential("a1")

        self.connection.send.has_been_called_with(
            b"<create_credential><copy>a1</copy></create_credential>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_credential("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_credential(None)
