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

from gvm.errors import RequiredArgument

from gvm.protocols.gmpv7 import EntityType


class GmpCreateTagTestCase:
    def test_create_tag_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name=None, resource_id='foo', resource_type=EntityType.TASK
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name='', resource_id='foo', resource_type=EntityType.TASK
            )

    def test_create_tag_missing_resource_id(self):
        self.gmp.create_tag(
            name='foo', resource_id=None, resource_type=EntityType.TASK
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resource id="">'
            '<type>task</type>'
            '</resource>'
            '</create_tag>'
        )

        self.gmp.create_tag(
            name='foo', resource_id='', resource_type=EntityType.TASK
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resource id="">'
            '<type>task</type>'
            '</resource>'
            '</create_tag>'
        )

    def test_create_tag_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name='foo', resource_id='foo', resource_type=None
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(name='foo', resource_id='foo', resource_type='')

    def test_create_tag(self):
        self.gmp.create_tag(
            name='foo', resource_id='foo', resource_type=EntityType.TASK
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resource id="foo">'
            '<type>task</type>'
            '</resource>'
            '</create_tag>'
        )

    def test_create_tag_with_comment(self):
        self.gmp.create_tag(
            name='foo',
            resource_id='foo',
            resource_type=EntityType.TASK,
            comment='bar',
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resource id="foo">'
            '<type>task</type>'
            '</resource>'
            '<comment>bar</comment>'
            '</create_tag>'
        )

    def test_create_tag_with_value(self):
        self.gmp.create_tag(
            name='foo',
            resource_id='foo',
            resource_type=EntityType.TASK,
            value='bar',
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resource id="foo">'
            '<type>task</type>'
            '</resource>'
            '<value>bar</value>'
            '</create_tag>'
        )

    def test_create_tag_with_active(self):
        self.gmp.create_tag(
            name='foo',
            resource_id='foo',
            resource_type=EntityType.TASK,
            active=True,
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resource id="foo">'
            '<type>task</type>'
            '</resource>'
            '<active>1</active>'
            '</create_tag>'
        )

        self.gmp.create_tag(
            name='foo',
            resource_id='foo',
            resource_type=EntityType.TASK,
            active=False,
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resource id="foo">'
            '<type>task</type>'
            '</resource>'
            '<active>0</active>'
            '</create_tag>'
        )


if __name__ == '__main__':
    unittest.main()
