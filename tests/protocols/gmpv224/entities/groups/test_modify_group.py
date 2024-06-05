# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyGroupTestMixin:
    def test_modify_group(self):
        self.gmp.modify_group(group_id="f1")

        self.connection.send.has_been_called_with(
            b'<modify_group group_id="f1"/>'
        )

    def test_modify_group_missing_group_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_group(group_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_group(group_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_group("")

    def test_modify_group_with_comment(self):
        self.gmp.modify_group(group_id="f1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_group group_id="f1">'
            b"<comment>foo</comment>"
            b"</modify_group>"
        )

    def test_modify_group_with_name(self):
        self.gmp.modify_group(group_id="f1", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_group group_id="f1"><name>foo</name></modify_group>'
        )

    def test_modify_group_with_users(self):
        self.gmp.modify_group(group_id="f1", users=["foo"])

        self.connection.send.has_been_called_with(
            b'<modify_group group_id="f1">'
            b"<users>foo</users>"
            b"</modify_group>"
        )

        self.gmp.modify_group(group_id="f1", users=["foo", "bar"])

        self.connection.send.has_been_called_with(
            b'<modify_group group_id="f1">'
            b"<users>foo,bar</users>"
            b"</modify_group>"
        )
