# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import Permissions, PermissionSubjectType


class PermissionsTestCase(unittest.TestCase):
    def test_clone_permission(self):
        request = Permissions.clone_permission("permission_id")
        self.assertEqual(
            bytes(request),
            b"<create_permission><copy>permission_id</copy></create_permission>",
        )

    def test_clone_permission_missing_permission_id(self):
        with self.assertRaises(RequiredArgument):
            Permissions.clone_permission(None)

        with self.assertRaises(RequiredArgument):
            Permissions.clone_permission("")

    def test_create_permission(self):
        request = Permissions.create_permission(
            "name", "subject_id", PermissionSubjectType.USER
        )
        self.assertEqual(
            bytes(request),
            b"<create_permission>"
            b"<name>name</name>"
            b'<subject id="subject_id">'
            b"<type>user</type>"
            b"</subject>"
            b"</create_permission>",
        )

        request = Permissions.create_permission(
            "name",
            "subject_id",
            "user",
        )
        self.assertEqual(
            bytes(request),
            b"<create_permission>"
            b"<name>name</name>"
            b'<subject id="subject_id">'
            b"<type>user</type>"
            b"</subject>"
            b"</create_permission>",
        )

    def test_create_permission_with_resource(self):
        request = Permissions.create_permission(
            "name",
            "subject_id",
            PermissionSubjectType.USER,
            resource_id="resource_id",
            resource_type="alert",
        )
        self.assertEqual(
            bytes(request),
            b"<create_permission>"
            b"<name>name</name>"
            b'<subject id="subject_id">'
            b"<type>user</type>"
            b"</subject>"
            b'<resource id="resource_id">'
            b"<type>alert</type>"
            b"</resource>"
            b"</create_permission>",
        )

    def test_create_permission_with_comment(self):
        request = Permissions.create_permission(
            "name",
            "subject_id",
            PermissionSubjectType.USER,
            comment="comment",
        )
        self.assertEqual(
            bytes(request),
            b"<create_permission>"
            b"<name>name</name>"
            b'<subject id="subject_id">'
            b"<type>user</type>"
            b"</subject>"
            b"<comment>comment</comment>"
            b"</create_permission>",
        )

    def test_create_permission_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Permissions.create_permission(
                None, "subject_id", PermissionSubjectType.USER
            )

        with self.assertRaises(RequiredArgument):
            Permissions.create_permission(
                "", "subject_id", PermissionSubjectType.USER
            )

    def test_create_permission_missing_subject_id(self):
        with self.assertRaises(RequiredArgument):
            Permissions.create_permission(
                "name", None, PermissionSubjectType.USER
            )

        with self.assertRaises(RequiredArgument):
            Permissions.create_permission(
                "name", "", PermissionSubjectType.USER
            )

    def test_create_permission_with_resource_missing_resource_id(self):
        with self.assertRaises(RequiredArgument):
            Permissions.create_permission(
                "name",
                "subject_id",
                PermissionSubjectType.USER,
                resource_type="alert",
            )

    def test_create_permission_with_resource_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            Permissions.create_permission(
                "name",
                "subject_id",
                PermissionSubjectType.USER,
                resource_id="resource_id",
            )

    def test_create_permission_invalid_subject_type(self):
        with self.assertRaises(InvalidArgument):
            Permissions.create_permission("name", "subject_id", "invalid")

    def test_create_permission_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            Permissions.create_permission(
                "name",
                "subject_id",
                PermissionSubjectType.USER,
                resource_id="resource_id",
                resource_type="invalid",
            )

    def test_delete_permission(self):
        request = Permissions.delete_permission("permission_id")
        self.assertEqual(
            bytes(request),
            b'<delete_permission permission_id="permission_id" ultimate="0"/>',
        )

    def test_delete_permission_ultimate(self):
        request = Permissions.delete_permission("permission_id", ultimate=True)
        self.assertEqual(
            bytes(request),
            b'<delete_permission permission_id="permission_id" ultimate="1"/>',
        )

        request = Permissions.delete_permission("permission_id", ultimate=False)
        self.assertEqual(
            bytes(request),
            b'<delete_permission permission_id="permission_id" ultimate="0"/>',
        )

    def test_delete_permission_missing_permission_id(self):
        with self.assertRaises(RequiredArgument):
            Permissions.delete_permission(None)

        with self.assertRaises(RequiredArgument):
            Permissions.delete_permission("")

    def test_get_permissions(self):
        request = Permissions.get_permissions()
        self.assertEqual(
            bytes(request),
            b"<get_permissions/>",
        )

    def test_get_permissions_with_filter_string(self):
        request = Permissions.get_permissions(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_permissions filter="filter_string"/>',
        )

    def test_get_permissions_with_filter_id(self):
        request = Permissions.get_permissions(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_permissions filt_id="filter_id"/>',
        )

    def test_get_permissions_with_trash(self):
        request = Permissions.get_permissions(trash=True)
        self.assertEqual(
            bytes(request),
            b'<get_permissions trash="1"/>',
        )

        request = Permissions.get_permissions(trash=False)
        self.assertEqual(
            bytes(request),
            b'<get_permissions trash="0"/>',
        )

    def test_get_permission(self):
        request = Permissions.get_permission("permission_id")
        self.assertEqual(
            bytes(request),
            b'<get_permissions permission_id="permission_id"/>',
        )

    def test_get_permission_missing_permission_id(self):
        with self.assertRaises(RequiredArgument):
            Permissions.get_permission(None)

        with self.assertRaises(RequiredArgument):
            Permissions.get_permission("")

    def test_modify_permission(self):
        request = Permissions.modify_permission("permission_id")
        self.assertEqual(
            bytes(request),
            b'<modify_permission permission_id="permission_id"/>',
        )

    def test_modify_permission_with_name(self):
        request = Permissions.modify_permission("permission_id", name="name")
        self.assertEqual(
            bytes(request),
            b'<modify_permission permission_id="permission_id">'
            b"<name>name</name>"
            b"</modify_permission>",
        )

    def test_modify_permission_with_comment(self):
        request = Permissions.modify_permission(
            "permission_id", comment="comment"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_permission permission_id="permission_id">'
            b"<comment>comment</comment>"
            b"</modify_permission>",
        )

    def test_modify_permission_with_resource(self):
        request = Permissions.modify_permission(
            "permission_id", resource_id="resource_id", resource_type="alert"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_permission permission_id="permission_id">'
            b'<resource id="resource_id">'
            b"<type>alert</type>"
            b"</resource>"
            b"</modify_permission>",
        )

    def test_modify_permission_with_subject(self):
        request = Permissions.modify_permission(
            "permission_id", subject_id="subject_id", subject_type="user"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_permission permission_id="permission_id">'
            b'<subject id="subject_id">'
            b"<type>user</type>"
            b"</subject>"
            b"</modify_permission>",
        )

    def test_modify_permission_with_resource_missing_resource_id(self):
        with self.assertRaises(RequiredArgument):
            Permissions.modify_permission(
                "permission_id", resource_type="alert"
            )

    def test_modify_permission_with_resource_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            Permissions.modify_permission(
                "permission_id", resource_id="resource_id"
            )

    def test_modify_permission_with_subject_missing_subject_id(self):
        with self.assertRaises(RequiredArgument):
            Permissions.modify_permission("permission_id", subject_type="user")

    def test_modify_permission_with_subject_missing_subject_type(self):
        with self.assertRaises(RequiredArgument):
            Permissions.modify_permission(
                "permission_id", subject_id="subject_id"
            )

    def test_modify_permission_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            Permissions.modify_permission(
                "permission_id",
                resource_id="resource_id",
                resource_type="invalid",
            )

    def test_modify_permission_invalid_subject_type(self):
        with self.assertRaises(InvalidArgument):
            Permissions.modify_permission(
                "permission_id", subject_type="invalid", subject_id="subject_id"
            )
