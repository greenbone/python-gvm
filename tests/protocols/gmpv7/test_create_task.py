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

    TASK_NAME = "important task"
    CONFIG_ID = "cd0641e7-40b8-4e2c-811e-6b39d6d4b904"
    TARGET_ID = '267a3405-e84a-47da-97b2-5fa0d2e8995e'
    SCANNER_ID = 'b64c81b2-b9de-11e3-a2e9-406186ea4fc5'
    ALERT_IDS = ['3ab38c6a-30ac-407a-98db-ad6e74c98b9a',]
    COMMENT = 'this task has been created for test purposes'

    def setUp(self):
        self.connection = MockConnection()
        self.gmp = Gmp(self.connection)

    def test_without_alert_correct_cmd(self):
        self.gmp.create_task(
            self.TASK_NAME, self.CONFIG_ID, self.TARGET_ID, self.SCANNER_ID,
            comment=self.COMMENT)

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>{0}</name>'
            '<config id="{2}"/><target id="{3}"/><scanner id="{4}"/>'
            '<comment>{1}</comment>'
            '</create_task>'.format(self.TASK_NAME, self.COMMENT,
                                    self.CONFIG_ID, self.TARGET_ID,
                                    self.SCANNER_ID)
        )

    def test_single_alert(self):
        self.gmp.create_task(
            self.TASK_NAME, self.CONFIG_ID, self.TARGET_ID, self.SCANNER_ID,
            alert_ids=self.ALERT_IDS)

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>{task}</name>'
            '<config id="{config}"/>'
            '<target id="{target}"/>'
            '<scanner id="{scanner}"/>'
            '<alert id="{alert}"/>'
            '</create_task>'.format(
                task=self.TASK_NAME, config=self.CONFIG_ID,
                target=self.TARGET_ID, scanner=self.SCANNER_ID,
                alert=self.ALERT_IDS[0])
        )

    def test_multiple_alerts(self):
        alert_id2 = 'fb3d6f82-d706-4f99-9e53-d7d85257e25f'
        alert_id3 = 'a33864a9-d3fd-44b3-8717-972bfb01dfcf'
        alert_ids = self.ALERT_IDS[:]
        alert_ids.extend([alert_id2, alert_id3])

        self.gmp.create_task(
            self.TASK_NAME, self.CONFIG_ID, self.TARGET_ID, self.SCANNER_ID,
            alert_ids=alert_ids)

        self.connection.send.has_been_called_with(
            '<create_task>'
            '<name>{task}</name>'
            '<config id="{config}"/>'
            '<target id="{target}"/>'
            '<scanner id="{scanner}"/>'
            '<alert id="{alert1}"/>'
            '<alert id="{alert2}"/>'
            '<alert id="{alert3}"/>'
            '</create_task>'.format(
                task=self.TASK_NAME, config=self.CONFIG_ID,
                target=self.TARGET_ID, scanner=self.SCANNER_ID,
                alert1=alert_ids[0],
                alert2=alert_ids[1],
                alert3=alert_ids[2])
        )


if __name__ == '__main__':
    unittest.main()
