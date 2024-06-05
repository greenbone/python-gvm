# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpDeleteOperatingSystemTestMixin:
    def test_delete_operating_system(self):
        self.gmp.delete_operating_system(operating_system_id="a1")

        self.connection.send.has_been_called_with(
            b'<delete_asset asset_id="a1"/>'
        )

    def test_missing_arguments(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_operating_system(None)
