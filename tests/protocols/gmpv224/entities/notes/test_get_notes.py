# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetNotesTestMixin:
    def test_get_notes(self):
        self.gmp.get_notes()

        self.connection.send.has_been_called_with(b"<get_notes/>")

    def test_get_notes_with_filter_string(self):
        self.gmp.get_notes(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_notes filter="foo=bar"/>'
        )

    def test_get_notes_with_filter_id(self):
        self.gmp.get_notes(filter_id="f1")

        self.connection.send.has_been_called_with(b'<get_notes filt_id="f1"/>')

    def test_get_notes_with_details(self):
        self.gmp.get_notes(details=True)

        self.connection.send.has_been_called_with(b'<get_notes details="1"/>')

        self.gmp.get_notes(details=False)

        self.connection.send.has_been_called_with(b'<get_notes details="0"/>')

    def test_get_notes_with_result(self):
        self.gmp.get_notes(result=True)

        self.connection.send.has_been_called_with(b'<get_notes result="1"/>')

        self.gmp.get_notes(result=False)

        self.connection.send.has_been_called_with(b'<get_notes result="0"/>')
