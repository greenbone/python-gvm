# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetNvtTestMixin:
    def test_get_nvt(self):
        self.gmp.get_nvt(nvt_id="i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="NVT" details="1"/>'
        )

        self.gmp.get_nvt("i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="NVT" details="1"/>'
        )

    def test_get_nvt_missing_nvt_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_nvt(nvt_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_nvt("")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_nvt(nvt_id=None)

    def test_get_extended_nvt_with_nvt_oid(self):
        self.gmp.get_nvt(extended=True, nvt_id="nvt_oid")

        self.connection.send.has_been_called_with(
            b'<get_nvts nvt_oid="nvt_oid" details="1" '
            b'preferences="1" preference_count="1"/>'
        )

    def test_get_extended_nvt_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_nvt(extended=True, nvt_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_nvt(extended=True, nvt_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_nvt("", extended=True)
