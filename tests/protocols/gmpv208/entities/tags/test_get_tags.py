# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetTagsTestMixin:
    def test_get_tags(self):
        self.gmp.get_tags()

        self.connection.send.has_been_called_with(b"<get_tags/>")

    def test_get_tags_with_filter_string(self):
        self.gmp.get_tags(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_tags filter="foo=bar"/>'
        )

    def test_get_tags_with_filter_id(self):
        self.gmp.get_tags(filter_id="f1")

        self.connection.send.has_been_called_with(b'<get_tags filt_id="f1"/>')

    def test_get_tags_with_trash(self):
        self.gmp.get_tags(trash=True)

        self.connection.send.has_been_called_with(b'<get_tags trash="1"/>')

        self.gmp.get_tags(trash=False)

        self.connection.send.has_been_called_with(b'<get_tags trash="0"/>')

    def test_get_tags_with_names_only(self):
        self.gmp.get_tags(names_only=True)

        self.connection.send.has_been_called_with(b'<get_tags names_only="1"/>')

        self.gmp.get_tags(names_only=False)

        self.connection.send.has_been_called_with(b'<get_tags names_only="0"/>')
