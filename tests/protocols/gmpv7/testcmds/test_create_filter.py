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

from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv7 import FilterType


class GmpCreateFilterCommandTestCase:
    def test_all_available_filters_types_correct(self):
        for filter_type in list(FilterType):
            self.gmp.create_filter(
                name='f1',
                term='sort-reverse=threat first=1 rows=1000',
                filter_type=filter_type,
            )

            self.connection.send.has_been_called_with(
                '<create_filter>'
                '<name>f1</name>'
                '<term>sort-reverse=threat first=1 rows=1000</term>'
                '<type>{}</type>'
                '</create_filter>'.format(filter_type.value)
            )

    def test_create_filter_invalid_filter_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_filter(
                name='f1',
                term='sort-reverse=threat result_hosts_only=1 '
                'notes=1 overrides=1 levels=hml first=1 rows=1000',
                filter_type='foo',
            )

    def test_create_filter(self):
        self.gmp.create_filter(
            name='f1',
            term='sort-reverse=threat result_hosts_only=1 '
            'notes=1 overrides=1 levels=hml first=1 rows=1000',
            filter_type=FilterType.TASK,
            comment='foo',
        )

        self.connection.send.has_been_called_with(
            '<create_filter>'
            '<name>f1</name>'
            '<comment>foo</comment>'
            '<term>sort-reverse=threat result_hosts_only=1 notes=1 '
            'overrides=1 levels=hml first=1 rows=1000</term>'
            '<type>task</type>'
            '</create_filter>'
        )

    def test_create_filter_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_filter('')

        with self.assertRaises(RequiredArgument):
            self.gmp.create_filter(None)


if __name__ == '__main__':
    unittest.main()
