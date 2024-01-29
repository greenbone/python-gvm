# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpDeletePolicyTestMixin:
    def test_delete(self):
        self.gmp.delete_policy("a1")

        self.connection.send.has_been_called_with(
            '<delete_config config_id="a1" ultimate="0"/>'
        )

    def test_delete_ultimate(self):
        self.gmp.delete_policy("a1", ultimate=True)

        self.connection.send.has_been_called_with(
            '<delete_config config_id="a1" ultimate="1"/>'
        )

    def test_missing_config_id(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_policy(None)

        with self.assertRaises(GvmError):
            self.gmp.delete_policy("")
