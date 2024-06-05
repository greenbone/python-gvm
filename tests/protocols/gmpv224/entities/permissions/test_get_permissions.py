# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetPermissionsTestMixin:
    def test_get_permissions(self):
        self.gmp.get_permissions()

        self.connection.send.has_been_called_with(b"<get_permissions/>")

    def test_get_permissions_with_filter_string(self):
        self.gmp.get_permissions(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_permissions filter="foo=bar"/>'
        )

    def test_get_permissions_with_filter_id(self):
        self.gmp.get_permissions(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_permissions filt_id="f1"/>'
        )

    def test_get_permissions_with_trash(self):
        self.gmp.get_permissions(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_permissions trash="1"/>'
        )

        self.gmp.get_permissions(trash=False)

        self.connection.send.has_been_called_with(
            b'<get_permissions trash="0"/>'
        )
