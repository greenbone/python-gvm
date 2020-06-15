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
from lxml import etree
from .classes import (
    Role,
    Task,
    Target,
    PortList,
    Config,
    Scanner,
    Preference,
    User,
    Report,
    Group,
)


@dataclass
class Response:
    """
    standard Python Response Object
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
    Response Object for authenticate command
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
    Response Object for a get_port_lists command
    """

    port_lists: list

    def __init__(self, _gmp, root: etree.Element):
        super().__init__(root)
        self.port_lists = PortList.resolve_port_lists(root)


@dataclass
class GetTasksResponse(Response):
    """
    Response Object for a get_tasks command
    """

    apply_overrides: bool
    tasks: list

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        apply_overrides = root.find("apply_overrides")
        self.apply_overrides = False if apply_overrides.text == "0" else True
        root.remove(apply_overrides)
        self.tasks = Task.resolve_tasks(gmp, root)
        print(etree.tostring(root))


@dataclass
class GetConfigsResponse(Response):

    configs: list

    def __init__(self, _gmp, root: etree.Element):
        super().__init__(root)
        self.configs = Config.resolve_configs(root)
        # print(etree.tostring(root))


@dataclass
class GetTargetsResponse(Response):

    targets: list

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        self.targets = Target.resolve_targets(root, gmp)


@dataclass
class GetScannersResponse(Response):

    scanners: list

    def __init__(self, _gmp, root: etree.Element):
        super().__init__(root)
        self.scanners = Scanner.resolve_scanners(root)


@dataclass
class GetPreferencesResponse(Response):

    preferences: list

    def __init__(self, _gmp, root: etree.Element):
        super().__init__(root)
        self.preferences = Preference.resolve_preferences(root)


@dataclass
class GetUsersResponse(Response):

    users: list

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        self.users = User.resolve_users(root, gmp)
        # print(etree.tostring(root))


@dataclass
class GetReportsResponse(Response):

    reports: list

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        # print(etree.tostring(root))
        self.reports = Report.resolve_reports(root, gmp)


@dataclass
class GetGroupsResponse(Response):

    groups: list

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        # print(etree.tostring(root))
        self.groups = Group.resolve_groups(root, gmp)


@dataclass
class CreateTaskResponse(Response):

    task: Task

    def __init__(self, gmp, root: etree.Element):
        super().__init__(root)
        self.task = gmp.get_task(root.get("id")).tasks


@dataclass
class StartTaskResponse(Response):

    # report: Report

    def __init__(self, _gmp, root: etree.Element):
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
}


def get_response_class(tag_name: str) -> Response:
    return CLASSDICT[tag_name]
