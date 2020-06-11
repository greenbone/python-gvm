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
import os
import datetime

from lxml import etree

from gvm.transform import ObjectTransform
from gvm.transform.object.responses import Response, AuthenticateResponse

from gvm.transform.object.classes import (
    Role,
    Task,
    Owner,
    Permission,
    ReportCount,
    Schedule,
)

FILEPATH = os.path.dirname(os.path.realpath(__file__)) + '/test_xml/'


class ObjectTransformAuthenticateTestCase(unittest.TestCase):
    def test_reponse_status(self):

        xml = '<test_response status="200" status_text="test"></test_response>'
        parser = etree.XMLParser(encoding="utf-8", recover=True, huge_tree=True)

        root = etree.XML(xml, parser)
        response = Response(root)

        self.assertEqual(response.status, '200')
        self.assertEqual(response.status_text, 'test')
        self.assertEqual(response.response_name, 'test_response')

    def test_authenticate(self):

        transform = ObjectTransform()

        root = ''
        with open(FILEPATH + 'test_authenticate.xml', 'r') as file:
            root = file.read().replace('\n', '')

        response = transform(root)

        self.assertIsInstance(response, AuthenticateResponse)
        self.assertIsInstance(response.role, Role)
        self.assertEqual(response.role.name, 'Test')
        self.assertEqual(response.timezone, 'UTC')
        self.assertEqual(response.severity, 'nist')


class ObjectTransformGetTaskTestCase(unittest.TestCase):
    def test_get_task(self):
        transform = ObjectTransform()

        root = ''
        with open(FILEPATH + 'test_get_task.xml', 'r') as file:
            root = file.read().replace('\n', '')
            root = root.replace('\t', '')

        response = transform(root)
        permissions = []
        permissions.append(Permission("Test1"))
        permissions.append(Permission("Test2"))

        task = Task(
            None,
            "c6415957-984c-40ba-9906-db6e3390c82d",
            Owner("admin"),
            "Discovery",
            "Test Comment",
            datetime.datetime(2020, 3, 5, 15, 35, 21),
            datetime.datetime(2020, 3, 5, 15, 35, 21),
            True,
            False,
            permissions,
            # user_tags,
            False,
            "scan",
            "Test Ordering",
            # alert,
            "Done",
            -1,
            ReportCount(1, 1),
            "Test Trend",
            Schedule("Test Schedule", "over", False),
            0,
            None,
            None,
            False,
            None,
            None,
            None,
            None,
            None,
        )

        self.assertEqual(response.tasks, task)


if __name__ == "__main__":
    unittest.main()
