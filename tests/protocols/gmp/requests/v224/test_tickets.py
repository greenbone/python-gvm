# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import Tickets, TicketStatus


class TicketsTestCase(unittest.TestCase):
    def test_clone_ticket(self):
        request = Tickets.clone_ticket("ticket_id")
        self.assertEqual(
            bytes(request),
            b"<create_ticket><copy>ticket_id</copy></create_ticket>",
        )

    def test_clone_ticket_missing_ticket_id(self):
        with self.assertRaises(RequiredArgument):
            Tickets.clone_ticket(None)

        with self.assertRaises(RequiredArgument):
            Tickets.clone_ticket("")

    def test_create_ticket(self):
        request = Tickets.create_ticket(
            result_id="result_id",
            assigned_to_user_id="user_id",
            note="note",
        )
        self.assertEqual(
            bytes(request),
            b"<create_ticket>"
            b'<result id="result_id"/>'
            b'<assigned_to><user id="user_id"/></assigned_to>'
            b"<open_note>note</open_note>"
            b"</create_ticket>",
        )

    def test_create_ticket_with_comment(self):
        request = Tickets.create_ticket(
            result_id="result_id",
            assigned_to_user_id="user_id",
            note="note",
            comment="comment",
        )
        self.assertEqual(
            bytes(request),
            b"<create_ticket>"
            b'<result id="result_id"/>'
            b'<assigned_to><user id="user_id"/></assigned_to>'
            b"<open_note>note</open_note>"
            b"<comment>comment</comment>"
            b"</create_ticket>",
        )

    def test_create_ticket_missing_result_id(self):
        with self.assertRaises(RequiredArgument):
            Tickets.create_ticket(
                result_id=None, assigned_to_user_id="user_id", note="note"
            )
        with self.assertRaises(RequiredArgument):
            Tickets.create_ticket(
                result_id="", assigned_to_user_id="user_id", note="note"
            )

    def test_create_ticket_missing_assigned_to_user_id(self):
        with self.assertRaises(RequiredArgument):
            Tickets.create_ticket(
                result_id="result_id", assigned_to_user_id=None, note="note"
            )
        with self.assertRaises(RequiredArgument):
            Tickets.create_ticket(
                result_id="result_id", assigned_to_user_id="", note="note"
            )

    def test_create_ticket_missing_note(self):
        with self.assertRaises(RequiredArgument):
            Tickets.create_ticket(
                result_id="result_id", assigned_to_user_id="user_id", note=None
            )

        with self.assertRaises(RequiredArgument):
            Tickets.create_ticket(
                result_id="result_id", assigned_to_user_id="user_id", note=""
            )

    def test_delete_ticket(self):
        request = Tickets.delete_ticket("ticket_id")
        self.assertEqual(
            bytes(request),
            b'<delete_ticket ticket_id="ticket_id" ultimate="0"/>',
        )

    def test_delete_ticket_with_ultimate(self):
        request = Tickets.delete_ticket("ticket_id", ultimate=True)
        self.assertEqual(
            bytes(request),
            b'<delete_ticket ticket_id="ticket_id" ultimate="1"/>',
        )

        request = Tickets.delete_ticket("ticket_id", ultimate=False)
        self.assertEqual(
            bytes(request),
            b'<delete_ticket ticket_id="ticket_id" ultimate="0"/>',
        )

    def test_delete_ticket_missing_ticket_id(self):
        with self.assertRaises(RequiredArgument):
            Tickets.delete_ticket(None)

        with self.assertRaises(RequiredArgument):
            Tickets.delete_ticket("")

    def test_get_tickets(self):
        request = Tickets.get_tickets()
        self.assertEqual(
            bytes(request),
            b"<get_tickets/>",
        )

    def test_get_tickets_with_filter_string(self):
        request = Tickets.get_tickets(filter_string="filter")
        self.assertEqual(
            bytes(request),
            b'<get_tickets filter="filter"/>',
        )

    def test_get_tickets_with_filter_id(self):
        request = Tickets.get_tickets(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_tickets filt_id="filter_id"/>',
        )

    def test_get_tickets_with_trash(self):
        request = Tickets.get_tickets(trash=True)
        self.assertEqual(
            bytes(request),
            b'<get_tickets trash="1"/>',
        )

        request = Tickets.get_tickets(trash=False)
        self.assertEqual(
            bytes(request),
            b'<get_tickets trash="0"/>',
        )

    def test_get_ticket(self):
        request = Tickets.get_ticket("ticket_id")
        self.assertEqual(
            bytes(request),
            b'<get_tickets ticket_id="ticket_id"/>',
        )

    def test_get_ticket_missing_ticket_id(self):
        with self.assertRaises(RequiredArgument):
            Tickets.get_ticket(None)

        with self.assertRaises(RequiredArgument):
            Tickets.get_ticket("")

    def test_modify_ticket(self):
        request = Tickets.modify_ticket("ticket_id")
        self.assertEqual(
            bytes(request),
            b'<modify_ticket ticket_id="ticket_id"/>',
        )

    def test_modify_ticket_with_status_and_note(self):
        request = Tickets.modify_ticket(
            "ticket_id", status=TicketStatus.FIXED, note="note"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_ticket ticket_id="ticket_id">'
            b"<status>Fixed</status>"
            b"<fixed_note>note</fixed_note>"
            b"</modify_ticket>",
        )

        request = Tickets.modify_ticket(
            "ticket_id", status="fixed", note="note"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_ticket ticket_id="ticket_id">'
            b"<status>Fixed</status>"
            b"<fixed_note>note</fixed_note>"
            b"</modify_ticket>",
        )

    def test_modify_ticket_with_assigned_to_user_id(self):
        request = Tickets.modify_ticket(
            "ticket_id", assigned_to_user_id="user_id"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_ticket ticket_id="ticket_id">'
            b'<assigned_to><user id="user_id"/></assigned_to>'
            b"</modify_ticket>",
        )

    def test_modify_ticket_with_comment(self):
        request = Tickets.modify_ticket("ticket_id", comment="comment")
        self.assertEqual(
            bytes(request),
            b'<modify_ticket ticket_id="ticket_id">'
            b"<comment>comment</comment>"
            b"</modify_ticket>",
        )

    def test_modify_ticket_missing_ticket_id(self):
        with self.assertRaises(RequiredArgument):
            Tickets.modify_ticket(None)

        with self.assertRaises(RequiredArgument):
            Tickets.modify_ticket("")

    def test_modify_ticket_with_status_missing_note(self):
        with self.assertRaises(RequiredArgument):
            Tickets.modify_ticket("ticket_id", status=TicketStatus.FIXED)

        with self.assertRaises(RequiredArgument):
            Tickets.modify_ticket(
                "ticket_id", status=TicketStatus.FIXED, note=None
            )

        with self.assertRaises(RequiredArgument):
            Tickets.modify_ticket(
                "ticket_id", status=TicketStatus.FIXED, note=""
            )

    def test_modify_ticket_with_note_missing_status(self):
        with self.assertRaises(RequiredArgument):
            Tickets.modify_ticket("ticket_id", note="note")

        with self.assertRaises(RequiredArgument):
            Tickets.modify_ticket("ticket_id", note="note", status=None)

        with self.assertRaises(RequiredArgument):
            Tickets.modify_ticket("ticket_id", note="note", status="")

    def test_modify_ticket_invalid_status(self):
        with self.assertRaises(InvalidArgument):
            Tickets.modify_ticket("ticket_id", note="note", status="invalid")
