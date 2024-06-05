# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyRoleTestMixin:
    def test_modify_role(self):
        self.gmp.modify_role(role_id="r1")

        self.connection.send.has_been_called_with(
            b'<modify_role role_id="r1"/>'
        )

    def test_modify_role_missing_role_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_role(role_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_role(role_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_role("")

    def test_modify_role_with_comment(self):
        self.gmp.modify_role(role_id="r1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_role role_id="r1">'
            b"<comment>foo</comment>"
            b"</modify_role>"
        )

    def test_modify_role_with_name(self):
        self.gmp.modify_role(role_id="r1", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_role role_id="r1"><name>foo</name></modify_role>'
        )

    def test_modify_role_with_users(self):
        self.gmp.modify_role(role_id="r1", users=[])

        self.connection.send.has_been_called_with(
            b'<modify_role role_id="r1"/>'
        )

        self.gmp.modify_role(role_id="r1", users=["foo"])

        self.connection.send.has_been_called_with(
            b'<modify_role role_id="r1"><users>foo</users></modify_role>'
        )

        self.gmp.modify_role(role_id="r1", users=["foo", "bar"])

        self.connection.send.has_been_called_with(
            b'<modify_role role_id="r1">'
            b"<users>foo,bar</users>"
            b"</modify_role>"
        )
