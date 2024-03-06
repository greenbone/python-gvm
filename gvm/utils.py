# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# pylint: disable=arguments-differ, redefined-builtin

import base64
import logging
import re
import warnings
from typing import Any, List, Union

from gvm.xml import XmlError, parse_xml

logger = logging.getLogger(__name__)


class TypesDict(dict):
    """For dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def deprecation(message: str):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


def check_command_status(xml: str) -> bool:
    """Check gmp response

    Look into the gmp response and check for the status in the root element

    Arguments:
        xml: XML-Source

    Returns:
        True if valid, otherwise False
    """

    if xml == 0 or xml is None:
        logger.error("XML Command is empty.")
        return False

    try:
        root = parse_xml(xml)
        status = root.attrib["status"]
        return status is not None and status[0] == "2"
    except KeyError:
        print(logger)
        logger.error("Not received an status code within the response.")
        return False
    except XmlError as e:
        logger.error("Error while parsing the command status: %s", e)
        return False


def to_dotted_types_dict(types: List) -> TypesDict:
    """Create a dictionary accessible via dot notation"""
    dic = {}
    for typ in types:
        dic[typ.__name__] = typ
    return TypesDict(dic)


def to_bool(value: Union[bool, int, None]) -> str:
    return "1" if value else "0"


def to_base64(value: str) -> bytes:
    return base64.b64encode(value.encode("utf-8"))


def to_comma_list(value: List) -> str:
    return ",".join(value)


def add_filter(cmd, filter_string, filter_id):
    if filter_string:
        cmd.set_attribute("filter", filter_string)

    if filter_id:
        cmd.set_attribute("filt_id", filter_id)


def is_list_like(value: Any) -> bool:
    return isinstance(value, (list, tuple))


def check_port(value: str) -> bool:
    pattern = re.compile(
        r"^(cpe:[^\s]+|(general|[1-9][0-9]{0,4})/[0-9A-Za-z]+)$"
    )
    if pattern.fullmatch(value):
        return True
    return False
