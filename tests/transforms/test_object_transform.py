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

from gvm.transforms import ObjectTransform
from gvm.transforms.object.responses import (
    Response,
    AuthenticateResponse,
    StartTaskResponse,
    CreateTaskResponse,
    GetTasksResponse,
    GetPortListsResponse,
)

from gvm.transforms.object.port_classes import PortList, PortCount, PortRange
from gvm.transforms.object.user_classes import (
    Role,
    Owner,
    Permission,
    Observers,
    Group,
    UserTags,
    Tag,
)
from gvm.transforms.object.task_classes import Task, Schedule
from gvm.transforms.object.count_classes import ReportCount


FILEPATH = os.path.dirname(os.path.realpath(__file__)) + '/test_xml/'


def get_root_from_file(file_name: str):

    root = ''
    with open(FILEPATH + file_name, 'r') as file:
        root = file.read().replace('\n', '')
        root = root.replace('\t', '')
    return root


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

        root = get_root_from_file("test_authenticate.xml")

        response = transform(root, None)

        self.assertIsInstance(response, AuthenticateResponse)
        self.assertIsInstance(response.role, Role)
        self.assertEqual(response.role.name, 'Test')
        self.assertEqual(response.timezone, 'UTC')
        self.assertEqual(response.severity, 'nist')


class ObjectTransformPortClassesTestCase(unittest.TestCase):

    # This tests also PortRange and Permission,
    # because they are part of the get_port_lists_response
    def test_get_port_list(self):
        transform = ObjectTransform()

        root = get_root_from_file("test_get_port_list.xml")
        permissions = [
            Permission("Test_Permission1"),
            Permission("Test_Permission2"),
        ]
        port_count = PortCount(3, 2, 1)
        port_ranges = []
        port_ranges.append(
            PortRange(
                "1fa9476e-ba37-4d99-a7fa-90d912250c47",
                1,
                80,
                "tcp",
                "TestComment1",
            )
        )
        port_ranges.append(
            PortRange(
                "5d203ed9-35ac-48c2-a850-5f9de31af411",
                82,
                113,
                "tcp",
                "TestComment2",
            )
        )

        port_list = PortList(
            "33d0cd82-57c6-11e1-8ed1-406186ea4fc5",
            Owner("Test_name"),
            "All IANA assigned TCP 2012-02-10",
            "TestComment",
            datetime.datetime(2020, 3, 2, 10, 48, 37),
            datetime.datetime(2020, 3, 2, 10, 48, 37),
            False,
            True,
            permissions,
            port_count,
            port_ranges,
        )

        response = transform(root, None)

        self.assertIsInstance(response, GetPortListsResponse)
        self.assertEqual(response.port_lists, port_list)


"""
class ObjectTransformScanClassesTestCase(unittest.TestCase):

    def test_get_config(self):
        transform = ObjectTransform()

        root = get_root_from_file("test_get_config.xml")
"""


class ObjectTransformTaskTestCase(unittest.TestCase):
    def test_get_task(self):
        transform = ObjectTransform()

        root = get_root_from_file("test_get_task.xml")

        response = transform(root, None)
        permissions = []
        permissions.append(Permission("Test1"))
        permissions.append(Permission("Test2"))

        users = ["admin", "admin_Clone_4"]
        groups = Group(
            None,
            "44ff149f-8817-4419-9d5c-b6c3a8655ab2",
            None,
            "plebeians",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )

        observers = Observers(users, groups)

        user_tags = UserTags(
            1, Tag("6e6f1411-c2ba-4fe6-99bf-470dc67ccade", None, None, None)
        )

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
            user_tags,
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
            observers,
            None,
            False,
            None,
            None,
            None,
            None,
            None,
        )

        self.assertIsInstance(response, GetTasksResponse)
        self.assertEqual(response.tasks, task)

    def test_create_task(self):
        transform = ObjectTransform()

        root = get_root_from_file("test_create_task.xml")

        response = transform(root, None)

        self.assertIsInstance(response, CreateTaskResponse)
        self.assertEqual(response.status, "201")
        self.assertEqual(response.status_text, "OK, resource created")
        self.assertEqual(
            response.task_id, "4a8db8ee-0c42-452d-bf64-64e735a71b87"
        )

    def test_start_task(self):
        transform = ObjectTransform()

        root = get_root_from_file("test_start_task.xml")

        response = transform(root, None)

        self.assertIsInstance(response, StartTaskResponse)
        self.assertEqual(
            response.report_id, "9cdadab8-d28e-4a29-a2b7-bd63380515e3"
        )


if __name__ == "__main__":
    unittest.main()
