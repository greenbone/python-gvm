# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetGroupsTestMixin:
    def test_get_groups(self):
        self.gmp.get_groups()

        self.connection.send.has_been_called_with(b"<get_groups/>")

    def test_get_groups_with_filter_string(self):
        self.gmp.get_groups(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_groups filter="foo=bar"/>'
        )

    def test_get_groups_with_filter_id(self):
        self.gmp.get_groups(filter_id="f1")

        self.connection.send.has_been_called_with(b'<get_groups filt_id="f1"/>')

    def test_get_groups_with_trash(self):
        self.gmp.get_groups(trash=True)

        self.connection.send.has_been_called_with(b'<get_groups trash="1"/>')

        self.gmp.get_groups(trash=False)

        self.connection.send.has_been_called_with(b'<get_groups trash="0"/>')
