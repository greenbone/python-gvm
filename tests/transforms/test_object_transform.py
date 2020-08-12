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
from unittest.mock import patch

from lxml import etree

from gvm.transforms.object.responses import GetReportsResponse
from gvm.transforms import ObjectTransform
from gvm.transforms.object.responses import (
    AuthenticateResponse,
    CreateTaskResponse,
    GetConfigsResponse,
    GetPortListsResponse,
    GetScannersResponse,
    GetTargetsResponse,
    GetTasksResponse,
    Response,
    StartTaskResponse,
    StopTaskResponse,
    GetUsersResponse,
)

from gvm.transforms.object.port_classes import PortList, PortCount, PortRange
from gvm.transforms.object.user_classes import (
    Role,
    User,
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
    Target,
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
    ResultCount,
    ResultCounter,
)


FILEPATH = os.path.dirname(os.path.realpath(__file__)) + '/test_xml/'


def get_root_from_file(file_name: str):

    root = ''
    with open(FILEPATH + file_name, 'r') as file:
        root = file.read().replace('\n', '')
        root = root.replace('\t', '')
    return root


class ObjectTransformTestCase(unittest.TestCase):
    def test_key_error(self):
        transform = ObjectTransform()
        response = transform(
            '<no_valid_response status="200" status_text="OK"/>'
        )
        self.assertEqual(response, None)


class ObjectTransformAuthenticateTestCase(unittest.TestCase):
    def test_reponse_status(self):

        xml = '<test_response status="200" status_text="test"></test_response>'
        parser = etree.XMLParser(encoding="utf-8", recover=True, huge_tree=True)

        root = etree.XML(xml, parser)
        response = Response(root)

        self.assertEqual(response.status, 200)
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


class ObjectTransformUserClassesTestCase(unittest.TestCase):
    def test_get_users(self):
        transform = ObjectTransform()
        root = get_root_from_file("test_get_users.xml")

        groups = [
            Group(
                uuid="62d425f1-41af-4b62-b6a8-ea0201490eab", name="TestGruppe1"
            ),
            Group(
                uuid="62d425f1-41af-4b62-b6a8-ea0201490ebb", name="TestGruppe2"
            ),
        ]

        user_expected1 = User(
            uuid="d6dcf91b-e9cf-4700-9d33-34c92ce1c3c8",
            owner=None,
            name="admin",
            comment="comment",
            creation_time=datetime.datetime(2020, 6, 4, 9, 57, 37),
            modification_time=datetime.datetime(2020, 6, 4, 9, 57, 37),
            writable=True,
            in_use=False,
            groups=groups,
            permissions=Permission(name="get_users"),
            user_tags=None,
        )

        user_expected2 = User(
            uuid="ec3266fd-1a35-40db-ab5a-794de9060e04",
            owner=Owner(name="admin"),
            name="TestUser",
            comment="Tester",
            creation_time=datetime.datetime(2020, 6, 4, 14, 35, 20),
            modification_time=datetime.datetime(2020, 6, 4, 14, 35, 20),
            writable=True,
            in_use=False,
            groups=groups,
            permissions=Permission(name="Everything"),
            user_tags=UserTags(count=1, tags=[]),
        )

        users_expected = [user_expected1, user_expected2]

        response = transform(root)

        self.assertIsInstance(response, GetUsersResponse)
        self.assertEqual(response.users, users_expected)


class ObjectTransformScanClassesTestCase(unittest.TestCase):
    def test_get_scanners(self):
        transform = ObjectTransform()

        root = get_root_from_file("test_get_scanners.xml")
        permissions = [Permission("get_scanners"), Permission("get_scanners")]
        scanner_expected1 = Scanner(
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

        scanner_expected2 = Scanner(
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

        scanners = [scanner_expected1, scanner_expected2]

        response = transform(root)

        self.assertEqual(response.scanners, scanners)

    def test_get_targets(self):
        transform = ObjectTransform()

        root = get_root_from_file("test_get_targets.xml")

        permissions = Permission("Everything")

        target_expected1 = Target(
            gmp=None,
            uuid="f8fac1da-de4f-461a-b4cc-7aff71734ec7",
            owner=Owner("admin"),
            name="Test target",
            comment="Test comment",
            creation_time=datetime.datetime(2020, 3, 3, 10, 5, 26),
            modification_time=datetime.datetime(2020, 3, 3, 10, 5, 26),
            writable=True,
            in_use=True,
            permissions=permissions,
            reverse_lookup_only=False,
            reverse_lookup_unify=False,
            trash=None,
            all_info_loaded=False,
            _port_list=None,
        )

        target_expected2 = Target(
            gmp=None,
            uuid="7d27b6b7-b9ec-4543-9620-6e39c74a0c57",
            owner=Owner("admin"),
            name="Target for Test - 2020-03-03 10:37:49",
            comment="Automatically generated by wizard",
            creation_time=datetime.datetime(2020, 3, 3, 10, 37, 49),
            modification_time=datetime.datetime(2020, 3, 3, 10, 37, 49),
            writable=True,
            in_use=True,
            permissions=permissions,
            reverse_lookup_only=False,
            reverse_lookup_unify=False,
            trash=None,
            all_info_loaded=False,
            _port_list=None,
        )

        targets = [target_expected1, target_expected2]
        response = transform(root)

        self.assertEqual(response.targets, targets)

    def test_get_configs(self):
        """
        This tests also Preferences,
        because they are part of the get_configs_response
        """
        transform = ObjectTransform()

        root = get_root_from_file("test_get_configs.xml")
        permissions = [Permission("get_configs"), Permission("get_configs")]

        preference_expected1 = Preference(
            nvt=Nvt("1.3.6.1.4.1.25623.1.0.100151", "PostgreSQL Detection"),
            preference_id=1,
            hr_name="Postgres Username:",
            name="Postgres Username:",
            preference_type="entry",
            value="postgres",
            alternatives=None,
            default="postgres",
        )

        preference_expected2 = Preference(
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

        preferences = [preference_expected1, preference_expected2]

        config_expected1 = ScanConfig(
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

        config_expected2 = ScanConfig(
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
        scan_configs = [config_expected1, config_expected2]
        response = transform(root)

        self.assertEqual(response.scan_configs, scan_configs)


class ObjectTransformCountClassesTestCase(unittest.TestCase):
    def test_resolve_family_count(self):
        family_count1 = FamilyCount.resolve_family_count(None)
        xml = "<family_count>2<growing>0</growing></family_count>"
        parser = etree.XMLParser(encoding="utf-8", recover=True, huge_tree=True)

        root = etree.XML(xml, parser)

        family_count_expected = FamilyCount(2, False)
        family_count2 = FamilyCount.resolve_family_count(root)

        self.assertEqual(family_count1, None)
        self.assertEqual(family_count2, family_count_expected)

    def test_resolve_nvt_count(self):
        nvt_count1 = NvtCount.resolve_nvt_count(None)
        xml = "<nvt_count>5<growing>1</growing></nvt_count>"
        parser = etree.XMLParser(encoding="utf-8", recover=True, huge_tree=True)

        root = etree.XML(xml, parser)

        nvt_count_expected = NvtCount(5, True)
        nvt_count2 = NvtCount.resolve_nvt_count(root)

        self.assertEqual(nvt_count1, None)
        self.assertEqual(nvt_count2, nvt_count_expected)


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

        task_scan_config_expected = TaskScanConfig(
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
            task_scan_config_expected,
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
        self.assertEqual(response.status, 201)
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

    def test_stop_task(self):
        transform = ObjectTransform()

        xml = '<stop_task_response status="200" status_text="OK"/>'

        response = transform(xml)
        self.assertIsInstance(response, StopTaskResponse)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.status_text, "OK")

    def test_resolve_severity(self):
        xml = (
            "<severity>"
            "<full>-99.0</full>"
            "<filtered>10.0</filtered>"
            "</severity>"
        )
        parser = etree.XMLParser(encoding="utf-8", recover=True, huge_tree=True)

        root = etree.XML(xml, parser)
        severity_expected = Severity(float(-99.0), float(10.0))
        response = Severity.resolve_severity(root)

        self.assertEqual(response, severity_expected)

    def test_get_reports(self):
        transform = ObjectTransform()

        root = get_root_from_file("test_get_reports.xml")

        debug = ResultCounter(0, 0)
        hole = ResultCounter(0, 0)
        info = ResultCounter(0, 0)
        log = ResultCounter(0, 0)
        log2 = ResultCounter(5, 5)
        warning = ResultCounter(0, 0)
        false_positiv = ResultCounter(0, 0)

        report_expected1 = Report(
            gmp=None,
            uuid="c96b26fb-22df-4a79-9d20-c579a5fa5533",
            format_id="",
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
            result_count=ResultCount(
                0, 0, 0, debug, hole, info, log, warning, false_positiv
            ),
            severity=Severity(float(-99.0), float(-99.0)),
            all_info_loaded=False,
            _task=ReportTask("1e9844ab-9918-44db-b7d8-9bc32c0b1cee", False),
        )

        report_expected2 = Report(
            gmp=None,
            uuid="0f7c7734-e33c-45ef-a9e4-f624e39312cf",
            format_id="Test_ID",
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
            result_count=ResultCount(
                5, 5, 5, debug, hole, info, log2, warning, false_positiv
            ),
            severity=Severity(float(0.0), float(0.0)),
            all_info_loaded=False,
            _task=ReportTask("a16aec9e-9c53-4fde-b42f-3c20311c0afc", False),
        )

        reports = [report_expected1, report_expected2]

        response = transform(root)

        self.assertEqual(response.reports, reports)

    def test_task_load_current_report(self):
        with patch('gvm.protocols.gmpv9.Gmp') as gmp_mock:
            xml = get_root_from_file("test_get_report.xml")
            parser = etree.XMLParser(
                encoding="utf-8", recover=True, huge_tree=True
            )
            root = etree.XML(xml, parser)

            gmp_mock.get_report.return_value = GetReportsResponse(None, root)

            report_before = Report(
                uuid="c96b26fb-22df-4a79-9d20-c579a5fa5533",
                all_info_loaded=False,
            )

            debug = ResultCounter(0, 0)
            hole = ResultCounter(0, 0)
            info = ResultCounter(0, 0)
            log = ResultCounter(0, 0)
            warning = ResultCounter(0, 0)
            false_positiv = ResultCounter(0, 0)

            report_expected = Report(
                gmp=None,
                uuid="c96b26fb-22df-4a79-9d20-c579a5fa5533",
                format_id="",
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
                result_count=ResultCount(
                    0, 0, 0, debug, hole, info, log, warning, false_positiv
                ),
                severity=Severity(float(-99.0), float(-99.0)),
                all_info_loaded=True,
                _task=ReportTask("1e9844ab-9918-44db-b7d8-9bc32c0b1cee", False),
            )

            task1 = Task(gmp=gmp_mock, _current_report=report_before)
            report_after = task1.current_report
            self.assertEqual(report_after, report_expected)

            task2 = Task()
            report2 = task2.current_report
            self.assertIsNone(report2)

    def test_task_load_last_report(self):
        with patch('gvm.protocols.gmpv9.Gmp') as gmp_mock:
            xml = get_root_from_file("test_get_report.xml")
            parser = etree.XMLParser(
                encoding="utf-8", recover=True, huge_tree=True
            )
            root = etree.XML(xml, parser)
            gmp_mock.get_report.return_value = GetReportsResponse(None, root)

            report_before = Report(
                uuid="c96b26fb-22df-4a79-9d20-c579a5fa5533",
                all_info_loaded=False,
            )

            debug = ResultCounter(0, 0)
            hole = ResultCounter(0, 0)
            info = ResultCounter(0, 0)
            log = ResultCounter(0, 0)
            warning = ResultCounter(0, 0)
            false_positiv = ResultCounter(0, 0)

            report_expected = Report(
                gmp=None,
                uuid="c96b26fb-22df-4a79-9d20-c579a5fa5533",
                format_id="",
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
                result_count=ResultCount(
                    0, 0, 0, debug, hole, info, log, warning, false_positiv
                ),
                severity=Severity(float(-99.0), float(-99.0)),
                all_info_loaded=True,
                _task=ReportTask("1e9844ab-9918-44db-b7d8-9bc32c0b1cee", False),
            )

            task1 = Task(gmp=gmp_mock, _last_report=report_before)
            report_after = task1.last_report
            self.assertEqual(report_after, report_expected)

            task2 = Task()
            report2 = task2.last_report
            self.assertIsNone(report2)

    def test_task_load_scan_config(self):
        with patch('gvm.protocols.gmpv9.Gmp') as gmp_mock:
            xml = get_root_from_file("test_get_config.xml")
            parser = etree.XMLParser(
                encoding="utf-8", recover=True, huge_tree=True
            )
            root = etree.XML(xml, parser)
            gmp_mock.get_config.return_value = GetConfigsResponse(None, root)

            scan_config_before = ScanConfig(
                uuid="d21f6c81-2b88-4ac1-b7b4-a2a9f2ad4663",
                all_info_loaded=False,
            )

            scan_config_expected = ScanConfig(
                uuid="d21f6c81-2b88-4ac1-b7b4-a2a9f2ad4663",
                owner=None,
                name="Base",
                comment="Basic configuration template.",
                creation_time=datetime.datetime(2020, 3, 2, 10, 48, 37),
                modification_time=datetime.datetime(2020, 3, 2, 10, 48, 37),
                writable=False,
                in_use=False,
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
                all_info_loaded=True,
            )

            task1 = Task(gmp=gmp_mock, _scan_config=scan_config_before)
            scan_config_after = task1.scan_config
            self.assertEqual(scan_config_after, scan_config_expected)

            task2 = Task()
            scan_config2 = task2.scan_config
            self.assertIsNone(scan_config2)

    def test_task_load_target(self):
        with patch('gvm.protocols.gmpv9.Gmp') as gmp_mock:
            xml = get_root_from_file("test_get_target.xml")
            parser = etree.XMLParser(
                encoding="utf-8", recover=True, huge_tree=True
            )
            root = etree.XML(xml, parser)
            gmp_mock.get_target.return_value = GetTargetsResponse(None, root)

            target_before = Target(
                uuid="f8fac1da-de4f-461a-b4cc-7aff71734ec7",
                all_info_loaded=False,
            )

            target_expected = Target(
                uuid="f8fac1da-de4f-461a-b4cc-7aff71734ec7",
                owner=Owner("admin"),
                name="Test target",
                comment="Test comment",
                creation_time=datetime.datetime(2020, 3, 3, 10, 5, 26),
                modification_time=datetime.datetime(2020, 3, 3, 10, 5, 26),
                writable=True,
                in_use=True,
                reverse_lookup_only=False,
                reverse_lookup_unify=False,
                trash=None,
                all_info_loaded=True,
                _port_list=None,
            )

            task1 = Task(gmp=gmp_mock, _target=target_before)
            target_after = task1.target
            self.assertEqual(target_after, target_expected)

            task2 = Task()
            target2 = task2.target
            self.assertIsNone(target2)

    def test_task_load_scanner(self):
        with patch('gvm.protocols.gmpv9.Gmp') as gmp_mock:
            xml = get_root_from_file("test_get_scanner.xml")
            parser = etree.XMLParser(
                encoding="utf-8", recover=True, huge_tree=True
            )
            root = etree.XML(xml, parser)
            gmp_mock.get_scanner.return_value = GetScannersResponse(None, root)

            scanner_before = Scanner(
                uuid="08b69003-5fc2-4037-a479-93b440211c73",
                all_info_loaded=False,
            )

            scanner_expected = Scanner(
                uuid="08b69003-5fc2-4037-a479-93b440211c73",
                owner=None,
                name="OpenVAS Default",
                comment=None,
                creation_time=datetime.datetime(2020, 3, 2, 10, 48, 37),
                modification_time=datetime.datetime(2020, 3, 2, 10, 48, 39),
                writable=True,
                in_use=True,
                port=0,
                scanner_type=2,
                trash=None,
                all_info_loaded=True,
            )

            task1 = Task(gmp=gmp_mock, _scanner=scanner_before)
            scanner_after = task1.scanner
            self.assertEqual(scanner_after, scanner_expected)

            task2 = Task()
            scanner2 = task2.scanner
            self.assertIsNone(scanner2)


if __name__ == "__main__":
    unittest.main()
