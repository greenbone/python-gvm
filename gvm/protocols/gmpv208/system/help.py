# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
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

from enum import Enum
from typing import Any, Optional

from gvm.errors import InvalidArgument, InvalidArgumentType
from gvm.xml import XmlCommand


class HelpFormat(Enum):
    """Enum for the help format"""

    HTML = "html"
    RNC = "rnc"
    TEXT = "text"
    XML = "xml"

    @classmethod
    def from_string(
        cls,
        sort_order: Optional[str],
    ) -> Optional["HelpFormat"]:
        """
        Convert a sort order string to an actual SortOrder instance.

        Arguments:
            sort_order: Sort order string to convert to a SortOrder
        """
        if not sort_order:
            return None

        try:
            return cls[sort_order.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="sort_order", function=cls.from_string.__name__
            ) from None


class HelpMixin:
    def help(
        self,
        *,
        help_format: Optional[HelpFormat] = None,
        brief: Optional[bool] = None,
    ) -> Any:
        """Get the help text

        Arguments:
            help_format: Format of of the help:
                "html", "rnc", "text" or "xml
            brief: If True help is brief

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("help")

        help_type = ""
        if brief:
            help_type = "brief"

        cmd.set_attribute("type", help_type)

        if help_format:
            if not isinstance(help_format, HelpFormat):
                raise InvalidArgumentType(
                    function=self.help.__name__,
                    argument="feed_type",
                    arg_type=HelpFormat.__name__,
                )

            cmd.set_attribute("format", help_format.value)

        return self._send_xml_command(cmd)
