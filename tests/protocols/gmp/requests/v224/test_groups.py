# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import Groups


class GroupsTestCase(unittest.TestCase):
    def test_clone_group(self):
        request = Groups.clone_group("group_id")
        self.assertEqual(
            bytes(request),
            b"<create_group><copy>group_id</copy></create_group>",
        )

    def test_clone_group_missing_group_id(self):
        with self.assertRaises(RequiredArgument):
            Groups.clone_group(None)

        with self.assertRaises(RequiredArgument):
            Groups.clone_group("")

    def test_create_group(self):
        request = Groups.create_group("group_name")
        self.assertEqual(
            bytes(request),
            b"<create_group><name>group_name</name></create_group>",
        )

    def test_create_group_with_comment(self):
        request = Groups.create_group("group_name", comment="comment")
        self.assertEqual(
            bytes(request),
            b"<create_group>"
            b"<name>group_name</name>"
            b"<comment>comment</comment>"
            b"</create_group>",
        )

    def test_create_group_with_special(self):
        request = Groups.create_group("group_name", special=True)
        self.assertEqual(
            bytes(request),
            b"<create_group>"
            b"<name>group_name</name>"
            b"<specials><full/></specials>"
            b"</create_group>",
        )

        request = Groups.create_group("group_name", special=False)
        self.assertEqual(
            bytes(request),
            b"<create_group><name>group_name</name></create_group>",
        )

    def test_create_group_with_users(self):
        request = Groups.create_group("group_name", users=["user1", "user2"])
        self.assertEqual(
            bytes(request),
            b"<create_group>"
            b"<name>group_name</name>"
            b"<users>user1,user2</users>"
            b"</create_group>",
        )

    def test_create_group_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Groups.create_group(None)

        with self.assertRaises(RequiredArgument):
            Groups.create_group("")

    def test_delete_group(self):
        request = Groups.delete_group("group_id")
        self.assertEqual(
            bytes(request),
            b'<delete_group group_id="group_id" ultimate="0"/>',
        )

    def test_delete_group_with_ultimate(self):
        request = Groups.delete_group("group_id", ultimate=True)
        self.assertEqual(
            bytes(request),
            b'<delete_group group_id="group_id" ultimate="1"/>',
        )

        request = Groups.delete_group("group_id", ultimate=False)
        self.assertEqual(
            bytes(request),
            b'<delete_group group_id="group_id" ultimate="0"/>',
        )

    def test_delete_group_missing_group_id(self):
        with self.assertRaises(RequiredArgument):
            Groups.delete_group(None)

        with self.assertRaises(RequiredArgument):
            Groups.delete_group("")

    def test_get_groups(self):
        request = Groups.get_groups()
        self.assertEqual(
            bytes(request),
            b"<get_groups/>",
        )

    def test_get_groups_with_filter_string(self):
        request = Groups.get_groups(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_groups filter="filter_string"/>',
        )

    def test_get_groups_with_filter_id(self):
        request = Groups.get_groups(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_groups filt_id="filter_id"/>',
        )

    def test_get_groups_with_trash(self):
        request = Groups.get_groups(trash=True)
        self.assertEqual(
            bytes(request),
            b'<get_groups trash="1"/>',
        )

        request = Groups.get_groups(trash=False)
        self.assertEqual(
            bytes(request),
            b'<get_groups trash="0"/>',
        )

    def test_get_group(self):
        request = Groups.get_group("group_id")
        self.assertEqual(
            bytes(request),
            b'<get_groups group_id="group_id"/>',
        )

    def test_group_missing_group_id(self):
        with self.assertRaises(RequiredArgument):
            Groups.get_group(None)

        with self.assertRaises(RequiredArgument):
            Groups.get_group("")

    def test_modify_group(self):
        request = Groups.modify_group("group_id")
        self.assertEqual(
            bytes(request),
            b'<modify_group group_id="group_id"/>',
        )

    def test_modify_group_with_comment(self):
        request = Groups.modify_group("group_id", comment="comment")
        self.assertEqual(
            bytes(request),
            b'<modify_group group_id="group_id">'
            b"<comment>comment</comment>"
            b"</modify_group>",
        )

    def test_modify_group_with_name(self):
        request = Groups.modify_group("group_id", name="name")
        self.assertEqual(
            bytes(request),
            b'<modify_group group_id="group_id">'
            b"<name>name</name>"
            b"</modify_group>",
        )

    def test_modify_group_with_users(self):
        request = Groups.modify_group("group_id", users=["user1", "user2"])
        self.assertEqual(
            bytes(request),
            b'<modify_group group_id="group_id">'
            b"<users>user1,user2</users>"
            b"</modify_group>",
        )

    def test_modify_group_missing_group_id(self):
        with self.assertRaises(RequiredArgument):
            Groups.modify_group(None)

        with self.assertRaises(RequiredArgument):
            Groups.modify_group("")
