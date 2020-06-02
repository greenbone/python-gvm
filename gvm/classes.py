# -*- coding: utf-8 -*-
# Copyright (C) 2018 - 2019 Greenbone Networks GmbH
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

LOAD_MORE = True  # just temporary


def resolve_datetime(time: str) -> datetime.datetime:
    """
    takes a time String like: 2020-03-05T15:35:21Z
    and forms a datetime object from it.
    """
    return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")


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
    port_range_id: str
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
    port_list_id: str
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
        port_list_id = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = root.find("name").text
        comment = root.find("comment")
        if comment is not None:
            comment = comment.text
        creation_time = root.find("creation_time")
        if creation_time is not None:
            creation_time = resolve_datetime(creation_time.text)

        modification_time = root.find("modification_time")
        if modification_time is not None:
            modification_time = resolve_datetime(modification_time.text)

        writable = root.find("writable")
        if writable is not None:
            writable = False if writable.text == "0" else True

        in_use = root.find("in_use")
        if in_use is not None:
            in_use = False if in_use.text == "0" else True

        permissions = Permission.resolve_permissions(root.find("permissions"))
        port_count = PortCount.resolve_port_count(root.find("port_count"))
        port_ranges = PortRange.resolve_port_ranges(root.find("port_ranges"))

        port_list = PortList(
            port_list_id,
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
    def resolve_nvt_count(root: etree.Element) -> "Nvt_Count":
        if root is None:
            return None
        return NvtCount(
            current=int(root.text), growing=int(root.find("growing").text)
        )


@dataclass
class Config:
    config_id: str
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
    # was bedeutet <trash> in der get Tasks antwort für configs??

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
        config_id = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = root.find("name").text

        comment = root.find("comment")
        if comment is not None:
            comment = comment.text

        if root.find("creation_time") is not None:
            creation_time = resolve_datetime(root.find("creation_time").text)
        else:
            creation_time = None

        if root.find("modification_time") is not None:
            modification_time = resolve_datetime(
                root.find("modification_time").text
            )
        else:
            modification_time = None

        writable = root.find("writable")
        if writable is not None:
            writable = False if writable.text == "0" else True

        in_use = root.find("in_use")
        if in_use is not None:
            in_use = False if in_use.text == "0" else True

        permissions = Permission.resolve_permissions(root.find("permissions"))
        family_count = FamilyCount.resolve_family_count(
            root.find("family_count")
        )
        nvt_count = NvtCount.resolve_nvt_count(root.find("nvt_count"))
        config_type = int(root.find("type").text)

        usage_type = root.find("usage_type")
        if usage_type is not None:
            usage_type = usage_type.text

        return Config(
            config_id,
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
        )


@dataclass
class Target:
    target_id: str
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
        target_id = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = root.find("name").text
        comment = root.find("comment")
        if comment is not None:
            comment = comment.text
        creation_time = root.find("creation_time")
        if creation_time is not None:
            creation_time = resolve_datetime(creation_time.text)

        modification_time = root.find("modification_time")
        if modification_time is not None:
            modification_time = resolve_datetime(modification_time.text)

        writable = root.find("writable")
        if writable is not None:
            writable = False if writable.text == "0" else True

        in_use = root.find("in_use")
        if in_use is not None:
            in_use = False if in_use.text == "0" else True

        permissions = Permission.resolve_permissions(root.find("permissions"))
        # hosts
        # exclude_hosts
        port_list = PortList.resolve_port_list(root.find("port_list"))
        # ssh_credential
        # smb_credential
        # esxi_credential
        # snmp_credential
        reverse_lookup_only = root.find("reverse_lookup_only")
        if reverse_lookup_only is not None:
            reverse_lookup_only = (
                False if reverse_lookup_only.text == "0" else True
            )

        reverse_lookup_unify = root.find("reverse_lookup_unify")
        if reverse_lookup_unify is not None:
            reverse_lookup_unify = (
                False if reverse_lookup_unify.text == "0" else True
            )

        # alive_tests: str ?

        return Target(
            target_id,
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
        )


@dataclass
class Scanner:
    scanner_id: str
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
        scanner_id = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = root.find("name").text
        comment = root.find("comment")
        if comment is not None:
            comment = comment.text

        creation_time = root.find("creation_time")
        if creation_time is not None:
            creation_time = resolve_datetime(creation_time.text)

        modification_time = root.find("modification_time")
        if modification_time is not None:
            modification_time = resolve_datetime(modification_time.text)

        writable = root.find("writable")
        if writable is not None:
            writable = False if writable.text == "0" else True

        in_use = root.find("in_use")
        if in_use is not None:
            in_use = False if in_use.text == "0" else True

        permissions = Permission.resolve_permissions(root.find("permissions"))
        # host
        port = root.find("port")
        if port is not None:
            port = int(port.text)

        scanner_type = root.find("type")
        if scanner_type is not None:
            scanner_type = int(scanner_type.text)

        scanner = Scanner(
            scanner_id,
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
        )
        return scanner


@dataclass
class Task:
    task_id: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    permissions: list
    alterable: bool
    usage_type: str
    config: Config
    target: Target
    host_ordering: str
    scanner: Scanner
    status: str
    progress: int
    # report_count: ReportCount
    # trend: ??
    # schedule: Schedule
    # last_report: Report
    # observers: ??
    # preferences: list

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
        task_id = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = root.find("name").text
        comment = root.find("comment").text
        creation_time = resolve_datetime(root.find("creation_time").text)
        modification_time = resolve_datetime(
            root.find("modification_time").text
        )
        writable = False if root.find("writable").text == "0" else True
        in_use = False if root.find("in_use").text == "0" else True
        permissions = Permission.resolve_permissions(root.find("permissions"))
        alterable = False if root.find("alterable").text == "0" else True
        usage_type = root.find("usage_type").text
        config = Config.resolve_config(root.find("config"))
        target = Target.resolve_target(root.find("target"))
        host_ordering = root.find("hosts_ordering").text
        scanner = Scanner.resolve_scanner(root.find("scanner"))
        status = root.find("status").text
        progress = int(root.find("progress").text)

        task = Task(
            task_id,
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
            host_ordering,
            scanner,
            status,
            progress,
        )

        if LOAD_MORE:
            task.load_config(gmp)
            task.load_target(gmp)
            task.load_scanner(gmp)

        return task

    def load_config(self, gmp):
        self.config = gmp.get_config(self.config.config_id).configs

    def load_target(self, gmp):
        self.target = gmp.get_target(self.target.target_id).targets

    def load_scanner(self, gmp):
        # das Abfragen von Informationen zu einem Scanner dauert sehr lange.
        self.scanner = gmp.get_scanner(self.scanner.scanner_id).scanners
