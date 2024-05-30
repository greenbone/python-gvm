# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetPortListsTestMixin:
    def test_get_port_lists(self):
        self.gmp.get_port_lists()

        self.connection.send.has_been_called_with(b"<get_port_lists/>")

    def test_get_port_lists_with_filter_string(self):
        self.gmp.get_port_lists(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_port_lists filter="foo=bar"/>'
        )

    def test_get_port_lists_with_filter_id(self):
        self.gmp.get_port_lists(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_port_lists filt_id="f1"/>'
        )

    def test_get_port_lists_with_trash(self):
        self.gmp.get_port_lists(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_port_lists trash="1"/>'
        )

        self.gmp.get_port_lists(trash=False)

        self.connection.send.has_been_called_with(
            b'<get_port_lists trash="0"/>'
        )

    def test_get_port_lists_with_details(self):
        self.gmp.get_port_lists(details=True)

        self.connection.send.has_been_called_with(
            b'<get_port_lists details="1"/>'
        )

        self.gmp.get_port_lists(details=False)

        self.connection.send.has_been_called_with(
            b'<get_port_lists details="0"/>'
        )

    def test_get_port_lists_with_targets(self):
        self.gmp.get_port_lists(targets=True)

        self.connection.send.has_been_called_with(
            b'<get_port_lists targets="1"/>'
        )

        self.gmp.get_port_lists(targets=False)

        self.connection.send.has_been_called_with(
            b'<get_port_lists targets="0"/>'
        )
