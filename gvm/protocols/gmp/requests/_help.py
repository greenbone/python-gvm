# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm._enum import Enum
from gvm.protocols.core import Request
from gvm.xml import XmlCommand


class HelpFormat(Enum):
    """Enum for the help format"""

    HTML = "html"
    RNC = "rnc"
    TEXT = "text"
    XML = "xml"


class Help:
    @staticmethod
    def help(
        *,
        help_format: Optional[Union[HelpFormat, str]] = None,
        brief: Optional[bool] = None,
    ) -> Request:
        """Get the help text

        Arguments:
            help_format: Format of of the help:
                "html", "rnc", "text" or "xml
            brief: If True help is brief
        """
        cmd = XmlCommand("help")

        help_type = ""
        if brief:
            help_type = "brief"

        cmd.set_attribute("type", help_type)

        if help_format:
            if not isinstance(help_format, HelpFormat):
                help_format = HelpFormat(help_format)

            cmd.set_attribute("format", help_format.value)

        return cmd
