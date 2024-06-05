# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import Roles


class RolesTestCase(unittest.TestCase):
    def test_clone_role(self):
        request = Roles.clone_role("role_id")
        self.assertEqual(
            bytes(request),
            b"<create_role><copy>role_id</copy></create_role>",
        )

    def test_clone_role_missing_role_id(self):
        with self.assertRaises(RequiredArgument):
            Roles.clone_role(None)

        with self.assertRaises(RequiredArgument):
            Roles.clone_role("")

    def test_create_role(self):
        request = Roles.create_role("name")
        self.assertEqual(
            bytes(request),
            b"<create_role><name>name</name></create_role>",
        )

    def test_create_role_with_comment(self):
        request = Roles.create_role("name", comment="comment")
        self.assertEqual(
            bytes(request),
            b"<create_role>"
            b"<name>name</name>"
            b"<comment>comment</comment>"
            b"</create_role>",
        )

    def test_create_role_with_users(self):
        request = Roles.create_role("name", users=["user1", "user2"])
        self.assertEqual(
            bytes(request),
            b"<create_role>"
            b"<name>name</name>"
            b"<users>user1,user2</users>"
            b"</create_role>",
        )

    def test_create_role_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Roles.create_role(None)

        with self.assertRaises(RequiredArgument):
            Roles.create_role("")

    def test_get_roles(self):
        request = Roles.get_roles()
        self.assertEqual(
            bytes(request),
            b"<get_roles/>",
        )

    def test_get_roles_with_filter_string(self):
        request = Roles.get_roles(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_roles filter="filter_string"/>',
        )

    def test_get_roles_with_filter_id(self):
        request = Roles.get_roles(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_roles filt_id="filter_id"/>',
        )

    def test_get_roles_with_trash(self):
        request = Roles.get_roles(trash=True)
        self.assertEqual(
            bytes(request),
            b'<get_roles trash="1"/>',
        )

        request = Roles.get_roles(trash=False)
        self.assertEqual(
            bytes(request),
            b'<get_roles trash="0"/>',
        )

    def test_get_role(self):
        request = Roles.get_role("role_id")
        self.assertEqual(
            bytes(request),
            b'<get_roles role_id="role_id"/>',
        )

    def test_get_role_missing_role_id(self):
        with self.assertRaises(RequiredArgument):
            Roles.get_role(None)

        with self.assertRaises(RequiredArgument):
            Roles.get_role("")

    def test_modify_role(self):
        request = Roles.modify_role("role_id")
        self.assertEqual(
            bytes(request),
            b'<modify_role role_id="role_id"/>',
        )

    def test_modify_role_with_comment(self):
        request = Roles.modify_role("role_id", comment="comment")
        self.assertEqual(
            bytes(request),
            b'<modify_role role_id="role_id">'
            b"<comment>comment</comment>"
            b"</modify_role>",
        )

    def test_modify_role_with_name(self):
        request = Roles.modify_role("role_id", name="name")
        self.assertEqual(
            bytes(request),
            b'<modify_role role_id="role_id">'
            b"<name>name</name>"
            b"</modify_role>",
        )

    def test_modify_role_with_users(self):
        request = Roles.modify_role("role_id", users=["user1", "user2"])
        self.assertEqual(
            bytes(request),
            b'<modify_role role_id="role_id">'
            b"<users>user1,user2</users>"
            b"</modify_role>",
        )

    def test_modify_role_missing_role_id(self):
        with self.assertRaises(RequiredArgument):
            Roles.modify_role(None)

        with self.assertRaises(RequiredArgument):
            Roles.modify_role("")
