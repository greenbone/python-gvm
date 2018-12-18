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

from gvm.protocols.gmpv7 import Gmp

from .. import MockConnection


class GMPCreateTaskCommandTestCase(unittest.TestCase):

    def setUp(self):
        self.connection = MockConnection()
        self.gmp = Gmp(self.connection)

    def test_create_task(self):
        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '</create_task>'
        )

    def test_create_task_single_alert(self):
        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            alert_ids=['a1'],
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<alert id="a1"/>'
            '</create_task>'
        )

    def test_create_task_multiple_alerts(self):
        self.gmp.create_task(
            name='foo',
            config_id='c1',
            target_id='t1',
            scanner_id='s1',
            alert_ids=['a1', 'a2', 'a3'],
        )

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>foo</name>'
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<alert id="a1"/>'
            '<alert id="a2"/>'
            '<alert id="a3"/>'
            '</create_task>'
        )


if __name__ == '__main__':
    unittest.main()
