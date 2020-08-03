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


class GmpCreateAgentTestCase:
    def test_missing_installer(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_agent(installer='', signature='foo', name='bar')

        with self.assertRaises(RequiredArgument):
            self.gmp.create_agent(installer=None, signature='foo', name='bar')

    def test_missing_signature(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_agent(installer='foo', signature='', name='bar')

        with self.assertRaises(RequiredArgument):
            self.gmp.create_agent(installer='foo', signature=None, name='bar')

    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_agent(installer='foo', signature='bar', name='')

        with self.assertRaises(RequiredArgument):
            self.gmp.create_agent(installer='foo', signature='bar', name=None)

    def test_create_agent(self):
        self.gmp.create_agent(installer='foo', signature='bar', name='ipsum')

        self.connection.send.has_been_called_with(
            '<create_agent>'
            '<installer>foo</installer>'
            '<signature>bar</signature>'
            '<name>ipsum</name>'
            '</create_agent>'
        )

    def test_create_agent_with_comment(self):
        self.gmp.create_agent(
            installer='foo', signature='bar', name='ipsum', comment='lorem'
        )

        self.connection.send.has_been_called_with(
            '<create_agent>'
            '<installer>foo</installer>'
            '<signature>bar</signature>'
            '<name>ipsum</name>'
            '<comment>lorem</comment>'
            '</create_agent>'
        )

    def test_create_agent_with_howto_install(self):
        self.gmp.create_agent(
            installer='foo',
            signature='bar',
            name='ipsum',
            howto_install='lorem',
        )

        self.connection.send.has_been_called_with(
            '<create_agent>'
            '<installer>foo</installer>'
            '<signature>bar</signature>'
            '<name>ipsum</name>'
            '<howto_install>lorem</howto_install>'
            '</create_agent>'
        )

    def test_create_agent_with_howto_use(self):
        self.gmp.create_agent(
            installer='foo', signature='bar', name='ipsum', howto_use='lorem'
        )

        self.connection.send.has_been_called_with(
            '<create_agent>'
            '<installer>foo</installer>'
            '<signature>bar</signature>'
            '<name>ipsum</name>'
            '<howto_use>lorem</howto_use>'
            '</create_agent>'
        )


if __name__ == '__main__':
    unittest.main()
