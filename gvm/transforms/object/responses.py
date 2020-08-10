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

from dataclasses import dataclass
from typing import List
from lxml import etree
from .user_classes import Role, User, Group
from .task_classes import Task, Target, Report, Preference, ScanConfig
from .scan_classes import Scanner
from .port_classes import PortList


@dataclass
class Response:
    """
    standard Python response object
    """

    response_name: str
    status: int
    status_text: str

    def __init__(self, root: etree.Element):
        self.response_name = root.tag
        self.status = root.get("status")
        self.status_text = root.get("status_text")


@dataclass
class AuthenticateResponse(Response):
    """
    Response object for authenticate command
    """

    role: Role
    timezone: str
    severity: str

    def __init__(self, _gmp, root: etree.Element):
        super().__init__(root)
        self.role = Role.resolve_role(root.find("role"))
        self.timezone = root.find("timezone").text
        self.severity = root.find("severity").text


@dataclass
class GetPortListsResponse(Response):
    """
    Response object for a get_port_lists command\n
    (see also: :class:`.port_classes.PortList`)
    """

    port_lists: List[PortList]

    def __init__(self, _gmp, root: etree.Element):
        super().__init__(root)
        self.port_lists = PortList.resolve_port_lists(root)


@dataclass
class GetTasksResponse(Response):
    """
    Response object for a get_tasks command\n
    (see also: :class:`.task_classes.Task`)
    """

    apply_overrides: bool
    tasks: List[Task]

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        apply_overrides = root.find("apply_overrides")
        self.apply_overrides = False if apply_overrides.text == "0" else True
        root.remove(apply_overrides)
        self.tasks = Task.resolve_tasks(root, gmp)
        # print(etree.tostring(root))


@dataclass
class GetConfigsResponse(Response):
    """Response object for a get_configs command\n
    (see also: :class:`.task_classes.ScanConfig`)
    """

    scan_configs: List[ScanConfig]

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        self.scan_configs = ScanConfig.resolve_configs(root, gmp)
        # print(etree.tostring(root))


@dataclass
class GetTargetsResponse(Response):
    """Response object for a get_targets command\n
    (see also: :class:`.task_classes.Target`)
    """

    targets: List[Target]

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        self.targets = Target.resolve_targets(root, gmp)


@dataclass
class GetScannersResponse(Response):
    """Response object for a get_configs command\n
    (see also: :class:`.scan_classes.Scanner`)
    """

    scanners: List[Scanner]

    def __init__(self, _gmp, root: etree.Element):
        super().__init__(root)
        self.scanners = Scanner.resolve_scanners(root)


@dataclass
class GetPreferencesResponse(Response):
    """Response object for a get_preferences command\n
    (see also: :class:`.task_classes.Preference`)
    """

    preferences: List[Preference]

    def __init__(self, _gmp, root: etree.Element):
        super().__init__(root)
        self.preferences = Preference.resolve_preferences(root)


@dataclass
class GetUsersResponse(Response):
    """Response object for a get_users command\n
    (see also: :class:`.user_classes.User`)
    """

    users: List[User]

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        self.users = User.resolve_users(root, gmp)
        # print(etree.tostring(root))


@dataclass
class GetReportsResponse(Response):
    """Response object for a get_reports command\n
    (see also: :class:`.task_classes.Report`)
    """

    reports: List[Report]

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        # print(etree.tostring(root))
        self.reports = Report.resolve_reports(root, gmp)


@dataclass
class GetGroupsResponse(Response):
    """Response object for a get_groups command\n
    (see also: :class:`.user_classes.Group`)
    """

    groups: List[Group]

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        # print(etree.tostring(root))
        self.groups = Group.resolve_groups(root, gmp)


@dataclass
class CreateTaskResponse(Response):
    """Response object for a create_task command\n
    (see also: :class:`.task_classes.Task`)
    """

    task_id: str
    task: Task

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        self.task_id = root.get("id")
        print(self.task_id)
        if gmp is not None:
            self.task = gmp.get_task(root.get("id")).tasks


@dataclass
class StartTaskResponse(Response):
    """Response object for a start_task command\n
    (see also: :class:`.task_classes.Report`)
    """

    report_id: str
    report: Report

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        self.report_id = root.find("report_id").text
        if gmp is not None:
            self.report = gmp.get_report(self.report_id)


@dataclass
class StopTaskResponse(Response):
    """Response object for a stop_task command
    """

    def __init__(self, _gmp, root):
        super().__init__(root)


CLASSDICT = {
    "authenticate_response": AuthenticateResponse,
    "get_port_lists_response": GetPortListsResponse,
    "get_tasks_response": GetTasksResponse,
    "get_configs_response": GetConfigsResponse,
    "get_targets_response": GetTargetsResponse,
    "get_scanners_response": GetScannersResponse,
    "get_preferences_response": GetPreferencesResponse,
    "get_users_response": GetUsersResponse,
    "get_reports_response": GetReportsResponse,
    "get_groups_response": GetGroupsResponse,
    "create_task_response": CreateTaskResponse,
    "start_task_response": StartTaskResponse,
    "stop_task_response": StopTaskResponse,
}


def get_response_class(tag_name: str) -> Response:
    """ Finds the matching response class from the respose tag name.

    Arguments:
        tag_name: The tag name of a GMP response.
    """
    return CLASSDICT[tag_name]
