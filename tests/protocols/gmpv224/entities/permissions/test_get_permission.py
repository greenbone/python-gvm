# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetPermissionTestMixin:
    def test_get_permission(self):
        self.gmp.get_permission("p1")

        self.connection.send.has_been_called_with(
            b'<get_permissions permission_id="p1"/>'
        )

        self.gmp.get_permission(permission_id="p1")

        self.connection.send.has_been_called_with(
            b'<get_permissions permission_id="p1"/>'
        )

    def test_get_permission_missing_permission_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_permission(permission_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_permission("")
