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

from gvm.classes import *
from dataclasses import dataclass
from lxml import etree


@dataclass
class Response:
    """
    standard Python Response Object
    """

    response_name: str
    status: int
    status_text: str

    def __init__(self, response_name: str, status: int, status_text: str):
        self.response_name = response_name
        self.status = status
        self.status_text = status_text


@dataclass
class AuthenticateResponse(Response):
    """
    Response Object for authenticate command
    """

    role: Role
    timezone: str
    severity: str

    def __init__(self, root: etree.Element):
        super().__init__(root.tag, root.get("status"), root.get("status_text"))
        self.role = Role.resolve_role(root.find("role"))
        self.timezone = root.find("timezone").text
        self.severity = root.find("severity").text


@dataclass
class GetPortListsResponse(Response):
    """
    Response Object for a get_port_lists command
    """

    port_lists: list

    def __init__(self, root: etree.Element):
        super().__init__(root.tag, root.get("status"), root.get("status_text"))
        self.port_lists = PortList.resolve_port_lists(root)


@dataclass
class GetTasksResponse(Response):
    """
    Response Object for a get_tasks command
    """

    apply_overrides: bool
    tasks: list

    def __init__(self, root: etree.Element):
        super().__init__(root.tag, root.get("status"), root.get("status_text"))
        # print(etree.tostring(root))


CLASSDICT = {
    "authenticate_response": AuthenticateResponse,
    "get_port_lists_response": GetPortListsResponse,
    "get_tasks_response": GetTasksResponse,
}


def get_response_class(tag_name: str) -> Response:
    return CLASSDICT[tag_name]
