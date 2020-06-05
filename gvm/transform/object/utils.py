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
from lxml import etree


def resolve_datetime(time: str) -> datetime.datetime:
    """
    takes a time String like: 2020-03-05T15:35:21Z
    and forms a datetime object from it.
    """
    if time is not None:
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    return None


def get_text(element: etree.Element) -> str:
    """ Get the text from an etree.Element
    """
    if element is not None:
        return element.text
    return None


def get_int(number: str) -> int:
    """ Forms a string into an integer
    """
    if number is not None:
        try:
            return int(number)
        except ValueError:
            return None
    return None


def get_bool(bool_str: str) -> bool:
    if bool_str is not None:
        return False if bool_str == "0" else True
    return None


def get_subelement(element: etree.Element, name: str) -> str:
    if element is not None:
        return element.find(name)
    return None


def get_text_from_element(element: etree.Element, name: str) -> str:
    return get_text(get_subelement(element, name))


def get_int_from_element(element: etree.Element, name: str) -> int:
    return get_int(get_text_from_element(element, name))


def get_bool_from_element(element: etree.Element, name: str) -> bool:
    return get_bool(get_text_from_element(element, name))


def get_datetime_from_element(
    element: etree.Element, name: str
) -> datetime.datetime:
    return resolve_datetime(get_text_from_element(element, name))
