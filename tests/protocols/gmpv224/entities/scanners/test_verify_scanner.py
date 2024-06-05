# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpVerifyScannerTestMixin:
    def test_verify(self):
        self.gmp.verify_scanner("a1")

        self.connection.send.has_been_called_with(
            b'<verify_scanner scanner_id="a1"/>'
        )

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.verify_scanner(None)

        with self.assertRaises(GvmError):
            self.gmp.verify_scanner("")
