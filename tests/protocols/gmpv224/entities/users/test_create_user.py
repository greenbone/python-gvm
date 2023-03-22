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


class GmpCreateUserTestMixin:
    def test_create_user_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_user(name=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_user(name="")

    def test_create_user(self):
        self.gmp.create_user(name="foo")

        self.connection.send.has_been_called_with(
            "<create_user><name>foo</name></create_user>"
        )

    def test_create_user_with_password(self):
        self.gmp.create_user(name="foo", password="bar")

        self.connection.send.has_been_called_with(
            "<create_user>"
            "<name>foo</name>"
            "<password>bar</password>"
            "</create_user>"
        )

    def test_create_user_with_hosts(self):
        self.gmp.create_user(name="foo", hosts=["h1", "h2"], hosts_allow=True)

        self.connection.send.has_been_called_with(
            "<create_user>"
            "<name>foo</name>"
            '<hosts allow="1">h1,h2</hosts>'
            "</create_user>"
        )

        self.gmp.create_user(name="foo", hosts=["h1", "h2"])

        self.connection.send.has_been_called_with(
            "<create_user>"
            "<name>foo</name>"
            '<hosts allow="0">h1,h2</hosts>'
            "</create_user>"
        )

        self.gmp.create_user(name="foo", hosts=["h1", "h2"], hosts_allow=False)

        self.connection.send.has_been_called_with(
            "<create_user>"
            "<name>foo</name>"
            '<hosts allow="0">h1,h2</hosts>'
            "</create_user>"
        )

    @patch("gvm.protocols.gmpv224.entities.users.deprecation")
    def test_create_user_with_ifaces(self, deprecation_mock):
        self.gmp.create_user(name="foo", ifaces=["h1", "h2"], ifaces_allow=True)

        self.connection.send.has_been_called_with(
            "<create_user><name>foo</name></create_user>"
        )

        self.gmp.create_user(name="foo", ifaces=["h1", "h2"])

        self.connection.send.has_been_called_with(
            "<create_user><name>foo</name></create_user>"
        )

        self.gmp.create_user(
            name="foo", ifaces=["h1", "h2"], ifaces_allow=False
        )

        self.connection.send.has_been_called_with(
            "<create_user><name>foo</name></create_user>"
        )

        # pylint: disable=line-too-long
        deprecation_calls = [
            call("The ifaces parameter has been removed in GMP version 224"),
            call(
                "The ifaces_allow parameter has been removed in GMP version 224"
            ),
            call("The ifaces parameter has been removed in GMP version 224"),
            call("The ifaces parameter has been removed in GMP version 224"),
            call(
                "The ifaces_allow parameter has been removed in GMP version 224"
            ),
        ]
        # pylint: enable=line-too-long
        deprecation_mock.assert_has_calls(deprecation_calls)

    def test_create_user_with_role_ids(self):
        self.gmp.create_user(name="foo", role_ids=["r1", "r2"])

        self.connection.send.has_been_called_with(
            "<create_user>"
            "<name>foo</name>"
            '<role id="r1"/>'
            '<role id="r2"/>'
            "</create_user>"
        )
