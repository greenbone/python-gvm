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

import datetime
from dataclasses import dataclass
from lxml import etree

# from gvm.protocols.gmp import Gmp

from .utils import (
    get_bool_from_element,
    get_int_from_element,
    get_text_from_element,
    get_datetime_from_element,
    get_text,
    get_int,
)


@dataclass
class Owner:
    name: str

    @staticmethod
    def resolve_owner(root: etree.Element) -> "Owner":
        if root is None:
            return None
        name = root.find('name').text
        if name is None:
            return None
        else:
            return Owner(name)


@dataclass
class User:
    uuid: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    # role
    # groups
    # hosts
    # ifaces
    permissions: list
    # user_tasgs
    # sources

    @staticmethod
    def resolve_users(root: etree.Element) -> list:
        if root is None:
            return None

        users = []

        for child in root:
            if child.tag == "user":
                users.append(User.resolve_user(child))

        return users

    @staticmethod
    def resolve_user(root: etree.Element) -> "User":
        uuid = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = get_text_from_element(root, "name")
        comment = get_text_from_element(root, "comment")
        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")
        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")
        # role
        # groups
        # hosts
        # ifaces
        permissions = Permission.resolve_permissions(root.find("permissions"))
        # user_tasgs
        # sources

        user = User(
            uuid,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            # role,
            # groups,
            # hosts,
            # ifaces,
            permissions,
            # user_tasgs
            # sources
        )

        return user


@dataclass
class Role:
    name: str

    @staticmethod
    def resolve_role(root: etree.Element) -> "Role":
        return Role(root.text)


@dataclass
class PortCount:
    all: int
    tcp: int
    udp: int

    @staticmethod
    def resolve_port_count(root: etree.Element) -> "PortCount":
        if root is None:
            return None
        return PortCount(
            int(root.find("all").text),
            int(root.find("tcp").text),
            int(root.find("udp").text),
        )


@dataclass
class PortRange:
    uuid: str
    start: int
    end: int
    port_range_type: str
    comment: str

    @staticmethod
    def resolve_port_ranges(root: etree.Element) -> list:
        if root is None:
            return None
        port_ranges = []
        for port_range in root:
            port_ranges.append(
                PortRange(
                    port_range.get("id"),
                    int(port_range.find("start").text),
                    int(port_range.find("end").text),
                    port_range.find("type").text,
                    port_range.find("comment").text,
                )
            )
        return port_ranges


@dataclass
class PortList:
    uuid: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    permissions: list
    port_count: PortCount
    port_ranges: list

    @staticmethod
    def resolve_port_list(root: etree.Element) -> "PortList":
        if root is None:
            return None
        uuid = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = get_text_from_element(root, "name")
        comment = get_text_from_element(root, "comment")

        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")

        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")

        permissions = Permission.resolve_permissions(root.find("permissions"))
        port_count = PortCount.resolve_port_count(root.find("port_count"))
        port_ranges = PortRange.resolve_port_ranges(root.find("port_ranges"))

        port_list = PortList(
            uuid,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            permissions,
            port_count,
            port_ranges,
        )
        return port_list

    @staticmethod
    def resolve_port_lists(root: etree.Element):
        result_list = []

        for child in root:
            if child.tag == "port_list":
                port_list = PortList.resolve_port_list(child)
                result_list.append(port_list)

        if len(result_list) == 1:
            return result_list[0]
        else:
            return result_list


@dataclass
class Permission:
    name: str

    @staticmethod
    def resolve_permissions(root: etree.Element) -> list:
        if root is None:
            return None
        permissions = []
        for permission in root:
            permissions.append(Permission(permission.find("name").text))

        if len(permissions) == 1:
            return permissions[0]
        else:
            return permissions


@dataclass
class FamilyCount:
    current: int
    growing: int

    @staticmethod
    def resolve_family_count(root: etree.Element) -> "FamilyCount":
        if root is None:
            return None
        return FamilyCount(
            current=int(root.text), growing=int(root.find("growing").text)
        )


@dataclass
class NvtCount:
    current: int
    growing: int

    @staticmethod
    def resolve_nvt_count(root: etree.Element) -> "NvtCount":
        if root is None:
            return None
        return NvtCount(
            current=int(root.text), growing=int(root.find("growing").text)
        )


@dataclass
class ReportCount:
    current: int
    finished: int

    @staticmethod
    def resolve_report_count(root: etree.Element) -> "ReportCount":
        if root is None:
            return None
        return ReportCount(
            current=get_int(root.text),
            finished=get_int_from_element(root, "finished"),
        )


@dataclass
class Config:
    uuid: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    permissions: list
    family_count: FamilyCount
    nvt_count: NvtCount
    config_type: int
    usage_type: str
    trash: bool
    all_info_loaded: bool

    @staticmethod
    def resolve_configs(root: etree.Element) -> list:
        configs = []
        for child in root:
            if child.tag == "config":
                configs.append(Config.resolve_config(child))

        if len(configs) == 1:
            return configs[0]
        else:
            return configs

    @staticmethod
    def resolve_config(root: etree.Element) -> "Config":
        uuid = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = root.find("name").text
        comment = get_text_from_element(root, "comment")

        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")

        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")

        permissions = Permission.resolve_permissions(root.find("permissions"))
        family_count = FamilyCount.resolve_family_count(
            root.find("family_count")
        )
        nvt_count = NvtCount.resolve_nvt_count(root.find("nvt_count"))
        config_type = get_int_from_element(root, "type")
        usage_type = get_text_from_element(root, "usage_type")

        trash = get_bool_from_element(root, "trash")

        return Config(
            uuid,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            permissions,
            family_count,
            nvt_count,
            config_type,
            usage_type,
            trash,
            False,
        )


@dataclass
class Target:
    gmp: "Gmp"
    uuid: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    permissions: list
    # hosts
    # exclude_hosts
    # ssh_credential
    # smb_credential
    # esxi_credential
    # snmp_credential
    reverse_lookup_only: bool
    reverse_lookup_unify: bool
    # alive_tests: str ?
    trash: bool
    all_info_loaded: bool
    _port_list: PortList

    @staticmethod
    def resolve_targets(root: etree.Element, gmp) -> list:
        targets = []
        for child in root:
            if child.tag == "target":
                targets.append(Target.resolve_target(child, gmp))

        if len(targets) == 1:
            return targets[0]
        else:
            return targets

    @staticmethod
    def resolve_target(root: etree.Element, gmp) -> "Target":
        uuid = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = root.find("name").text
        comment = get_text_from_element(root, "comment")

        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")

        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")

        permissions = Permission.resolve_permissions(root.find("permissions"))
        # hosts
        # exclude_hosts
        port_list = PortList.resolve_port_list(root.find("port_list"))
        # ssh_credential
        # smb_credential
        # esxi_credential
        # snmp_credential

        reverse_lookup_only = get_bool_from_element(root, "reverse_lookup_only")
        reverse_lookup_unify = get_bool_from_element(
            root, "reverse_lookup_unify"
        )

        # alive_tests: str ?
        trash = get_bool_from_element(root, "trash")

        return Target(
            gmp,
            uuid,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            permissions,
            # hosts,
            # exclude_hosts,
            # ssh_credential,
            # smb_credential,
            # esxi_credential,
            # snmp_credential,
            reverse_lookup_only,
            reverse_lookup_unify,
            trash,
            False,
            port_list,
        )

    def load_port_list(self, gmp):
        self._port_list = gmp.get_port_list(self._port_list.uuid).port_lists

    @property
    def port_list(self) -> PortList:
        self.load_port_list(self.gmp)
        return self._port_list

    @port_list.setter
    def port_list(self, port_list: PortList):
        self._port_list = port_list


@dataclass
class Scanner:
    uuid: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    permissions: list
    # hosts
    port: int
    scanner_type: int
    # ca_pub
    # credential
    trash: bool
    all_info_loaded: bool

    @staticmethod
    def resolve_scanners(root: etree.Element) -> list:
        scanners = []

        for child in root:
            if child.tag == "scanner":
                scanners.append(Scanner.resolve_scanner(child))

        if len(scanners) == 1:
            return scanners[0]
        else:
            return scanners

    @staticmethod
    def resolve_scanner(root: etree.Element) -> "Scanner":
        uuid = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = root.find("name").text
        comment = get_text_from_element(root, "comment")

        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")

        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")

        permissions = Permission.resolve_permissions(root.find("permissions"))
        # host
        port = get_int_from_element(root, "port")
        scanner_type = get_int_from_element(root, "type")

        trash = get_bool_from_element(root, "trash")

        scanner = Scanner(
            uuid,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            permissions,
            # host,
            port,
            scanner_type,
            trash,
            False,
        )
        return scanner


@dataclass
class Schedule:
    name: str
    next_time: str
    trash: bool

    @staticmethod
    def resolve_schedule(root: etree.Element) -> "Schedule":
        name = get_text_from_element(root, "name")
        next_time = get_text_from_element(root, "next_time")
        trash = get_bool_from_element(root, "trash")

        schedule = Schedule(name, next_time, trash)
        return schedule


@dataclass
class Nvt:
    oid: str
    name: str

    @staticmethod
    def resolve_nvt(root: etree.Element) -> "Nvt":
        if root is None:
            return None
        oid = root.get("oid")
        name = get_text_from_element(root, "name")

        nvt = Nvt(oid, name)

        return nvt


@dataclass
class Preference:
    nvt: Nvt
    preference_id: int
    hr_name: str
    name: str
    scanner_name: str
    preference_type: str
    value: str
    alternatives: list
    default: str

    @staticmethod
    def resolve_preferences(root: etree.Element) -> list:
        if root is None:
            return None
        preferences = []
        for child in root:
            if child.tag == "preference":
                preferences.append(Preference.resolve_preference(child))
        if len(preferences) == 1:
            return preferences[0]
        return preferences

    @staticmethod
    def resolve_preference(root: etree.Element) -> "Preference":
        nvt = Nvt.resolve_nvt(root.find("nvt"))
        preference_id = get_int_from_element(root, "id")
        hr_name = get_text_from_element(root, "hr_name")
        name = get_text_from_element(root, "name")
        scanner_name = get_text_from_element(root, "scanner_name")
        preference_type = get_text_from_element(root, "type")
        value = get_text_from_element(root, "value")

        alternatives_xml = root.findall("alt")
        alternatives = []
        for alt in alternatives_xml:
            alternatives.append(get_text(alt))

        if len(alternatives) == 0:
            alternatives = None

        default = get_text_from_element(root, "default")

        preference = Preference(
            nvt,
            preference_id,
            hr_name,
            name,
            scanner_name,
            preference_type,
            value,
            alternatives,
            default,
        )

        return preference


@dataclass
class Observers:
    users: list
    # groups: list
    # roles: list

    @staticmethod
    def resolve_observers(root: etree.Element) -> "Observers":
        users = User.resolve_users(root)

        observers = Observers(users)

        return observers


@dataclass
class ReportTask:
    uuid: str
    all_info_loaded: bool


@dataclass
class Report:
    gmp: "Gmp"
    uuid: str
    format_id: str
    extension: str
    content_type: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    gmp_version: str
    # sort
    # filters
    # severity_class
    scan_run_status: str
    # hosts
    # closed_cves
    # vulns
    # os
    # apps
    # ssl_certs
    # scan
    timestamp: datetime.datetime
    scan_start: datetime.datetime
    scan_end: datetime.datetime
    timezone: str
    timezone_abbrev: str
    # result_count
    # severity
    # errors
    all_info_loaded: bool
    _task: "Task"

    @staticmethod
    def resolve_reports(root: etree.Element, gmp):
        reports = []
        for child in root:
            if child.tag == "report":
                reports.append(Report.resolve_report(child, gmp))
        if len(reports) == 1:
            return reports[0]
        return reports

    @staticmethod
    def resolve_report(root: etree.Element, gmp) -> "Report":
        if root is None:
            return None
        uuid = root.get("id")
        format_id = root.get("format_id")
        extension = root.get("extension")
        content_type = root.get("content_type")
        owner = Owner.resolve_owner(root.find("owner"))
        name = get_text_from_element(root, "name")
        comment = get_text_from_element(root, "comment")
        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")
        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")
        task = root.find("task")
        if task is not None:
            task = ReportTask(task.get("id"), False)

        gmp_version = None
        # sort = None
        # filters = None
        # severity_class = None
        scan_run_status = None
        # hosts = None
        # closed_cves = None
        # vulns = None
        # os = None
        # apps = None
        # ssl_certs = None
        # scan  = None
        timestamp = None
        scan_start = None
        scan_end = None
        timezone = None
        timezone_abbrev = None
        # result_count = None
        # severity = None
        # errors = None

        second_level = root.find("report")

        if second_level is not None:
            gmp_version = get_text_from_element(
                second_level.find("gmp"), "version"
            )
            # sort
            # filters
            # severity_class
            scan_run_status = get_text_from_element(
                second_level, "scan_run_status"
            )
            # hosts
            # closed_cves
            # vulns
            # os
            # apps
            # ssl_certs
            # scan
            timestamp = get_datetime_from_element(second_level, "timestamp")
            scan_start = get_datetime_from_element(second_level, "scan_start")
            scan_end = get_datetime_from_element(second_level, "scan_end")
            timezone = get_text_from_element(second_level, "timezone")
            timezone_abbrev = get_text_from_element(
                second_level, "timezone_abbrev"
            )
            # result_count
            # severity
            # errors

        report = Report(
            gmp,
            uuid,
            format_id,
            extension,
            content_type,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            gmp_version,
            # sort,
            # filters,
            # severity_class,
            scan_run_status,
            # hosts,
            # closed_cves,
            # vulns,
            # os,
            # apps,
            # ssl_certs,
            # scan,
            timestamp,
            scan_start,
            scan_end,
            timezone,
            timezone_abbrev,
            # result_count,
            # severity,
            # errors,
            False,
            task,
        )

        return report

    def load_task(self, gmp) -> "Task":
        if self._task.uuid != "":
            if not self._task.all_info_loaded:
                self._task = gmp.get_task(self._task.uuid).tasks
                self._task.all_info_loaded = True

    @property
    def task(self) -> "Task":
        self.load_task(self.gmp)
        return self._task

    @task.setter
    def task(self, task: "Task"):
        self._task = task


@dataclass
class Task:
    gmp: "Gmp"
    uuid: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    permissions: list
    # user_tags
    alterable: bool
    usage_type: str
    hosts_ordering: str

    # alert
    status: str
    progress: int
    report_count: ReportCount
    trend: str
    schedule: Schedule
    # schedule_periods
    observers: Observers
    preferences: list
    all_info_loaded: bool
    _current_report: Report
    _last_report: Report
    _config: Config
    _target: Target
    _scanner: Scanner

    @staticmethod
    def resolve_tasks(gmp, root: etree.Element) -> list:
        tasks = []
        for child in root:
            if child.tag == "task":
                tasks.append(Task.resolve_task(gmp, child))
        if len(tasks) == 1:
            return tasks[0]
        else:
            return tasks

    @staticmethod
    def resolve_task(gmp, root: etree.Element) -> "Task":
        uuid = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = root.find("name").text
        comment = get_text_from_element(root, "comment")

        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")

        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")

        permissions = Permission.resolve_permissions(root.find("permissions"))
        alterable = get_bool_from_element(root, "alterable")
        usage_type = get_text_from_element(root, "usage_type")
        config = Config.resolve_config(root.find("config"))
        target = Target.resolve_target(root.find("target"), gmp)
        hosts_ordering = get_text_from_element(root, "hosts_ordering")
        scanner = Scanner.resolve_scanner(root.find("scanner"))
        status = get_text_from_element(root, "status")
        progress = get_int_from_element(root, "progress")

        report_count = ReportCount.resolve_report_count(
            root.find("report_count")
        )
        trend = get_text_from_element(root, "trend")

        schedule = Schedule.resolve_schedule(root.find("schedule"))
        current_report = root.find("current_report")
        if current_report is not None:
            current_report = Report.resolve_report(
                current_report.find("report"), gmp
            )

        last_report = root.find("last_report")
        if last_report is not None:
            last_report = Report.resolve_report(last_report.find("report"), gmp)

        observers = Observers.resolve_observers(root.find("observers"))
        preferences = Preference.resolve_preferences(root.find("preferences"))

        task = Task(
            gmp,
            uuid,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            permissions,
            alterable,
            usage_type,
            hosts_ordering,
            status,
            progress,
            report_count,
            trend,
            schedule,
            observers,
            preferences,
            False,
            current_report,
            last_report,
            config,
            target,
            scanner,
        )

        return task

    def load_current_report(self, gmp):
        if self._current_report is None:
            return None

        if self._current_report.uuid != "":
            self._current_report = gmp.get_report(
                self._current_report.uuid
            ).reports
            self._current_report.all_info_loaded = True

    def load_last_report(self, gmp):
        if self._last_report is None:
            return None

        if self._last_report.uuid != "":
            self._last_report = gmp.get_report(self._last_report.uuid).reports
            self._last_report.all_info_loaded = True

    def load_config(self, gmp):
        if self._last_report is None:
            return None

        if self._config.uuid != "":
            if not self._config.all_info_loaded:
                trash = self._config.trash
                self._config = gmp.get_config(self._config.uuid).configs
                self._config.trash = trash
                self._config.all_info_loaded = True

    def load_target(self, gmp):
        if self._target.uuid != "":
            if not self._target.all_info_loaded:
                trash = self._target.trash
                self._target = gmp.get_target(self._target.uuid).targets
                self._target.trash = trash
                self._target.all_info_loaded = True

    def load_scanner(self, gmp):
        # das Abfragen von Informationen zu einem Scanner dauert sehr lange.
        if self._scanner.uuid != "":
            if not self._scanner.all_info_loaded:
                # safe this information, because it's always None in get_scanner
                trash = self._scanner.trash
                self._scanner = gmp.get_scanner(self._scanner.uuid).scanners
                self._scanner.trash = trash
                self._scanner.all_info_loaded = True

    # Load additional Information when needed
    @property
    def current_report(self) -> Report:
        self.load_current_report(self.gmp)
        return self._current_report

    @current_report.setter
    def current_report(self, report: Report):
        self._current_report = report

    @property
    def last_report(self) -> Report:
        self.load_last_report(self.gmp)
        return self._last_report

    @last_report.setter
    def last_report(self, report: Report):
        self._last_report = report

    @property
    def config(self) -> Config:
        self.load_config(self.gmp)
        return self._config

    @config.setter
    def config(self, config: Config):
        self._config = config

    @property
    def target(self) -> Target:
        self.load_target(self.gmp)
        return self._target

    @target.setter
    def target(self, target: Target):
        self._target = target

    @property
    def scanner(self) -> Scanner:
        self.load_scanner(self.gmp)
        return self._scanner

    @scanner.setter
    def scanner(self, scanner: Scanner):
        self._scanner = scanner
