# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneTicketTestMixin:
    def test_clone(self):
        self.gmp.clone_ticket("t1")

        self.connection.send.has_been_called_with(
            b"<create_ticket><copy>t1</copy></create_ticket>"
        )

        self.gmp.clone_ticket(ticket_id="t1")

        self.connection.send.has_been_called_with(
            b"<create_ticket><copy>t1</copy></create_ticket>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_ticket("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_ticket(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_ticket(ticket_id=None)
