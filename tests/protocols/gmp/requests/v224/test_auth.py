# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests.v224 import Authentication


class AuthenticationTestCase(unittest.TestCase):
    def test_authenticate(self) -> None:
        request = Authentication.authenticate("admin", "admin")

        self.assertIsInstance(request, Request)
        self.assertEqual(
            bytes(request),
            b"<authenticate><credentials><username>admin</username>"
            b"<password>admin</password></credentials></authenticate>",
        )

    def test_authenticate_missing_username(self) -> None:
        with self.assertRaises(RequiredArgument):
            Authentication.authenticate(None, "foo")  # type: ignore

        with self.assertRaises(RequiredArgument):
            Authentication.authenticate("", "foo")

    def test_authenticate_missing_password(self) -> None:
        with self.assertRaises(RequiredArgument):
            Authentication.authenticate("bar", None)  # type: ignore

        with self.assertRaises(RequiredArgument):
            Authentication.authenticate("bar", "")

    def test_describe_auth(self) -> None:
        request = Authentication.describe_auth()

        self.assertIsInstance(request, Request)
        self.assertEqual(bytes(request), b"<describe_auth/>")

    def test_modify_auth(self) -> None:
        request = Authentication.modify_auth(
            "foo", dict([("foo", "bar"), ("lorem", "ipsum")])
        )

        self.assertIsInstance(request, Request)
        self.assertEqual(
            bytes(request),
            b"<modify_auth>"
            b'<group name="foo">'
            b"<auth_conf_setting>"
            b"<key>foo</key>"
            b"<value>bar</value>"
            b"</auth_conf_setting>"
            b"<auth_conf_setting>"
            b"<key>lorem</key>"
            b"<value>ipsum</value>"
            b"</auth_conf_setting>"
            b"</group>"
            b"</modify_auth>",
        )

    def test_modify_auth_missing_group_name(self) -> None:
        with self.assertRaises(RequiredArgument):
            Authentication.modify_auth(
                group_name=None, auth_conf_settings={"foo": "bar"}  # type: ignore
            )

        with self.assertRaises(RequiredArgument):
            Authentication.modify_auth(
                group_name="", auth_conf_settings={"foo": "bar"}
            )

        with self.assertRaises(RequiredArgument):
            Authentication.modify_auth("", auth_conf_settings={"foo": "bar"})

    def test_modify_auth_auth_conf_settings(self) -> None:
        with self.assertRaises(RequiredArgument):
            Authentication.modify_auth(
                group_name="foo", auth_conf_settings=None  # type: ignore
            )

        with self.assertRaises(RequiredArgument):
            Authentication.modify_auth(group_name="foo", auth_conf_settings="")  # type: ignore

        with self.assertRaises(RequiredArgument):
            Authentication.modify_auth("foo", "")  # type: ignore

        with self.assertRaises(RequiredArgument):
            Authentication.modify_auth("foo", {})
