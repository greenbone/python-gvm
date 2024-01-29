# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


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
