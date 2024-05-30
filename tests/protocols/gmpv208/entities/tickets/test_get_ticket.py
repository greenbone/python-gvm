# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetTicketTestMixin:
    def test_get_ticket(self):
        self.gmp.get_ticket("t1")

        self.connection.send.has_been_called_with(
            b'<get_tickets ticket_id="t1"/>'
        )

        self.gmp.get_ticket(ticket_id="t1")

        self.connection.send.has_been_called_with(
            b'<get_tickets ticket_id="t1"/>'
        )

    def test_get_ticket_missing_user_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_ticket(ticket_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_ticket("")
