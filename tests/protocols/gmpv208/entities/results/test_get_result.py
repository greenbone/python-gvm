# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetResultTestMixin:
    def test_get_result(self):
        self.gmp.get_result("r1")

        self.connection.send.has_been_called_with(
            b'<get_results result_id="r1" details="1"/>'
        )

        self.gmp.get_result(result_id="r1")

        self.connection.send.has_been_called_with(
            b'<get_results result_id="r1" details="1"/>'
        )

    def test_get_result_missing_result_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_result(result_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_result("")
