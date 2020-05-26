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

from lxml import etree
from gvm.classes import *


def resolve_role(root: etree.Element) -> Role:
    return Role(root.text)


def resolve_owner(root: etree.Element) -> Owner:
    name = root.find('name').text
    if name is None:
        return None
    else:
        return Owner(name)
def resolve_port_count(root: etree.Element) -> PortCount:
    return PortCount(
        int(root.find("all").text),
        int(root.find("tcp").text),
        int(root.find("udp").text)
    )

def resolve_port_ranges(root: etree.Element) -> list:
    if root is None: return None
    port_ranges = []
    for port_range in root:
        port_ranges.append(
            PortRange(
                port_range.get("id"),
                int(port_range.find("start").text),
                int(port_range.find("end").text),
                port_range.find("type").text,
                port_range.find("comment").text
            )
        )
    return port_ranges

def resolve_port_lists(root: etree.Element):
    result_list = []

    for child in root:
        if child.tag == "port_list":
            port_list = resolve_port_list(child)
            result_list.append(port_list)

    return result_list


def resolve_port_list(root: etree.Element) -> PortList:
    port_list_id = root.get("id")
    owner = resolve_owner(root.find("owner"))
    name = root.find("name").text
    comment = root.find("comment").text
    creation_time_text = root.find("creation_time").text
    creation_time = datetime.datetime.strptime(
        creation_time_text, "%Y-%m-%dT%H:%M:%SZ"
    )
    modification_time_text = root.find("modification_time").text
    modification_time = datetime.datetime.strptime(
        modification_time_text, "%Y-%m-%dT%H:%M:%SZ"
    )
    writable = False if root.find("writable").text == "0" else True
    in_use = False if root.find("in_use").text == "0" else True
    permissions = resolve_permissions(root.find("permissions"))
    port_count = resolve_port_count(root.find("port_count"))
    port_ranges = resolve_port_ranges(root.find("port_ranges"))

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
        port_ranges
    )
    return port_list

def resolve_permissions(root: etree.Element) -> list:
    permissions = []
    for permission in root:
        permissions.append(
            Permission(permission.find("name").text)
            )

    return permissions
