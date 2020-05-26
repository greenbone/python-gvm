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
    # print(etree.tostring(root))
    name = root.find('name').text
    if name is None:
        return None
    else:
        return Owner(name)


def resolve_port_lists(root: etree.Element):
    result_list = []

    for child in root:
        if child.tag == "port_list":
            result_list.append(resolve_port_list(child))
    return result_list


def resolve_port_list(root: etree.Element) -> PortList:
    owner = resolve_owner(root.find("owner"))
    name = root.find("name").text
    comment = root.find("comment").text
    creation_time_text = root.find("creation_time").text
    creation_time = datetime.datetime.strptime(
        creation_time_text, "%Y-%m-%dT%H:%M:%SZ"
    )
    modification_time_text = root.find("modification_time").text
    modification_time = datetime.datetime.strptime(
        creation_time_text, "%Y-%m-%dT%H:%M:%SZ"
    )
    writable = False if root.find("writable").text == "0" else True
    print(writable)

    # print(time.strftime("%D %H:%M:%S", time.localtime(creation_time)))
    # print(etree.tostring(creation_time))
    # print(comment)
