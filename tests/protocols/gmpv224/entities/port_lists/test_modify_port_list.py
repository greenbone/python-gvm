# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyPortListTestMixin:
    def test_modify_port_list(self):
        self.gmp.modify_port_list(port_list_id="p1")

        self.connection.send.has_been_called_with(
            b'<modify_port_list port_list_id="p1"/>'
        )

    def test_modify_port_list_missing_port_list_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_port_list(port_list_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_port_list(port_list_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_port_list("")

    def test_modify_port_list_with_comment(self):
        self.gmp.modify_port_list(port_list_id="p1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_port_list port_list_id="p1">'
            b"<comment>foo</comment>"
            b"</modify_port_list>"
        )

    def test_modify_port_list_with_name(self):
        self.gmp.modify_port_list(port_list_id="p1", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_port_list port_list_id="p1">'
            b"<name>foo</name>"
            b"</modify_port_list>"
        )
