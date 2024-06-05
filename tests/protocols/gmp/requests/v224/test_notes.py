# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from decimal import Decimal

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import Notes


class NotesTestCase(unittest.TestCase):
    def test_create_note(self):
        request = Notes.create_note("foo", nvt_oid="oid1")

        self.assertEqual(
            bytes(request),
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"</create_note>",
        )

    def test_create_note_missing_text(self):
        with self.assertRaises(RequiredArgument):
            Notes.create_note(None, "od1")

        with self.assertRaises(RequiredArgument):
            Notes.create_note("", "oid1")

    def test_create_note_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            Notes.create_note("foo", None)

        with self.assertRaises(RequiredArgument):
            Notes.create_note("foo", "")

    def test_create_note_with_hosts(self):
        request = Notes.create_note("foo", nvt_oid="oid1", hosts=[])

        self.assertEqual(
            bytes(request),
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"</create_note>",
        )

        request = Notes.create_note("foo", nvt_oid="oid1", hosts=["h1", "h2"])

        self.assertEqual(
            bytes(request),
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<hosts>h1,h2</hosts>"
            b"</create_note>",
        )

    def test_create_note_with_port(self):
        request = Notes.create_note("foo", nvt_oid="oid1", port="666/tcp")

        self.assertEqual(
            bytes(request),
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<port>666/tcp</port>"
            b"</create_note>",
        )

    def test_create_note_with_result_id(self):
        request = Notes.create_note("foo", nvt_oid="oid1", result_id="r1")

        self.assertEqual(
            bytes(request),
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b'<result id="r1"/>'
            b"</create_note>",
        )

    def test_create_note_with_task_id(self):
        request = Notes.create_note("foo", nvt_oid="oid1", task_id="t1")

        self.assertEqual(
            bytes(request),
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b'<task id="t1"/>'
            b"</create_note>",
        )

    def test_create_note_with_severity(self):
        request = Notes.create_note("foo", nvt_oid="oid1", severity="5.5")

        self.assertEqual(
            bytes(request),
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<severity>5.5</severity>"
            b"</create_note>",
        )

    def test_create_note_with_days_active(self):
        request = Notes.create_note("foo", nvt_oid="oid1", days_active=5)

        self.assertEqual(
            bytes(request),
            b"<create_note>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<active>5</active>"
            b"</create_note>",
        )

    def test_create_note_with_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            Notes.create_note("foo", nvt_oid="oid1", port="666")

        with self.assertRaises(InvalidArgument):
            Notes.create_note("foo", nvt_oid="oid1", port="666/")

        with self.assertRaises(InvalidArgument):
            Notes.create_note("foo", nvt_oid="oid1", port="udp/666")

    def test_modify_note(self):
        request = Notes.modify_note("n1", "foo")

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1"><text>foo</text></modify_note>',
        )

    def test_modify_note_missing_note_id(self):
        with self.assertRaises(RequiredArgument):
            Notes.modify_note(None, "foo")

        with self.assertRaises(RequiredArgument):
            Notes.modify_note("", "foo")

    def test_modify_note_missing_text(self):
        with self.assertRaises(RequiredArgument):
            Notes.modify_note("n1", None)

        with self.assertRaises(RequiredArgument):
            Notes.modify_note("n1", "")

    def test_modify_note_with_days_active(self):
        request = Notes.modify_note("n1", "foo", days_active=0)

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<active>0</active>"
            b"</modify_note>",
        )

        request = Notes.modify_note("n1", "foo", days_active=-1)

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<active>-1</active>"
            b"</modify_note>",
        )

        request = Notes.modify_note("n1", "foo", days_active=600)

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<active>600</active>"
            b"</modify_note>",
        )

    def test_modify_note_with_port(self):
        request = Notes.modify_note("n1", "foo", port="123/tcp")

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<port>123/tcp</port>"
            b"</modify_note>",
        )

    def test_modify_note_with_hosts(self):
        request = Notes.modify_note("n1", "foo", hosts=["h1"])

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<hosts>h1</hosts>"
            b"</modify_note>",
        )

        request = Notes.modify_note("n1", "foo", hosts=["h1", "h2"])

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<hosts>h1,h2</hosts>"
            b"</modify_note>",
        )

    def test_modify_note_with_result_id(self):
        request = Notes.modify_note("n1", "foo", result_id="r1")

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b'<result id="r1"/>'
            b"</modify_note>",
        )

    def test_modify_note_with_task_id(self):
        request = Notes.modify_note("n1", "foo", task_id="t1")

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b'<task id="t1"/>'
            b"</modify_note>",
        )

    def test_modify_note_with_severity(self):
        request = Notes.modify_note("n1", "foo", severity="5.5")

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_note>",
        )

        request = Notes.modify_note("n1", "foo", severity=5.5)

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_note>",
        )

        request = Notes.modify_note("n1", "foo", severity=Decimal(5.5))

        self.assertEqual(
            bytes(request),
            b'<modify_note note_id="n1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_note>",
        )

    def test_modify_note_with_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            Notes.modify_note("n1", "foo", port="666")

        with self.assertRaises(InvalidArgument):
            Notes.modify_note("n1", "foo", port="666/")

        with self.assertRaises(InvalidArgument):
            Notes.modify_note("n1", "foo", port="udp/666")

    def test_clone_note(self):
        request = Notes.clone_note("n1")

        self.assertEqual(
            bytes(request),
            b"<create_note><copy>n1</copy></create_note>",
        )

    def test_clone_note_missing_note_id(self):
        with self.assertRaises(RequiredArgument):
            Notes.clone_note(None)

        with self.assertRaises(RequiredArgument):
            Notes.clone_note("")

    def test_delete_note(self):
        request = Notes.delete_note("n1")

        self.assertEqual(
            bytes(request), b'<delete_note note_id="n1" ultimate="0"/>'
        )

    def test_delete_note_ultimate(self):
        request = Notes.delete_note("n1", ultimate=True)

        self.assertEqual(
            bytes(request), b'<delete_note note_id="n1" ultimate="1"/>'
        )

        request = Notes.delete_note("n1", ultimate=False)

        self.assertEqual(
            bytes(request), b'<delete_note note_id="n1" ultimate="0"/>'
        )

    def test_delete_note_missing_note_id(self):
        with self.assertRaises(RequiredArgument):
            Notes.delete_note(None)

        with self.assertRaises(RequiredArgument):
            Notes.delete_note("")

    def test_get_notes(self):
        request = Notes.get_notes()

        self.assertEqual(bytes(request), b"<get_notes/>")

    def test_get_notes_with_filter_string(self):
        request = Notes.get_notes(filter_string="foo=bar")

        self.assertEqual(bytes(request), b'<get_notes filter="foo=bar"/>')

    def test_get_notes_with_filter_id(self):
        request = Notes.get_notes(filter_id="f1")

        self.assertEqual(bytes(request), b'<get_notes filt_id="f1"/>')

    def test_get_notes_with_details(self):
        request = Notes.get_notes(details=True)

        self.assertEqual(bytes(request), b'<get_notes details="1"/>')

        request = Notes.get_notes(details=False)

        self.assertEqual(bytes(request), b'<get_notes details="0"/>')

    def test_get_notes_with_result(self):
        request = Notes.get_notes(result=True)

        self.assertEqual(bytes(request), b'<get_notes result="1"/>')

        request = Notes.get_notes(result=False)

        self.assertEqual(bytes(request), b'<get_notes result="0"/>')

    def test_get_note(self):
        request = Notes.get_note("n1")

        self.assertEqual(
            bytes(request), b'<get_notes note_id="n1" details="1"/>'
        )

    def test_get_note_missing_note_id(self):
        with self.assertRaises(RequiredArgument):
            Notes.get_note(None)

        with self.assertRaises(RequiredArgument):
            Notes.get_note("")
