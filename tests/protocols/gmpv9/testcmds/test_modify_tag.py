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
from gvm.protocols.gmpv9 import EntityType


class GmpModifyTagTestCase:
    def test_modify_tag(self):
        self.gmp.modify_tag(tag_id='t1')

        self.connection.send.has_been_called_with('<modify_tag tag_id="t1"/>')

    def test_modify_tag_missing_tag_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_tag(tag_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_tag(tag_id='')

    def test_modify_tag_with_comment(self):
        self.gmp.modify_tag(tag_id='t1', comment='foo')

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1"><comment>foo</comment></modify_tag>'
        )

    def test_modify_tag_with_value(self):
        self.gmp.modify_tag(tag_id='t1', value='foo')

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1"><value>foo</value></modify_tag>'
        )

    def test_modify_tag_with_name(self):
        self.gmp.modify_tag(tag_id='t1', name='foo')

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1"><name>foo</name></modify_tag>'
        )

    def test_modify_tag_with_active(self):
        self.gmp.modify_tag(tag_id='t1', active=True)

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1"><active>1</active></modify_tag>'
        )

        self.gmp.modify_tag(tag_id='t1', active=False)

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1"><active>0</active></modify_tag>'
        )

    def test_modify_tag_with_resource_filter_and_type(self):
        self.gmp.modify_tag(
            tag_id='t1',
            resource_filter='name=foo',
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1">'
            '<resources filter="name=foo">'
            '<type>task</type>'
            '</resources>'
            '</modify_tag>'
        )

    def test_modify_tag_with_resource_action_filter_and_type(self):
        self.gmp.modify_tag(
            tag_id='t1',
            resource_action='set',
            resource_filter='name=foo',
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1">'
            '<resources action="set" filter="name=foo">'
            '<type>task</type>'
            '</resources>'
            '</modify_tag>'
        )

    def test_modify_tag_with_resource_ids_and_type(self):
        self.gmp.modify_tag(
            tag_id='t1', resource_ids=['r1'], resource_type=EntityType.TASK
        )

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1">'
            '<resources>'
            '<resource id="r1"/>'
            '<type>task</type>'
            '</resources>'
            '</modify_tag>'
        )

    def test_modify_tag_with_resource_action_ids_and_type(self):
        self.gmp.modify_tag(
            tag_id='t1',
            resource_action="set",
            resource_ids=['r1'],
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1">'
            '<resources action="set">'
            '<resource id="r1"/>'
            '<type>task</type>'
            '</resources>'
            '</modify_tag>'
        )

    def test_modify_tag_with_missing_resource_filter_or_ids_andtype(self):
        self.gmp.modify_tag(tag_id='t1', resource_action='add')

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1">'
            '<resources action="add"/>'
            '</modify_tag>'
        )

    def test_modify_tag_with_missing_resource_type(self):
        self.gmp.modify_tag(tag_id='t1', resource_ids=['r1'])

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1">'
            '<resources>'
            '<resource id="r1"/>'
            '</resources>'
            '</modify_tag>'
        )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_tag(tag_id='t1', resource_filter='name=foo')

    def test_modify_tag_with_missing_resource_filter_and_ids(self):
        self.gmp.modify_tag(tag_id='t1', resource_type=EntityType.TASK)

        self.connection.send.has_been_called_with(
            '<modify_tag tag_id="t1">'
            '<resources>'
            '<type>task</type>'
            '</resources>'
            '</modify_tag>'
        )


if __name__ == '__main__':
    unittest.main()
