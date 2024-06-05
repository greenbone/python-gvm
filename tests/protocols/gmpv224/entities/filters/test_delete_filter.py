# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpDeleteFilterTestMixin:
    def test_delete(self):
        self.gmp.delete_filter("a1")

        self.connection.send.has_been_called_with(
            b'<delete_filter filter_id="a1" ultimate="0"/>'
        )

    def test_delete_ultimate(self):
        self.gmp.delete_filter("a1", ultimate=True)

        self.connection.send.has_been_called_with(
            b'<delete_filter filter_id="a1" ultimate="1"/>'
        )

    def test_missing_filter_id(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_filter(None)

        with self.assertRaises(GvmError):
            self.gmp.delete_filter("")
