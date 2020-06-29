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
from gvm.transforms.object.scan_classes import Scanner
from gvm.transforms.object.task_classes import (
    Task,
    Schedule,
    ScanConfig,
    Preference,
    Nvt,
    TaskScanConfig,
    Severity,
    Report,
    ReportTask,
)
from gvm.transforms.object.count_classes import (
    ReportCount,
    FamilyCount,
    NvtCount,
)


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

    # This tests also PortRange, PortCount and Permission,
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


class ObjectTransformScanClassesTestCase(unittest.TestCase):
    def test_get_scanners(self):
        transform = ObjectTransform()

        root = get_root_from_file("test_get_scanners.xml")
        permissions = [Permission("get_scanners"), Permission("get_scanners")]
        scanner_mock1 = Scanner(
            uuid="6acd0832-df90-11e4-b9d5-28d24461215b",
            owner=None,
            name="CVE",
            comment=None,
            creation_time=datetime.datetime(2020, 3, 2, 10, 48, 37),
            modification_time=datetime.datetime(2020, 3, 2, 10, 48, 37),
            writable=True,
            in_use=False,
            permissions=permissions,
            port=0,
            scanner_type=3,
            trash=None,
            all_info_loaded=False,
        )

        scanner_mock2 = Scanner(
            uuid="08b69003-5fc2-4037-a479-93b440211c73",
            owner=None,
            name="OpenVAS Default",
            comment=None,
            creation_time=datetime.datetime(2020, 3, 2, 10, 48, 37),
            modification_time=datetime.datetime(2020, 3, 2, 10, 48, 39),
            writable=True,
            in_use=True,
            permissions=permissions,
            port=0,
            scanner_type=2,
            trash=None,
            all_info_loaded=False,
        )

        scanners = [scanner_mock1, scanner_mock2]

        response = transform(root)

        self.assertEqual(response.scanners, scanners)

    def test_get_configs(self):
        """
        This tests also Preferences,
        because they are part of the get_configs_response
        """
        transform = ObjectTransform()

        root = get_root_from_file("test_get_configs.xml")
        permissions = [Permission("get_configs"), Permission("get_configs")]

        preference_mock1 = Preference(
            nvt=Nvt("1.3.6.1.4.1.25623.1.0.100151", "PostgreSQL Detection"),
            preference_id=1,
            hr_name="Postgres Username:",
            name="Postgres Username:",
            preference_type="entry",
            value="postgres",
            alternatives=None,
            default="postgres",
        )

        preference_mock2 = Preference(
            nvt=Nvt("1.3.6.1.4.1.25623.1.0.97001", "PCI-DSS Version 2.0"),
            preference_id=1,
            hr_name="Berichtformat/Report Format",
            name="Berichtformat/Report Format",
            preference_type="radio",
            value="Text",
            alternatives=[
                "Tabellarisch/Tabular",
                "Text und/and Tabellarisch/Tabular",
            ],
            default="Text",
        )

        preferences = [preference_mock1, preference_mock2]

        config_mock1 = ScanConfig(
            uuid="d21f6c81-2b88-4ac1-b7b4-a2a9f2ad4663",
            owner=None,
            name="Base",
            comment="Basic configuration template.",
            creation_time=datetime.datetime(2020, 3, 2, 10, 48, 37),
            modification_time=datetime.datetime(2020, 3, 2, 10, 48, 37),
            writable=False,
            in_use=False,
            permissions=permissions,
            family_count=FamilyCount(2, False),
            nvt_count=NvtCount(3, False),
            config_type=0,
            usage_type="scan",
            max_nvt_count=None,
            known_nvt_count=None,
            scanner=None,
            user_tags=None,
            tasks=None,
            preferences=None,
            trash=None,
            all_info_loaded=False,
        )

        config_mock2 = ScanConfig(
            uuid="8715c877-47a0-438d-98a3-27c7a6ab2196",
            owner=Owner("TestName"),
            name="Discovery",
            comment="Network Discovery scan configuration.",
            creation_time=datetime.datetime(2020, 3, 2, 10, 48, 37),
            modification_time=datetime.datetime(2020, 3, 2, 10, 48, 37),
            writable=False,
            in_use=True,
            permissions=permissions,
            family_count=FamilyCount(16, False),
            nvt_count=NvtCount(3023, True),
            config_type=0,
            usage_type="scan",
            max_nvt_count=239,
            known_nvt_count=3,
            scanner=None,
            user_tags=None,
            tasks=None,
            preferences=preferences,
            trash=None,
            all_info_loaded=False,
        )
        scan_configs = [config_mock1, config_mock2]
        response = transform(root)

        self.assertEqual(response.scan_configs, scan_configs)


class ObjectTransformCountClassesTestCase(unittest.TestCase):
    def test_resolve_family_count(self):
        family_count1 = FamilyCount.resolve_family_count(None)
        xml = "<family_count>2<growing>0</growing></family_count>"
        parser = etree.XMLParser(encoding="utf-8", recover=True, huge_tree=True)

        root = etree.XML(xml, parser)

        family_count_mock = FamilyCount(2, False)
        family_count2 = FamilyCount.resolve_family_count(root)

        self.assertEqual(family_count1, None)
        self.assertEqual(family_count2, family_count_mock)

    def test_resolve_nvt_count(self):
        nvt_count1 = NvtCount.resolve_nvt_count(None)
        xml = "<nvt_count>5<growing>1</growing></nvt_count>"
        parser = etree.XMLParser(encoding="utf-8", recover=True, huge_tree=True)

        root = etree.XML(xml, parser)

        nvt_count_mock = NvtCount(5, True)
        nvt_count2 = NvtCount.resolve_nvt_count(root)

        self.assertEqual(nvt_count1, None)
        self.assertEqual(nvt_count2, nvt_count_mock)


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

        task_scan_config_mock = TaskScanConfig(
            "8715c877-47a0-438d-98a3-27c7a6ab2196", False, False
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
            task_scan_config_mock,
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

    def test_resolve_severity(self):
        xml = (
            "<severity>"
            "<full>-99.0</full>"
            "<filtered>10.0</filtered>"
            "</severity>"
        )
        parser = etree.XMLParser(encoding="utf-8", recover=True, huge_tree=True)

        root = etree.XML(xml, parser)
        severity_mock = Severity(float(-99.0), float(10.0))
        response = Severity.resolve_severity(root)

        self.assertEqual(response, severity_mock)

    def test_get_reports(self):
        transform = ObjectTransform()

        root = get_root_from_file("test_get_reports.xml")

        report_mock1 = Report(
            gmp=None,
            uuid="c96b26fb-22df-4a79-9d20-c579a5fa5533",
            format_id="",
            extension="",
            content_type="application/xml",
            owner=Owner("admin"),
            name="2020-03-03T10:05:42Z",
            comment="Test Comment",
            creation_time=datetime.datetime(2020, 3, 3, 10, 5, 42),
            modification_time=datetime.datetime(2020, 3, 3, 10, 6, 22),
            writable=False,
            in_use=False,
            gmp_version="9.0",
            scan_run_status="Done",
            timestamp=datetime.datetime(2020, 3, 3, 10, 5, 26),
            scan_start=datetime.datetime(2020, 3, 3, 10, 5, 42),
            scan_end=datetime.datetime(2020, 3, 3, 10, 6, 22),
            timezone="Coordinated Universal Time",
            timezone_abbrev="UTC",
            severity=Severity(float(-99.0), float(-99.0)),
            all_info_loaded=False,
            _task=ReportTask("1e9844ab-9918-44db-b7d8-9bc32c0b1cee", False),
        )

        report_mock2 = Report(
            gmp=None,
            uuid="0f7c7734-e33c-45ef-a9e4-f624e39312cf",
            format_id="Test_ID",
            extension="Test_EXT",
            content_type="application/xml",
            owner=Owner("admin"),
            name="2020-03-03T10:38:05Z",
            comment=None,
            creation_time=datetime.datetime(2020, 3, 3, 10, 38, 5),
            modification_time=datetime.datetime(2020, 3, 3, 10, 39, 47),
            writable=False,
            in_use=True,
            gmp_version="9.0",
            scan_run_status="Done",
            timestamp=datetime.datetime(2020, 3, 3, 10, 37, 49),
            scan_start=datetime.datetime(2020, 3, 3, 10, 38, 5),
            scan_end=datetime.datetime(2020, 3, 3, 10, 39, 47),
            timezone="Coordinated Universal Time",
            timezone_abbrev="UTC",
            severity=Severity(float(0.0), float(0.0)),
            all_info_loaded=False,
            _task=ReportTask("a16aec9e-9c53-4fde-b42f-3c20311c0afc", False),
        )

        reports = [report_mock1, report_mock2]

        response = transform(root)

        self.assertEqual(response.reports, reports)


if __name__ == "__main__":
    unittest.main()
