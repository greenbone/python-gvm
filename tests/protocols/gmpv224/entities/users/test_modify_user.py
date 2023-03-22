# -*- coding: utf-8 -*-
# Copyright (C) 2018-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from unittest.mock import call, patch

from gvm.errors import RequiredArgument
from gvm.protocols.gmpv224 import UserAuthType


class GmpModifyUserTestMixin:
    def test_modify_user(self):
        self.gmp.modify_user(user_id="u1")

        self.connection.send.has_been_called_with('<modify_user user_id="u1"/>')

    def test_modify_user_missing_user_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_user(user_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_user(user_id="")

    def test_modify_user_with_new_name(self):
        self.gmp.modify_user(user_id="u1", name="foo")

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1">'
            "<new_name>foo</new_name>"
            "</modify_user>"
        )

    def test_modify_user_with_new_comment(self):
        self.gmp.modify_user(user_id="u1", comment="foo")

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1">'
            "<comment>foo</comment>"
            "</modify_user>"
        )

    def test_modify_user_with_role_ids(self):
        self.gmp.modify_user(user_id="u1", role_ids=[])

        self.connection.send.has_been_called_with('<modify_user user_id="u1"/>')

        self.gmp.modify_user(user_id="u1", role_ids=["r1"])

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1"><role id="r1"/></modify_user>'
        )

        self.gmp.modify_user(user_id="u1", role_ids=["r1", "r2"])

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1">'
            '<role id="r1"/>'
            '<role id="r2"/>'
            "</modify_user>"
        )

    def test_modify_user_with_group_ids(self):
        self.gmp.modify_user(user_id="u1", role_ids=[])

        self.connection.send.has_been_called_with('<modify_user user_id="u1"/>')

        self.gmp.modify_user(user_id="u1", group_ids=["r1"])

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1">'
            '<groups><group id="r1"/></groups>'
            "</modify_user>"
        )

        self.gmp.modify_user(user_id="u1", group_ids=["r1", "r2"])

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1">'
            "<groups>"
            '<group id="r1"/>'
            '<group id="r2"/>'
            "</groups>"
            "</modify_user>"
        )

    def test_modify_user_with_password(self):
        self.gmp.modify_user(user_id="u1", password="foo")

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1">'
            "<password>foo</password>"
            "</modify_user>"
        )

    def test_modify_user_with_auth_source(self):
        self.gmp.modify_user(
            user_id="u1", auth_source=UserAuthType.LDAP_CONNECT
        )

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1">'
            "<sources><source>ldap_connect</source></sources>"
            "</modify_user>"
        )

    def test_modify_user_with_hosts(self):
        self.gmp.modify_user(user_id="u1", hosts=[])

        self.connection.send.has_been_called_with('<modify_user user_id="u1"/>')

        self.gmp.modify_user(user_id="u1", hosts=["foo"])

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1">'
            '<hosts allow="0">foo</hosts>'
            "</modify_user>"
        )

        self.gmp.modify_user(user_id="u1", hosts=["foo", "bar"])

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1">'
            '<hosts allow="0">foo,bar</hosts>'
            "</modify_user>"
        )

        self.gmp.modify_user(
            user_id="u1", hosts=["foo", "bar"], hosts_allow=False
        )

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1">'
            '<hosts allow="0">foo,bar</hosts>'
            "</modify_user>"
        )

        self.gmp.modify_user(
            user_id="u1", hosts=["foo", "bar"], hosts_allow=True
        )

        self.connection.send.has_been_called_with(
            '<modify_user user_id="u1">'
            '<hosts allow="1">foo,bar</hosts>'
            "</modify_user>"
        )

    @patch("gvm.protocols.gmpv224.entities.users.deprecation")
    def test_modify_user_with_ifaces(self, deprecation_mock):
        self.gmp.modify_user(user_id="u1", ifaces=[])

        self.connection.send.has_been_called_with('<modify_user user_id="u1"/>')

        self.gmp.modify_user(user_id="u2", ifaces=["foo"])

        self.connection.send.has_been_called_with('<modify_user user_id="u2"/>')

        self.gmp.modify_user(user_id="u3", ifaces=["foo", "bar"])

        self.connection.send.has_been_called_with('<modify_user user_id="u3"/>')

        self.gmp.modify_user(
            user_id="u4", ifaces=["foo", "bar"], ifaces_allow=False
        )

        self.connection.send.has_been_called_with('<modify_user user_id="u4"/>')

        self.gmp.modify_user(
            user_id="u5", ifaces=["foo", "bar"], ifaces_allow=True
        )

        self.connection.send.has_been_called_with('<modify_user user_id="u5"/>')

        # pylint: disable=line-too-long
        deprecation_calls = [
            call("The ifaces parameter has been removed in GMP version 224"),
            call("The ifaces parameter has been removed in GMP version 224"),
            call("The ifaces parameter has been removed in GMP version 224"),
            call(
                "The ifaces_allow parameter has been removed in GMP version 224"
            ),
            call("The ifaces parameter has been removed in GMP version 224"),
            call(
                "The ifaces_allow parameter has been removed in GMP version 224"
            ),
        ]
        # pylint: enable=line-too-long
        deprecation_mock.assert_has_calls(deprecation_calls)
