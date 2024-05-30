# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetScannerTestMixin:
    def test_get_scanner(self):
        self.gmp.get_scanner("s1")

        self.connection.send.has_been_called_with(
            b'<get_scanners scanner_id="s1" details="1"/>'
        )

        self.gmp.get_scanner(scanner_id="s1")

        self.connection.send.has_been_called_with(
            b'<get_scanners scanner_id="s1" details="1"/>'
        )

    def test_get_scanner_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_scanner(scanner_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_scanner("")
