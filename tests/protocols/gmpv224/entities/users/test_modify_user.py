# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import UserAuthType


class GmpModifyUserTestMixin:
    def test_modify_user(self):
        self.gmp.modify_user(user_id="u1")

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1"/>'
        )

    def test_modify_user_missing_user_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_user(user_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_user(user_id="")

    def test_modify_user_with_new_name(self):
        self.gmp.modify_user(user_id="u1", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1">'
            b"<new_name>foo</new_name>"
            b"</modify_user>"
        )

    def test_modify_user_with_new_comment(self):
        self.gmp.modify_user(user_id="u1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1">'
            b"<comment>foo</comment>"
            b"</modify_user>"
        )

    def test_modify_user_with_role_ids(self):
        self.gmp.modify_user(user_id="u1", role_ids=[])

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1"/>'
        )

        self.gmp.modify_user(user_id="u1", role_ids=["r1"])

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1"><role id="r1"/></modify_user>'
        )

        self.gmp.modify_user(user_id="u1", role_ids=["r1", "r2"])

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1">'
            b'<role id="r1"/>'
            b'<role id="r2"/>'
            b"</modify_user>"
        )

    def test_modify_user_with_group_ids(self):
        self.gmp.modify_user(user_id="u1", role_ids=[])

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1"/>'
        )

        self.gmp.modify_user(user_id="u1", group_ids=["r1"])

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1">'
            b'<groups><group id="r1"/></groups>'
            b"</modify_user>"
        )

        self.gmp.modify_user(user_id="u1", group_ids=["r1", "r2"])

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1">'
            b"<groups>"
            b'<group id="r1"/>'
            b'<group id="r2"/>'
            b"</groups>"
            b"</modify_user>"
        )

    def test_modify_user_with_password(self):
        self.gmp.modify_user(user_id="u1", password="foo")

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1">'
            b"<password>foo</password>"
            b"</modify_user>"
        )

    def test_modify_user_with_auth_source(self):
        self.gmp.modify_user(
            user_id="u1", auth_source=UserAuthType.LDAP_CONNECT
        )

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1">'
            b"<sources><source>ldap_connect</source></sources>"
            b"</modify_user>"
        )

    def test_modify_user_with_hosts(self):
        self.gmp.modify_user(user_id="u1", hosts=[])

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1"/>'
        )

        self.gmp.modify_user(user_id="u1", hosts=["foo"])

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1">'
            b'<hosts allow="0">foo</hosts>'
            b"</modify_user>"
        )

        self.gmp.modify_user(user_id="u1", hosts=["foo", "bar"])

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1">'
            b'<hosts allow="0">foo,bar</hosts>'
            b"</modify_user>"
        )

        self.gmp.modify_user(
            user_id="u1", hosts=["foo", "bar"], hosts_allow=False
        )

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1">'
            b'<hosts allow="0">foo,bar</hosts>'
            b"</modify_user>"
        )

        self.gmp.modify_user(
            user_id="u1", hosts=["foo", "bar"], hosts_allow=True
        )

        self.connection.send.has_been_called_with(
            b'<modify_user user_id="u1">'
            b'<hosts allow="1">foo,bar</hosts>'
            b"</modify_user>"
        )
