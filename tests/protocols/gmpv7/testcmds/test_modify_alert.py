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

from gvm.protocols.gmpv7 import AlertCondition, AlertEvent, AlertMethod


class GmpModifyAlertTestCase:
    def test_modify_alert(self):
        self.gmp.modify_alert(alert_id='a1')

        self.connection.send.has_been_called_with(
            '<modify_alert alert_id="a1"/>'
        )

    def test_modify_alert_without_alert_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_alert(alert_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_alert(alert_id='')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_alert('')

    def test_modify_alert_with_comment(self):
        self.gmp.modify_alert(alert_id='a1', comment='lorem')

        self.connection.send.has_been_called_with(
            '<modify_alert alert_id="a1">'
            '<comment>lorem</comment>'
            '</modify_alert>'
        )

    def test_modify_alert_with_name(self):
        self.gmp.modify_alert(alert_id='a1', name='lorem')

        self.connection.send.has_been_called_with(
            '<modify_alert alert_id="a1">'
            '<name>lorem</name>'
            '</modify_alert>'
        )

    def test_modify_alert_with_filter_id(self):
        self.gmp.modify_alert(alert_id='a1', filter_id='f1')

        self.connection.send.has_been_called_with(
            '<modify_alert alert_id="a1">' '<filter id="f1"/>' '</modify_alert>'
        )

    def test_modify_alert_invalid_condition(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_alert(
                alert_id='a1',
                condition='bar',
                event='Task run status changed',
                method='Email',
            )

    def test_modify_alert_invalid_event(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_alert(
                alert_id='a1', condition='Always', event='lorem', method='Email'
            )

    def test_modify_alert_invalid_method(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_alert(
                alert_id='a1',
                condition='Always',
                event='Task run status changed',
                method='ipsum',
            )

    def test_modify_alert_with_event_missing_method(self):
        with self.assertRaisesRegex(RequiredArgument, "method is required"):
            self.gmp.modify_alert(
                alert_id='a1',
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                condition=AlertCondition.ALWAYS,
            )

        with self.assertRaisesRegex(RequiredArgument, "method is required"):
            self.gmp.modify_alert(
                alert_id='a1',
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                condition=AlertCondition.ALWAYS,
            )

        with self.assertRaisesRegex(RequiredArgument, "method is required"):
            self.gmp.modify_alert(
                alert_id='a1',
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                condition=AlertCondition.ALWAYS,
            )

    def test_modify_alert_with_event_missing_condition(self):
        with self.assertRaisesRegex(RequiredArgument, "condition is required"):
            self.gmp.modify_alert(
                alert_id='a1',
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.SCP,
            )

        with self.assertRaisesRegex(RequiredArgument, "condition is required"):
            self.gmp.modify_alert(
                alert_id='a1',
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.SCP,
            )

        with self.assertRaisesRegex(RequiredArgument, "condition is required"):
            self.gmp.modify_alert(
                alert_id='a1',
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.SCP,
            )

    def test_modify_alert_invalid_condition_for_secinfo(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_alert(
                alert_id='a1',
                condition='Severity at least',
                event='Updated SecInfo arrived',
                method='Email',
            )

    def test_modify_alert_invalid_method_for_secinfo(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_alert(
                alert_id='a1',
                condition='Always',
                event='Updated SecInfo arrived',
                method='HTTP Get',
            )

    def test_modify_alert_with_event_data(self):
        self.gmp.modify_alert(
            alert_id='a1',
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            event_data={'foo': 'bar'},
        )

        self.connection.send.has_been_called_with(
            '<modify_alert alert_id="a1">'
            '<condition>Always</condition>'
            '<method>Email</method>'
            '<event>Task run status changed'
            '<data>bar<name>foo</name></data>'
            '</event>'
            '</modify_alert>'
        )

    def test_modify_alert_with_condition_data(self):
        self.gmp.modify_alert(
            alert_id='a1',
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            condition_data={'foo': 'bar'},
        )

        self.connection.send.has_been_called_with(
            '<modify_alert alert_id="a1">'
            '<condition>Always<data>bar<name>foo</name></data></condition>'
            '<method>Email</method>'
            '<event>Task run status changed</event>'
            '</modify_alert>'
        )

    def test_modify_alert_with_method_data(self):
        self.gmp.modify_alert(
            alert_id='a1',
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            method_data={'foo': 'bar'},
        )

        self.connection.send.has_been_called_with(
            '<modify_alert alert_id="a1">'
            '<condition>Always</condition>'
            '<method>Email<data>bar<name>foo</name></data></method>'
            '<event>Task run status changed</event>'
            '</modify_alert>'
        )


if __name__ == '__main__':
    unittest.main()
