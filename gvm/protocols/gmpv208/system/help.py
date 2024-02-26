# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Any, Optional

from gvm._enum import Enum
from gvm.errors import InvalidArgumentType
from gvm.xml import XmlCommand


class HelpFormat(Enum):
    """Enum for the help format"""

    HTML = "html"
    RNC = "rnc"
    TEXT = "text"
    XML = "xml"


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
