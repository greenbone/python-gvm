# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetGroupTestMixin:
    def test_get_group(self):
        self.gmp.get_group("f1")

        self.connection.send.has_been_called_with(
            b'<get_groups group_id="f1"/>'
        )

        self.gmp.get_group(group_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_groups group_id="f1"/>'
        )

    def test_get_group_missing_group_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_group(group_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_group("")
