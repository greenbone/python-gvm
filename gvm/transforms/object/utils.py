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

import logging
import datetime
from lxml import etree

logger = logging.getLogger(__name__)


def resolve_datetime(time: str) -> datetime.datetime:
    """takes a time String and forms a datetime object from it.

    Arguments:
        time: Timestring eg. '2020-03-05T15:35:21Z'
    """
    if time is not None:
        try:
            return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError as error:
            logger.warning(str(error))
            return None
    return None


def get_text(element: etree.Element) -> str:
    """ Get the text from an etree.Element

    Arguments:
        element: Element which contains the text
    """
    if element is not None:
        return element.text
    return None


def get_int(number: str) -> int:
    """ Forms a string into an integer

    Arguments:
        number: Integer in form of a string
    """
    if number is not None:
        try:
            return int(number)
        except ValueError as error:
            logger.warning(str(error))
            return None
    return None


def get_float(number: str):
    """Forms a string into a float

    Arguments:
        number: Float in form of a string
    """
    if number is None:
        return None
    try:
        return float(number)
    except ValueError as error:
        logger.warning(str(error))
        return None


def get_bool(bool_str: str) -> bool:
    """Forms a string into a bool

    Arguments:
        bool_str: should be '1' or '0'
    """
    if bool_str is not None:
        return False if bool_str == "0" else True
    return None


def get_subelement(element: etree.Element, name: str) -> etree.Element:
    """ Get a subelement from an etree.Element.

    Arguments:
        element: Element which contains the subelement.
        name: Name of the subelement.
    """
    if element is not None:
        return element.find(name)
    return None


def get_text_from_element(element: etree.Element, name: str) -> str:
    """ Get the text from an etree.Element.

    Arguments:
        element: Element which contains the subelement with text in it.
        name: Name of the subelement.
    """
    return get_text(get_subelement(element, name))


def get_int_from_element(element: etree.Element, name: str) -> int:
    """ Get an integer from an etree.Element.

    Arguments:
        element: Element which contains the subelement with an integer in it.
        name: Name of the subelement.
    """
    return get_int(get_text_from_element(element, name))


def get_bool_from_element(element: etree.Element, name: str) -> bool:
    """ Get a bool from an etree.Element.

    Arguments:
        element: Element which contains the subelement with a '1' or '0' in it.
        name: Name of the subelement.
    """
    return get_bool(get_text_from_element(element, name))


def get_float_from_element(element: etree.Element, name: str) -> float:
    """ Get a float from an etree.Element.

    Arguments:
        element: Element which contains the subelement with a float in it.
        name: Name of the subelement.
    """
    return get_float(get_text_from_element(element, name))


def get_datetime_from_element(
    element: etree.Element, name: str
) -> datetime.datetime:
    """ Get a datetime from an etree.Element.

    Arguments:
        element: Element which contains the subelement with a datetime string.
        name: Name of the subelement.
    """
    return resolve_datetime(get_text_from_element(element, name))
