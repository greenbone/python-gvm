# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneScannerTestMixin:
    def test_clone(self):
        self.gmp.clone_scanner("a1")

        self.connection.send.has_been_called_with(
            b"<create_scanner><copy>a1</copy></create_scanner>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_scanner("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_scanner(None)
