# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from decimal import Decimal

from gvm.errors import InvalidArgument, RequiredArgument


class GmpModifyNoteTestMixin:
    def test_modify_note(self):
        self.gmp.modify_note(note_id="n1", text="foo")

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1"><text>foo</text></modify_note>'
        )

    def test_modify_note_missing_note_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note(note_id=None, text="foo")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note(note_id="", text="foo")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note("", text="foo")

    def test_modify_note_missing_text(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note(note_id="n1", text="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note(note_id="n1", text=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_note("n1", "")

    def test_modify_note_with_days_active(self):
        self.gmp.modify_note(note_id="n1", text="foo", days_active=0)

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<active>0</active>"
            b"</modify_note>"
        )

        self.gmp.modify_note(note_id="n1", text="foo", days_active=-1)

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<active>-1</active>"
            b"</modify_note>"
        )

        self.gmp.modify_note(note_id="n1", text="foo", days_active=600)

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<active>600</active>"
            b"</modify_note>"
        )

    def test_modify_note_with_port(self):
        self.gmp.modify_note(note_id="n1", text="foo", port="123/tcp")

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<port>123/tcp</port>"
            b"</modify_note>"
        )

    def test_modify_note_with_hosts(self):
        self.gmp.modify_note(note_id="n1", text="foo", hosts=["foo"])

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<hosts>foo</hosts>"
            b"</modify_note>"
        )

        self.gmp.modify_note(note_id="n1", text="foo", hosts=["foo", "bar"])

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<hosts>foo,bar</hosts>"
            b"</modify_note>"
        )

    def test_modify_note_with_result_id(self):
        self.gmp.modify_note(note_id="n1", text="foo", result_id="r1")

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b'<result id="r1"/>'
            b"</modify_note>"
        )

    def test_modify_note_with_task_id(self):
        self.gmp.modify_note(note_id="n1", text="foo", task_id="r1")

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b'<task id="r1"/>'
            b"</modify_note>"
        )

    def test_modify_note_with_severity(self):
        self.gmp.modify_note(note_id="n1", text="foo", severity="5.5")

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_note>"
        )

        self.gmp.modify_note(note_id="n1", text="foo", severity=5.5)

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_note>"
        )

        self.gmp.modify_note(note_id="n1", text="foo", severity=Decimal(5.5))

        self.connection.send.has_been_called_with(
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_note>"
        )

    def test_modify_note_with_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_note(note_id="o1", text="foo", port="123")

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_note(note_id="o1", text="foo", port="tcp/123")
