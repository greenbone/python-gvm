# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetRoleTestMixin:
    def test_get_role(self):
        self.gmp.get_role("r1")

        self.connection.send.has_been_called_with(b'<get_roles role_id="r1"/>')

        self.gmp.get_role(role_id="r1")

        self.connection.send.has_been_called_with(b'<get_roles role_id="r1"/>')

    def test_get_role_missing_role_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_role(role_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_role("")
