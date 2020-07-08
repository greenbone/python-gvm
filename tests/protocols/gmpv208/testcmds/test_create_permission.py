# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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

import unittest

from gvm.errors import RequiredArgument, InvalidArgumentType

from gvm.protocols.gmpv208 import PermissionSubjectType, EntityType


class GmpCreatePermissionTestCase:
    def test_create_permission(self):
        self.gmp.create_permission(
            'foo', subject_id='u1', subject_type=PermissionSubjectType.USER
        )

        self.connection.send.has_been_called_with(
            '<create_permission>'
            '<name>foo</name>'
            '<subject id="u1">'
            '<type>user</type>'
            '</subject>'
            '</create_permission>'
        )

    def test_create_permission_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                None, subject_id='u1', subject_type=PermissionSubjectType.USER
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                '', subject_id='u1', subject_type=PermissionSubjectType.USER
            )

    def test_create_permission_missing_subject_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                'create_task',
                subject_id=None,
                subject_type=PermissionSubjectType.USER,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                'create_task',
                subject_id='',
                subject_type=PermissionSubjectType.USER,
            )

    def test_create_permission_invalid_subject_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_permission(
                'create_task', subject_id='u1', subject_type=''
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_permission(
                'create_task', subject_id='u1', subject_type=None
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_permission(
                'create_task', subject_id='u1', subject_type='foo'
            )

    def test_create_permission_with_comment(self):
        self.gmp.create_permission(
            'create_task',
            subject_id='u1',
            subject_type=PermissionSubjectType.USER,
            comment='foo',
        )

        self.connection.send.has_been_called_with(
            '<create_permission>'
            '<name>create_task</name>'
            '<subject id="u1">'
            '<type>user</type>'
            '</subject>'
            '<comment>foo</comment>'
            '</create_permission>'
        )

    def test_create_permission_missing_resource_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                'create_task',
                subject_id='u1',
                subject_type=PermissionSubjectType.USER,
                resource_type='task',
            )

    def test_create_permission_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_permission(
                'create_task',
                subject_id='u1',
                subject_type=PermissionSubjectType.USER,
                resource_id='t1',
            )

    def test_create_permission_with_resource(self):
        self.gmp.create_permission(
            'create_task',
            subject_id='u1',
            subject_type=PermissionSubjectType.USER,
            resource_id='t1',
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            '<create_permission>'
            '<name>create_task</name>'
            '<subject id="u1">'
            '<type>user</type>'
            '</subject>'
            '<resource id="t1">'
            '<type>task</type>'
            '</resource>'
            '</create_permission>'
        )


if __name__ == '__main__':
    unittest.main()
