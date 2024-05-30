# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetPortListTestMixin:
    def test_get_port_list(self):
        self.gmp.get_port_list(port_list_id="port_list_id")

        self.connection.send.has_been_called_with(
            b'<get_port_lists port_list_id="port_list_id" details="1"/>'
        )

    def test_get_port_list_missing_port_list_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_port_list(port_list_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_port_list(port_list_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_port_list("")
