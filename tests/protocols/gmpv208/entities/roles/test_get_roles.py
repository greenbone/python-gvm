# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetRolesTestMixin:
    def test_get_roles(self):
        self.gmp.get_roles()

        self.connection.send.has_been_called_with(b"<get_roles/>")

    def test_get_roles_with_filter_string(self):
        self.gmp.get_roles(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_roles filter="foo=bar"/>'
        )

    def test_get_roles_with_filter_id(self):
        self.gmp.get_roles(filter_id="f1")

        self.connection.send.has_been_called_with(b'<get_roles filt_id="f1"/>')

    def test_get_roles_with_trash(self):
        self.gmp.get_roles(trash=True)

        self.connection.send.has_been_called_with(b'<get_roles trash="1"/>')

        self.gmp.get_roles(trash=False)

        self.connection.send.has_been_called_with(b'<get_roles trash="0"/>')
