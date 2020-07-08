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

from gvm.protocols.gmpv9 import PermissionSubjectType, EntityType


class GmpModifyPermissionTestCase:
    def test_modify_permission(self):
        self.gmp.modify_permission(permission_id='p1')

        self.connection.send.has_been_called_with(
            '<modify_permission permission_id="p1"/>'
        )

    def test_modify_permission_missing_permission_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(permission_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(permission_id='')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission('')

    def test_modify_permission_with_comment(self):
        self.gmp.modify_permission(permission_id='p1', comment='foo')

        self.connection.send.has_been_called_with(
            '<modify_permission permission_id="p1">'
            '<comment>foo</comment>'
            '</modify_permission>'
        )

    def test_modify_permission_with_resource_id_and_type(self):
        self.gmp.modify_permission(
            permission_id='p1', resource_id='r1', resource_type=EntityType.TASK
        )

        self.connection.send.has_been_called_with(
            '<modify_permission permission_id="p1">'
            '<resource id="r1">'
            '<type>task</type>'
            '</resource>'
            '</modify_permission>'
        )

    def test_modify_permission_with_missing_resource_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id='p1', resource_id='', resource_type='foo'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(permission_id='p1', resource_type='foo')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id='p1', resource_id=None, resource_type='foo'
            )

    def test_modify_permission_with_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id='p1', resource_id='r1', resource_type=''
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(permission_id='p1', resource_id='r1')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id='p1', resource_id='r1', resource_type=None
            )

    def test_modify_permission_with_subject_id_and_type(self):
        self.gmp.modify_permission(
            permission_id='p1',
            subject_id='s1',
            subject_type=PermissionSubjectType.ROLE,
        )

        self.connection.send.has_been_called_with(
            '<modify_permission permission_id="p1">'
            '<subject id="s1">'
            '<type>role</type>'
            '</subject>'
            '</modify_permission>'
        )

        self.gmp.modify_permission(
            permission_id='p1',
            subject_id='s1',
            subject_type=PermissionSubjectType.USER,
        )

        self.connection.send.has_been_called_with(
            '<modify_permission permission_id="p1">'
            '<subject id="s1">'
            '<type>user</type>'
            '</subject>'
            '</modify_permission>'
        )

        self.gmp.modify_permission(
            permission_id='p1',
            subject_id='s1',
            subject_type=PermissionSubjectType.GROUP,
        )

        self.connection.send.has_been_called_with(
            '<modify_permission permission_id="p1">'
            '<subject id="s1">'
            '<type>group</type>'
            '</subject>'
            '</modify_permission>'
        )

    def test_modify_permission_missing_subject_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id='p1', subject_type=PermissionSubjectType.ROLE
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id='p1',
                subject_type=PermissionSubjectType.ROLE,
                subject_id='',
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_permission(
                permission_id='p1',
                subject_type=PermissionSubjectType.ROLE,
                subject_id=None,
            )

    def test_modify_permission_invalid_subject_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_permission(
                permission_id='p1', subject_id='s1', subject_type='foo'
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_permission(
                permission_id='p1', subject_id='s1', subject_type=''
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_permission(
                permission_id='p1', subject_id='s1', subject_type=None
            )

    def test_modify_permission_with_name(self):
        self.gmp.modify_permission(permission_id='p1', name='foo')

        self.connection.send.has_been_called_with(
            '<modify_permission permission_id="p1">'
            '<name>foo</name>'
            '</modify_permission>'
        )


if __name__ == '__main__':
    unittest.main()
