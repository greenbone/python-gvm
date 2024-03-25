# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from numbers import Real

from gvm._enum import Enum

Severity = Real


class SeverityLevel(Enum):
    """Enum for severity levels"""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOG = "Log"
    ALARM = "Alarm"
    DEBUG = "Debug"
