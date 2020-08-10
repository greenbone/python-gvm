# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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
from gvm.protocols.gmpv9 import FilterType


class GmpModifyFilterTestCase:
    def test_modify_filter(self):
        self.gmp.modify_filter(filter_id='f1')

        self.connection.send.has_been_called_with(
            '<modify_filter filter_id="f1"/>'
        )

    def test_modify_filter_with_filter_type(self):
        self.gmp.modify_filter(filter_id='f1', filter_type=FilterType.TASK)

        self.connection.send.has_been_called_with(
            '<modify_filter filter_id="f1">'
            '<type>task</type>'
            '</modify_filter>'
        )

    def test_modify_filter_invalid_filter_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_filter(filter_id='f1', filter_type='foo')

    def test_modify_filter_missing_filter_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_filter(filter_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_filter(filter_id='')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_filter('')

    def test_modify_filter_with_comment(self):
        self.gmp.modify_filter(filter_id='f1', comment='foo')

        self.connection.send.has_been_called_with(
            '<modify_filter filter_id="f1">'
            '<comment>foo</comment>'
            '</modify_filter>'
        )

    def test_modify_filter_with_name(self):
        self.gmp.modify_filter(filter_id='f1', name='foo')

        self.connection.send.has_been_called_with(
            '<modify_filter filter_id="f1">'
            '<name>foo</name>'
            '</modify_filter>'
        )

    def test_modify_filter_with_term(self):
        self.gmp.modify_filter(filter_id='f1', term='foo=bar')

        self.connection.send.has_been_called_with(
            '<modify_filter filter_id="f1">'
            '<term>foo=bar</term>'
            '</modify_filter>'
        )


if __name__ == '__main__':
    unittest.main()
