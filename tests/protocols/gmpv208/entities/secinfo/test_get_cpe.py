# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetCpeTestMixin:
    def test_get_cpe(self):
        self.gmp.get_cpe(cpe_id="i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="CPE" details="1"/>'
        )

        self.gmp.get_cpe("i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="CPE" details="1"/>'
        )

    def test_get_cpe_missing_cpe_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_cpe(cpe_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_cpe("")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_cpe(cpe_id=None)
