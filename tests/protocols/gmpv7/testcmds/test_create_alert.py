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

from gvm.errors import RequiredArgument, InvalidArgument, InvalidArgumentType

from gvm.protocols.gmpv7 import AlertCondition, AlertEvent, AlertMethod


class GmpCreateAlertTestCase:
    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='',
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name=None,
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

    def test_missing_condition(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition='', event='bar', method='lorem'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition=None, event='bar', method='lorem'
            )

    def test_missing_event(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition='bar', event='', method='lorem'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition='bar', event=None, method='lorem'
            )

    def test_missing_method(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition='bar', event='lorem', method=''
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name='foo', condition='bar', event='lorem', method=None
            )

    def test_invalid_condition(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_alert(
                name='foo',
                condition='bar',
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

    def test_invalid_event(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_alert(
                name='foo',
                condition=AlertCondition.ALWAYS,
                event='lorem',
                method=AlertMethod.EMAIL,
            )

    def test_invalid_method(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_alert(
                name='foo',
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method='ipsum',
            )

    def test_invalid_condition_for_secinfo(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name='foo',
                condition=AlertCondition.SEVERITY_AT_LEAST,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.EMAIL,
            )

    def test_invalid_method_for_secinfo(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name='foo',
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.HTTP_GET,
            )

    def test_create_alert(self):
        self.gmp.create_alert(
            name='foo',
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
        )

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>Always</condition>'
            '<event>Task run status changed</event>'
            '<method>Email</method>'
            '</create_alert>'
        )

    def test_create_alert_with_filter_id(self):
        self.gmp.create_alert(
            name='foo',
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            filter_id='f1',
        )

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>Always</condition>'
            '<event>Task run status changed</event>'
            '<method>Email</method>'
            '<filter id="f1"/>'
            '</create_alert>'
        )

    def test_create_alert_with_comment(self):
        self.gmp.create_alert(
            name='foo',
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            comment='hello',
        )

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>Always</condition>'
            '<event>Task run status changed</event>'
            '<method>Email</method>'
            '<comment>hello</comment>'
            '</create_alert>'
        )

    def test_create_alert_with_condition_data(self):
        self.gmp.create_alert(
            name='foo',
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            condition_data={'foo': 'bar'},
        )

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>Always<data>bar<name>foo</name></data></condition>'
            '<event>Task run status changed</event>'
            '<method>Email</method>'
            '</create_alert>'
        )

    def test_create_alert_with_event_data(self):
        self.gmp.create_alert(
            name='foo',
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            event_data={'foo': 'bar'},
        )

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>Always</condition>'
            '<event>Task run status changed'
            '<data>bar<name>foo</name></data>'
            '</event>'
            '<method>Email</method>'
            '</create_alert>'
        )

    def test_create_alert_with_method_data(self):
        self.gmp.create_alert(
            name='foo',
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            method_data={'foo': 'bar'},
        )

        self.connection.send.has_been_called_with(
            '<create_alert>'
            '<name>foo</name>'
            '<condition>Always</condition>'
            '<event>Task run status changed</event>'
            '<method>Email<data>bar<name>foo</name></data></method>'
            '</create_alert>'
        )


if __name__ == '__main__':
    unittest.main()
