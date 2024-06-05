# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetCveTestMixin:
    def test_get_cve(self):
        self.gmp.get_cve(cve_id="i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="CVE" details="1"/>'
        )

        self.gmp.get_cve("i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="CVE" details="1"/>'
        )

    def test_get_cve_missing_cve_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_cve(cve_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_cve("")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_cve(cve_id=None)
