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

from gvm.errors import InvalidArgument
from gvm.protocols.gmpv7 import Gmp, FILTER_TYPES

from .. import MockConnection

class GMPCreateFilterCommandTestCase(unittest.TestCase):

    FILTER_NAME = "special filter"

    def setUp(self):
        self.connection = MockConnection()
        self.gmp = Gmp(self.connection)

    def test_all_available_filters_types_correct(self):
        for filter_type in FILTER_TYPES:
            self.gmp.create_filter(
                name=self.FILTER_NAME,
                term='sort-reverse=threat first=1 rows=1000',
                filter_type=filter_type,
            )

            self.connection.send.has_been_called_with(
                '<create_filter>'
                '<name>{0}</name>'
                '<term>sort-reverse=threat first=1 rows=1000</term>'
                '<type>{1}</type>'
                '</create_filter>'.format(self.FILTER_NAME, filter_type),
            )

    def test_invalid_filters_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_filter(
                name=self.FILTER_NAME,
                term='sort-reverse=threat result_hosts_only=1 '
                     'notes=1 overrides=1 levels=hml first=1 rows=1000',
                filter_type='foo',
            )

    def test_all_arguments(self):
        self.gmp.create_filter(
            name=self.FILTER_NAME, make_unique=True,
            term='sort-reverse=threat result_hosts_only=1 '
                 'notes=1 overrides=1 levels=hml first=1 rows=1000',
            filter_type='task',
            comment='foo',
        )

        self.connection.send.has_been_called_with(
            '<create_filter>'
            '<name>{0}<make_unique>1</make_unique></name>'
            '<comment>foo</comment>'
            '<term>sort-reverse=threat result_hosts_only=1 notes=1 '
            'overrides=1 levels=hml first=1 rows=1000</term>'
            '<type>task</type>'
            '</create_filter>'.format(self.FILTER_NAME),
        )


if __name__ == '__main__':
    unittest.main()
