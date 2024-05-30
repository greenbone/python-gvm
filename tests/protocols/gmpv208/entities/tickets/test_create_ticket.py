# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateTicketTestMixin:
    def test_create_ticket(self):
        self.gmp.create_ticket(
            result_id="r1", assigned_to_user_id="u1", note="lorem ipsum"
        )

        self.connection.send.has_been_called_with(
            b"<create_ticket>"
            b'<result id="r1"/>'
            b"<assigned_to>"
            b'<user id="u1"/>'
            b"</assigned_to>"
            b"<open_note>lorem ipsum</open_note>"
            b"</create_ticket>"
        )

    def test_create_ticket_with_comment(self):
        self.gmp.create_ticket(
            result_id="r1",
            assigned_to_user_id="u1",
            note="lorem ipsum",
            comment="bar",
        )

        self.connection.send.has_been_called_with(
            b"<create_ticket>"
            b'<result id="r1"/>'
            b"<assigned_to>"
            b'<user id="u1"/>'
            b"</assigned_to>"
            b"<open_note>lorem ipsum</open_note>"
            b"<comment>bar</comment>"
            b"</create_ticket>"
        )

    def test_create_ticket_missing_result_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_ticket(
                result_id="", assigned_to_user_id="u1", note="lorem ipsum"
            )

    def test_create_ticket_missing_assigned_to_user_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_ticket(
                result_id="r1", assigned_to_user_id="", note="lorem ipsum"
            )

    def test_create_ticket_missing_open_note(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_ticket(
                result_id="r1", assigned_to_user_id="u1", note=""
            )
