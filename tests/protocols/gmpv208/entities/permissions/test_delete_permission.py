# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpDeletePermissionTestMixin:
    def test_delete(self):
        self.gmp.delete_permission("a1")

        self.connection.send.has_been_called_with(
            '<delete_permission permission_id="a1" ultimate="0"/>'
        )

    def test_delete_ultimate(self):
        self.gmp.delete_permission("a1", ultimate=True)

        self.connection.send.has_been_called_with(
            '<delete_permission permission_id="a1" ultimate="1"/>'
        )

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_permission(None)

        with self.assertRaises(GvmError):
            self.gmp.delete_permission("")
