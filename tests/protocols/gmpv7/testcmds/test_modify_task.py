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

from collections import OrderedDict

from gvm.errors import RequiredArgument, InvalidArgument, InvalidArgumentType

from gvm.protocols.gmpv7 import HostsOrdering


class GmpModifyTaskCommandTestCase:
    def test_modify_task(self):
        self.gmp.modify_task('t1')

        self.connection.send.has_been_called_with('<modify_task task_id="t1"/>')

    def test_modify_task_missing_task_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_task(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_task('')

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_task(task_id='')

    def test_modify_task_with_name(self):
        self.gmp.modify_task(task_id='t1', name='foo')

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">' '<name>foo</name>' '</modify_task>'
        )

    def test_modify_task_with_config_id(self):
        self.gmp.modify_task(task_id='t1', config_id='c1')

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">' '<config id="c1"/>' '</modify_task>'
        )

    def test_modify_task_with_target_id(self):
        self.gmp.modify_task(task_id='t1', target_id='t1')

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">' '<target id="t1"/>' '</modify_task>'
        )

    def test_modify_task_with_scanner_id(self):
        self.gmp.modify_task(task_id='t1', scanner_id='s1')

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">' '<scanner id="s1"/>' '</modify_task>'
        )

    def test_modify_task_with_schedule_id(self):
        self.gmp.modify_task(task_id='t1', schedule_id='s1')

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">' '<schedule id="s1"/>' '</modify_task>'
        )

    def test_modify_task_with_comment(self):
        self.gmp.modify_task(task_id='t1', comment='bar')

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">'
            '<comment>bar</comment>'
            '</modify_task>'
        )

    def test_modify_task_with_alerts_ids(self):
        self.gmp.modify_task(task_id='t1', alert_ids=['a1', 'a2', 'a3'])

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">'
            '<alert id="a1"/>'
            '<alert id="a2"/>'
            '<alert id="a3"/>'
            '</modify_task>'
        )

    def test_modify_task_invalid_alerts_ids(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_task(task_id='t1', alert_ids='')

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_task(task_id='t1', alert_ids='a1')

    def test_modify_task_with_empty_alert_ids(self):
        self.gmp.modify_task(task_id='t1', alert_ids=[])

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">' '<alert id="0"/>' '</modify_task>'
        )

    def test_modify_task_with_alterable(self):
        self.gmp.modify_task(task_id='t1', alterable=True)

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">'
            '<alterable>1</alterable>'
            '</modify_task>'
        )

        self.gmp.modify_task(task_id='t1', alterable=False)

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">'
            '<alterable>0</alterable>'
            '</modify_task>'
        )

    def test_modify_task_with_hosts_ordering(self):
        self.gmp.modify_task(task_id='t1', hosts_ordering=HostsOrdering.REVERSE)

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">'
            '<hosts_ordering>reverse</hosts_ordering>'
            '</modify_task>'
        )

    def test_modify_task_invalid_hosts_ordering(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_task(task_id='t1', hosts_ordering='foo')

    def test_modify_task_with_schedule(self):
        self.gmp.modify_task(task_id='t1', schedule_id='s1')

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">' '<schedule id="s1"/>' '</modify_task>'
        )

    def test_modify_task_with_schedule_periods(self):
        self.gmp.modify_task(task_id='t1', schedule_periods=0)

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">'
            '<schedule_periods>0</schedule_periods>'
            '</modify_task>'
        )

        self.gmp.modify_task(task_id='t1', schedule_periods=5)

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">'
            '<schedule_periods>5</schedule_periods>'
            '</modify_task>'
        )

    def test_modify_task_invalid_schedule_periods(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_task(task_id='t1', schedule_periods='foo')

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_task(task_id='t1', schedule_periods=-1)

    def test_modify_task_with_observers(self):
        self.gmp.modify_task(task_id='t1', observers=['u1', 'u2'])

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">'
            '<observers>u1,u2</observers>'
            '</modify_task>'
        )

    def test_modify_task_invalid_observers(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_task(task_id='t1', observers='')

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_task(task_id='t1', observers='foo')

    def test_modify_task_with_preferences(self):
        self.gmp.modify_task(
            task_id='t1',
            preferences=OrderedDict([('foo', 'bar'), ('lorem', 'ipsum')]),
        )

        self.connection.send.has_been_called_with(
            '<modify_task task_id="t1">'
            '<preferences>'
            '<preference>'
            '<scanner_name>foo</scanner_name>'
            '<value>bar</value>'
            '</preference>'
            '<preference>'
            '<scanner_name>lorem</scanner_name>'
            '<value>ipsum</value>'
            '</preference>'
            '</preferences>'
            '</modify_task>'
        )

    def test_modify_task_invalid_preferences(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_task(task_id='t1', preferences='')

        with self.assertRaises(InvalidArgumentType):
            self.gmp.modify_task(task_id='t1', preferences=['foo', 'bar'])


if __name__ == '__main__':
    unittest.main()
