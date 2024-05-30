# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetTicketsTestMixin:
    def test_get_tickets(self):
        self.gmp.get_tickets()

        self.connection.send.has_been_called_with(b"<get_tickets/>")

    def test_get_tickets_with_filter_string(self):
        self.gmp.get_tickets(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_tickets filter="foo=bar"/>'
        )

    def test_get_tickets_with_filter_id(self):
        self.gmp.get_tickets(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_tickets filt_id="f1"/>'
        )

    def test_get_tickets_with_trash(self):
        self.gmp.get_tickets(trash=True)

        self.connection.send.has_been_called_with(b'<get_tickets trash="1"/>')

        self.gmp.get_tickets(trash=False)

        self.connection.send.has_been_called_with(b'<get_tickets trash="0"/>')
