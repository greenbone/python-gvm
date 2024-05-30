# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpRestoreFromTrashcanTestMixin:
    def test_restore_from_trashcan(self):
        self.gmp.restore_from_trashcan("a1")

        self.connection.send.has_been_called_with(b'<restore id="a1"/>')

    def test_restore_from_trashcan_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.restore_from_trashcan(None)

        with self.assertRaises(GvmError):
            self.gmp.restore_from_trashcan("")
