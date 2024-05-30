# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpDeleteTicketTestMixin:
    def test_delete(self):
        self.gmp.delete_ticket("t1")

        self.connection.send.has_been_called_with(
            b'<delete_ticket ticket_id="t1" ultimate="0"/>'
        )

    def test_delete_ultimate(self):
        self.gmp.delete_ticket("t1", ultimate=True)

        self.connection.send.has_been_called_with(
            b'<delete_ticket ticket_id="t1" ultimate="1"/>'
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.delete_ticket(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.delete_ticket("")
