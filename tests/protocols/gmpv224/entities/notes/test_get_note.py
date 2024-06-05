# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetNoteTestMixin:
    def test_get_note(self):
        self.gmp.get_note("n1")

        self.connection.send.has_been_called_with(
            b'<get_notes note_id="n1" details="1"/>'
        )

        self.gmp.get_note(note_id="n1")

        self.connection.send.has_been_called_with(
            b'<get_notes note_id="n1" details="1"/>'
        )

    def test_get_note_missing_note_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_note(note_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_note("")
