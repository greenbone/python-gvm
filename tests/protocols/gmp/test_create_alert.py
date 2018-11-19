
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
from gvm.protocols.gmpv7 import Gmp

from .. import MockConnection

class GmpCreateAlertTestCase(unittest.TestCase):

    def setUp(self):
        self.connection = MockConnection()
        self.gmp = Gmp(self.connection)

    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='', condition='foo', event='bar', method='lorem')

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name=None, condition='foo', event='bar', method='lorem')

    def test_missing_condition(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition='', event='bar', method='lorem')

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition=None, event='bar', method='lorem')

    def test_missing_event(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition='bar', event='', method='lorem')

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition='bar', event=None, method='lorem')

    def test_missing_method(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition='bar', event='lorem', method='')

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition='bar', event='lorem', method=None)

    def test_create_alert(self):
        self.gmp.create_alert(
            name='foo', condition='bar', event='lorem', method='ipsum')

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>bar</condition>'
            '<event>lorem</event>'
            '<method>ipsum</method>'
            '</create_alert>'
        )

    def test_create_alert_with_filter_id(self):
        self.gmp.create_alert(
            name='foo', condition='bar', event='lorem', method='ipsum',
            filter_id='f1')

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>bar</condition>'
            '<event>lorem</event>'
            '<method>ipsum</method>'
            '<filter id="f1"/>'
            '</create_alert>'
        )

    def test_create_alert_with_comment(self):
        self.gmp.create_alert(
            name='foo', condition='bar', event='lorem', method='ipsum',
            comment='hello')

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>bar</condition>'
            '<event>lorem</event>'
            '<method>ipsum</method>'
            '<comment>hello</comment>'
            '</create_alert>'
        )

    def test_create_alert_with_condition_data(self):
        self.gmp.create_alert(
            name='foo', condition='bar', event='lorem', method='ipsum',
            condition_data={'foo': 'bar'})

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>bar<data>bar<name>foo</name></data></condition>'
            '<event>lorem</event>'
            '<method>ipsum</method>'
            '</create_alert>'
        )

    def test_create_alert_with_event_data(self):
        self.gmp.create_alert(
            name='foo', condition='bar', event='lorem', method='ipsum',
            event_data={'foo': 'bar'})

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>bar</condition>'
            '<event>lorem<data>bar<name>foo</name></data></event>'
            '<method>ipsum</method>'
            '</create_alert>'
        )

    def test_create_alert_with_method_data(self):
        self.gmp.create_alert(
            name='foo', condition='bar', event='lorem', method='ipsum',
            method_data={'foo': 'bar'})

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>bar</condition>'
            '<event>lorem</event>'
            '<method>ipsum<data>bar<name>foo</name></data></method>'
            '</create_alert>'
        )

if __name__ == '__main__':
    unittest.main()
