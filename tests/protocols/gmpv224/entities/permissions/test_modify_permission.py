# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import EntityType, PermissionSubjectType


class GmpModifyPermissionTestMixin:
    def test_modify_permission(self):
        self.gmp.modify_permission(permission_id="p1")

        self.connection.send.has_been_called_with(
            b'<modify_permission permission_id="p1"/>'
        )

    def test_modify_permission_missing_permission_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(permission_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(permission_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission("")

    def test_modify_permission_with_comment(self):
        self.gmp.modify_permission(permission_id="p1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_permission permission_id="p1">'
            b"<comment>foo</comment>"
            b"</modify_permission>"
        )

    def test_modify_permission_with_resource_id_and_type(self):
        self.gmp.modify_permission(
            permission_id="p1", resource_id="r1", resource_type=EntityType.TASK
        )

        self.connection.send.has_been_called_with(
            b'<modify_permission permission_id="p1">'
            b'<resource id="r1">'
            b"<type>task</type>"
            b"</resource>"
            b"</modify_permission>"
        )

    def test_modify_permission_with_resource_id_and_type_audit(self):
        self.gmp.modify_permission(
            permission_id="p1", resource_id="r1", resource_type=EntityType.AUDIT
        )

        self.connection.send.has_been_called_with(
            b'<modify_permission permission_id="p1">'
            b'<resource id="r1">'
            b"<type>task</type>"
            b"</resource>"
            b"</modify_permission>"
        )

    def test_modify_permission_with_resource_id_and_type_policy(self):
        self.gmp.modify_permission(
            permission_id="p1",
            resource_id="r1",
            resource_type=EntityType.POLICY,
        )

        self.connection.send.has_been_called_with(
            b'<modify_permission permission_id="p1">'
            b'<resource id="r1">'
            b"<type>config</type>"
            b"</resource>"
            b"</modify_permission>"
        )

    def test_modify_permission_with_missing_resource_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id="p1",
                resource_id="",
                resource_type=EntityType.TASK,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id="p1", resource_type=EntityType.TASK
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id="p1",
                resource_id=None,
                resource_type=EntityType.TASK,
            )

    def test_modify_permission_with_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id="p1", resource_id="r1", resource_type=""
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(permission_id="p1", resource_id="r1")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id="p1", resource_id="r1", resource_type=None
            )

    def test_modify_permission_with_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_permission(
                permission_id="p1", resource_id="r1", resource_type="blah"
            )

    def test_modify_permission_with_subject_id_and_type(self):
        self.gmp.modify_permission(
            permission_id="p1",
            subject_id="s1",
            subject_type=PermissionSubjectType.ROLE,
        )

        self.connection.send.has_been_called_with(
            b'<modify_permission permission_id="p1">'
            b'<subject id="s1">'
            b"<type>role</type>"
            b"</subject>"
            b"</modify_permission>"
        )

        self.gmp.modify_permission(
            permission_id="p1",
            subject_id="s1",
            subject_type=PermissionSubjectType.USER,
        )

        self.connection.send.has_been_called_with(
            b'<modify_permission permission_id="p1">'
            b'<subject id="s1">'
            b"<type>user</type>"
            b"</subject>"
            b"</modify_permission>"
        )

        self.gmp.modify_permission(
            permission_id="p1",
            subject_id="s1",
            subject_type=PermissionSubjectType.GROUP,
        )

        self.connection.send.has_been_called_with(
            b'<modify_permission permission_id="p1">'
            b'<subject id="s1">'
            b"<type>group</type>"
            b"</subject>"
            b"</modify_permission>"
        )

    def test_modify_permission_missing_subject_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id="p1", subject_type=PermissionSubjectType.ROLE
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id="p1",
                subject_type=PermissionSubjectType.ROLE,
                subject_id="",
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id="p1",
                subject_type=PermissionSubjectType.ROLE,
                subject_id=None,
            )

    def test_modify_permission_invalid_subject_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_permission(
                permission_id="p1", subject_id="s1", subject_type="foo"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id="p1", subject_id="s1", subject_type=""
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id="p1", subject_id="s1", subject_type=None
            )

    def test_modify_permission_with_name(self):
        self.gmp.modify_permission(permission_id="p1", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_permission permission_id="p1">'
            b"<name>foo</name>"
            b"</modify_permission>"
        )
