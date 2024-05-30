# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpDeleteHostTestMixin:
    def test_delete_host(self):
        self.gmp.delete_host(host_id="a1")

        self.connection.send.has_been_called_with(
            b'<delete_asset asset_id="a1"/>'
        )

    def test_missing_arguments(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_host(None)
