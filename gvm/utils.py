# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# pylint: disable=arguments-differ, redefined-builtin

import base64
import logging
import re
import warnings
from functools import wraps
from typing import (
    Any,
    Callable,
    Iterable,
    List,
    Optional,
    Protocol,
    Type,
    Union,
)

from gvm.xml import XmlCommand, XmlError, parse_xml

logger = logging.getLogger(__name__)


class TypesDict(dict):
    """For dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__  # type: ignore[assignment]
    __delattr__ = dict.__delitem__  # type: ignore[assignment]


def deprecation(message: str):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


def deprecated(
    _func_or_cls: Union[str, Callable, Type, None] = None,
    *,
    since: Optional[str] = None,
    reason: Optional[str] = None,
):
    """
    A decorator to mark functions, classes and methods as deprecated

    Args:
        since: An optional version since the referenced item is deprecated.
        reason: An optional reason why the references item is deprecated.

    Examples:
        .. code-block:: python

            from gvm.utils import deprecated

            @deprecated
            def my_function(*args, **kwargs):
                ...

            @deprecated("The function is obsolete. Please use my_func instead.")
            def my_function(*args, **kwargs):
                ...

            @deprecated(
                since="1.2.3",
                reason="The function is obsolete. Please use my_func instead."
            )
            def my_function(*args, **kwargs):
                ...

            @deprecated(reason="The class will be removed in version 3.4.5")
            class Foo:
                ...

            class Foo:
                @deprecated(since="2.3.4")
                def bar(self, *args, **kwargs):
                    ...
    """
    if isinstance(_func_or_cls, str):
        reason = _func_or_cls
        _func_or_cls = None

    def decorator_repeat(func_or_cls):
        module = func_or_cls.__module__
        name = func_or_cls.__name__

        if module == "__main__":
            msg = f"{name} is deprecated."
        else:
            msg = f"{module}.{name} is deprecated."

        if since:
            msg += f" It is deprecated since version {since}."
        if reason:
            msg += f" {reason}"

        @wraps(func_or_cls)
        def wrapper(*args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=3)
            return func_or_cls(*args, **kwargs)

        return wrapper

    if _func_or_cls is None:
        return decorator_repeat
    else:
        return decorator_repeat(_func_or_cls)


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


def to_base64(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode(encoding="utf-8")


class SupportsStr(Protocol):
    def __str__(self) -> str: ...


def to_comma_list(value: Iterable[SupportsStr]) -> str:
    return ",".join([str(value) for value in value])


@deprecated(since="24.3.0", reason="Please use XmlCommand.add_filter instead.")
def add_filter(
    cmd: XmlCommand, filter_string: Optional[str], filter_id: Optional[str]
) -> None:
    cmd.add_filter(filter_string, filter_id)


def is_list_like(value: Any) -> bool:
    return isinstance(value, (list, tuple))


def check_port(value: str) -> bool:
    pattern = re.compile(
        r"^(cpe:[^\s]+|(general|[1-9][0-9]{0,4})/[0-9A-Za-z]+)$"
    )
    return bool(pattern.fullmatch(value))
