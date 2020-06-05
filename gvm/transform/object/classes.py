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

from .utils import (
    get_bool_from_element,
    get_int_from_element,
    get_text_from_element,
    get_datetime_from_element,
    get_text,
    get_int,
)

LOAD_MORE = True  # just temporary


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
        )


@dataclass
class Target:
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
    port_list: PortList
    # ssh_credential
    # smb_credential
    # esxi_credential
    # snmp_credential
    reverse_lookup_only: bool
    reverse_lookup_unify: bool
    # alive_tests: str ?
    trash: bool

    @staticmethod
    def resolve_targets(root: etree.Element) -> list:
        targets = []
        for child in root:
            if child.tag == "target":
                targets.append(Target.resolve_target(child))

        if len(targets) == 1:
            return targets[0]
        else:
            return targets

    @staticmethod
    def resolve_target(root: etree.Element) -> "Target":
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
            port_list,
            # ssh_credential,
            # smb_credential,
            # esxi_credential,
            # snmp_credential,
            reverse_lookup_only,
            reverse_lookup_unify,
            trash,
        )


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
class Task:
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
    config: Config
    target: Target
    hosts_ordering: str
    scanner: Scanner
    # alert
    status: str
    progress: int
    report_count: ReportCount
    trend: str
    schedule: Schedule
    # schedule_periods
    # current_report
    # last_report: Report
    # reports
    observers: Observers
    preferences: list

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
        target = Target.resolve_target(root.find("target"))
        hosts_ordering = get_text_from_element(root, "hosts_ordering")
        scanner = Scanner.resolve_scanner(root.find("scanner"))
        status = get_text_from_element(root, "status")
        progress = get_int_from_element(root, "progress")

        report_count = ReportCount.resolve_report_count(
            root.find("report_count")
        )
        trend = get_text_from_element(root, "trend")

        schedule = Schedule.resolve_schedule(root.find("schedule"))

        # last_report: Report
        observers = Observers.resolve_observers(root.find("observers"))
        preferences = Preference.resolve_preferences(root.find("preferences"))

        task = Task(
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
            config,
            target,
            hosts_ordering,
            scanner,
            status,
            progress,
            report_count,
            trend,
            schedule,
            # last_report,
            observers,
            preferences,
        )

        if LOAD_MORE:
            task.load_config(gmp)
            task.load_target(gmp)
            task.load_scanner(gmp)

        return task

    def load_config(self, gmp):
        if self.config.uuid != "":
            self.config = gmp.get_config(self.config.uuid).configs

    def load_target(self, gmp):
        if self.target.uuid != "":
            self.target = gmp.get_target(self.target.uuid).targets

    def load_scanner(self, gmp):
        # das Abfragen von Informationen zu einem Scanner dauert sehr lange.
        if self.scanner.uuid != "":
            self.scanner = gmp.get_scanner(self.scanner.uuid).scanners
