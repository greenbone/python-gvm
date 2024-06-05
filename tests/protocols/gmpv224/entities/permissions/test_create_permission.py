# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import EntityType, PermissionSubjectType


class GmpCreatePermissionTestMixin:
    def test_create_permission(self):
        self.gmp.create_permission(
            "foo", subject_id="u1", subject_type=PermissionSubjectType.USER
        )

        self.connection.send.has_been_called_with(
            b"<create_permission>"
            b"<name>foo</name>"
            b'<subject id="u1">'
            b"<type>user</type>"
            b"</subject>"
            b"</create_permission>"
        )

    def test_create_permission_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                None, subject_id="u1", subject_type=PermissionSubjectType.USER
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                "", subject_id="u1", subject_type=PermissionSubjectType.USER
            )

    def test_create_permission_missing_subject_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                "create_task",
                subject_id=None,
                subject_type=PermissionSubjectType.USER,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                "create_task",
                subject_id="",
                subject_type=PermissionSubjectType.USER,
            )

    def test_create_permission_invalid_subject_type(self):
        with self.assertRaises(ValueError):
            self.gmp.create_permission(
                "create_task", subject_id="u1", subject_type=""
            )

        with self.assertRaises(ValueError):
            self.gmp.create_permission(
                "create_task", subject_id="u1", subject_type=None
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_permission(
                "create_task", subject_id="u1", subject_type="foo"
            )

    def test_create_permission_with_comment(self):
        self.gmp.create_permission(
            "create_task",
            subject_id="u1",
            subject_type=PermissionSubjectType.USER,
            comment="foo",
        )

        self.connection.send.has_been_called_with(
            b"<create_permission>"
            b"<name>create_task</name>"
            b'<subject id="u1">'
            b"<type>user</type>"
            b"</subject>"
            b"<comment>foo</comment>"
            b"</create_permission>"
        )

    def test_create_permission_missing_resource_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                "create_task",
                subject_id="u1",
                subject_type=PermissionSubjectType.USER,
                resource_type=EntityType.TASK,
            )

    def test_create_permission_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                "create_task",
                subject_id="u1",
                subject_type=PermissionSubjectType.USER,
                resource_id="t1",
            )

    def test_create_permission_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_permission(
                "create_task",
                subject_id="u1",
                subject_type=PermissionSubjectType.USER,
                resource_type="foo",
                resource_id="t1",
            )

    def test_create_permission_with_resource(self):
        self.gmp.create_permission(
            "create_task",
            subject_id="u1",
            subject_type=PermissionSubjectType.USER,
            resource_id="t1",
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            b"<create_permission>"
            b"<name>create_task</name>"
            b'<subject id="u1">'
            b"<type>user</type>"
            b"</subject>"
            b'<resource id="t1">'
            b"<type>task</type>"
            b"</resource>"
            b"</create_permission>"
        )

    def test_create_permission_with_resource_type_audit(self):
        self.gmp.create_permission(
            "create_task",
            subject_id="u1",
            subject_type=PermissionSubjectType.USER,
            resource_id="t1",
            resource_type=EntityType.AUDIT,
        )

        self.connection.send.has_been_called_with(
            b"<create_permission>"
            b"<name>create_task</name>"
            b'<subject id="u1">'
            b"<type>user</type>"
            b"</subject>"
            b'<resource id="t1">'
            b"<type>task</type>"
            b"</resource>"
            b"</create_permission>"
        )

    def test_create_permission_with_resource_type_policy(self):
        self.gmp.create_permission(
            "create_task",
            subject_id="u1",
            subject_type=PermissionSubjectType.USER,
            resource_id="t1",
            resource_type=EntityType.POLICY,
        )

        self.connection.send.has_been_called_with(
            b"<create_permission>"
            b"<name>create_task</name>"
            b'<subject id="u1">'
            b"<type>user</type>"
            b"</subject>"
            b'<resource id="t1">'
            b"<type>config</type>"
            b"</resource>"
            b"</create_permission>"
        )
