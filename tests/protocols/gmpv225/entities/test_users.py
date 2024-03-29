# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from unittest.mock import call, patch

from ...gmpv208.entities.users import (
    GmpCloneUserTestMixin,
    GmpDeleteUserTestMixin,
    GmpGetUsersTestMixin,
    GmpGetUserTestMixin,
)
from ...gmpv224.entities.users import (
    GmpCreateUserTestMixin,
    GmpModifyUserTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CloneUserTestCase(GmpCloneUserTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateUserTestCase(GmpCreateUserTestMixin, Gmpv225TestCase):
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
            call("The ifaces parameter has been removed in GMP version 225"),
            call(
                "The ifaces_allow parameter has been removed in GMP version 225"
            ),
            call("The ifaces parameter has been removed in GMP version 225"),
            call("The ifaces parameter has been removed in GMP version 225"),
            call(
                "The ifaces_allow parameter has been removed in GMP version 225"
            ),
        ]
        # pylint: enable=line-too-long
        deprecation_mock.assert_has_calls(deprecation_calls)


class Gmpv225DeleteUserTestCase(GmpDeleteUserTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetUserTestCase(GmpGetUserTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetUsersTestCase(GmpGetUsersTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyUserTestCase(GmpModifyUserTestMixin, Gmpv225TestCase):
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
            call("The ifaces parameter has been removed in GMP version 225"),
            call("The ifaces parameter has been removed in GMP version 225"),
            call("The ifaces parameter has been removed in GMP version 225"),
            call(
                "The ifaces_allow parameter has been removed in GMP version 225"
            ),
            call("The ifaces parameter has been removed in GMP version 225"),
            call(
                "The ifaces_allow parameter has been removed in GMP version 225"
            ),
        ]
        # pylint: enable=line-too-long
        deprecation_mock.assert_has_calls(deprecation_calls)
