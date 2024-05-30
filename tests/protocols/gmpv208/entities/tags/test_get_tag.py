# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetTagTestMixin:
    def test_get_tag(self):
        self.gmp.get_tag("t1")

        self.connection.send.has_been_called_with(b'<get_tags tag_id="t1"/>')

        self.gmp.get_tag(tag_id="t1")

        self.connection.send.has_been_called_with(b'<get_tags tag_id="t1"/>')

    def test_get_tag_missing_tag_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_tag(tag_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_tag("")
