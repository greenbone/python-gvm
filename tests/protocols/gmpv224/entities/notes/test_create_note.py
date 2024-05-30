# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from decimal import Decimal

from gvm.errors import InvalidArgument, RequiredArgument


class GmpCreateNoteTestMixin:
    def test_create_note(self):
        self.gmp.create_note("foo", nvt_oid="oid1")

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"</create_note>"
        )

    def test_create_note_missing_text(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_note(None, "od1")

        with self.assertRaises(RequiredArgument):
            self.gmp.create_note("", "oid1")

    def test_create_note_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_note("foo", None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_note("foo", "")

    def test_create_note_with_hosts(self):
        self.gmp.create_note("foo", nvt_oid="oid1", hosts=[])

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"</create_note>"
        )

        self.gmp.create_note("foo", nvt_oid="oid1", hosts=["h1", "h2"])

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<hosts>h1,h2</hosts>"
            b"</create_note>"
        )

    def test_create_note_with_port(self):
        self.gmp.create_note("foo", nvt_oid="oid1", port="666/tcp")

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<port>666/tcp</port>"
            b"</create_note>"
        )

    def test_create_note_with_result_id(self):
        self.gmp.create_note("foo", nvt_oid="oid1", result_id="r1")

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b'<result id="r1"/>'
            b"</create_note>"
        )

    def test_create_note_with_task_id(self):
        self.gmp.create_note("foo", nvt_oid="oid1", task_id="t1")

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b'<task id="t1"/>'
            b"</create_note>"
        )

    def test_create_note_with_severity(self):
        self.gmp.create_note("foo", nvt_oid="oid1", severity="5.5")

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<severity>5.5</severity>"
            b"</create_note>"
        )

        self.gmp.create_note("foo", nvt_oid="oid1", severity=5.5)

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<severity>5.5</severity>"
            b"</create_note>"
        )

        self.gmp.create_note("foo", nvt_oid="oid1", severity=Decimal(5.5))

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<severity>5.5</severity>"
            b"</create_note>"
        )

    def test_create_note_with_days_active(self):
        self.gmp.create_note("foo", nvt_oid="oid1", days_active=0)

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<active>0</active>"
            b"</create_note>"
        )

        self.gmp.create_note("foo", nvt_oid="oid1", days_active=-1)

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<active>-1</active>"
            b"</create_note>"
        )

        self.gmp.create_note("foo", nvt_oid="oid1", days_active=3600)

        self.connection.send.has_been_called_with(
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<active>3600</active>"
            b"</create_note>"
        )

    def test_create_note_with_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_note(text="foo", nvt_oid="oid1", port="123")

        with self.assertRaises(InvalidArgument):
            self.gmp.create_note(text="foo", nvt_oid="oid1", port="tcp/123")
