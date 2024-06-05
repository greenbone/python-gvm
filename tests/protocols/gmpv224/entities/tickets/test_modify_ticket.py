# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import TicketStatus


class GmpModifyTicketTestMixin:
    def test_modify_ticket(self):
        self.gmp.modify_ticket("t1")

        self.connection.send.has_been_called_with(
            b'<modify_ticket ticket_id="t1"/>'
        )

        self.gmp.modify_ticket(ticket_id="t1")

        self.connection.send.has_been_called_with(
            b'<modify_ticket ticket_id="t1"/>'
        )

    def test_missing_ticket_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_ticket("")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_ticket(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_ticket(ticket_id=None)

    def test_modify_ticket_with_comment(self):
        self.gmp.modify_ticket(ticket_id="t1", comment="bar")

        self.connection.send.has_been_called_with(
            b'<modify_ticket ticket_id="t1">'
            b"<comment>bar</comment>"
            b"</modify_ticket>"
        )

    def test_modify_ticket_with_assigned_to_user_id(self):
        self.gmp.modify_ticket(ticket_id="t1", assigned_to_user_id="u1")

        self.connection.send.has_been_called_with(
            b'<modify_ticket ticket_id="t1">'
            b"<assigned_to>"
            b'<user id="u1"/>'
            b"</assigned_to>"
            b"</modify_ticket>"
        )

    def test_modify_ticket_invalid_status(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_ticket(ticket_id="t1", status="foobar", note="bar")

    def test_modify_ticket_open(self):
        self.gmp.modify_ticket(
            ticket_id="t1", status=TicketStatus.OPEN, note="lorem ipsum"
        )

        self.connection.send.has_been_called_with(
            b'<modify_ticket ticket_id="t1">'
            b"<status>Open</status>"
            b"<open_note>lorem ipsum</open_note>"
            b"</modify_ticket>"
        )

    def test_modify_ticket_fixed(self):
        self.gmp.modify_ticket(
            ticket_id="t1", status=TicketStatus.FIXED, note="lorem ipsum"
        )

        self.connection.send.has_been_called_with(
            b'<modify_ticket ticket_id="t1">'
            b"<status>Fixed</status>"
            b"<fixed_note>lorem ipsum</fixed_note>"
            b"</modify_ticket>"
        )

    def test_modify_ticket_closed(self):
        self.gmp.modify_ticket(
            ticket_id="t1", status=TicketStatus.CLOSED, note="lorem ipsum"
        )

        self.connection.send.has_been_called_with(
            b'<modify_ticket ticket_id="t1">'
            b"<status>Closed</status>"
            b"<closed_note>lorem ipsum</closed_note>"
            b"</modify_ticket>"
        )

    def test_modify_ticket_status_without_note(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_ticket(ticket_id="t1", status=TicketStatus.CLOSED)

    def test_modify_ticket_note_without_status(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_ticket(ticket_id="t1", note="foo")
