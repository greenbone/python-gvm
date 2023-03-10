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
from numbers import Real
from typing import Optional

from gvm.errors import InvalidArgument

Severity = Real


class SeverityLevel(Enum):
    """Enum for severity levels"""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOG = "Log"
    ALARM = "Alarm"
    DEBUG = "Debug"

    @classmethod
    def from_string(
        cls,
        severity_level: Optional[str],
    ) -> Optional["SeverityLevel"]:
        """Convert a severity level string into a SeverityLevel instance"""
        if not severity_level:
            return None

        try:
            return cls[severity_level.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="severity_level",
                function=cls.from_string.__name__,
            ) from None
