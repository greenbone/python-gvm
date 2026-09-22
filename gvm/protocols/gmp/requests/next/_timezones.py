# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.protocols.core import Request
from gvm.xml import XmlCommand


class Timezones:
    @classmethod
    def get_timezones(cls) -> Request:
        """Request a list of supported timezones."""
        return XmlCommand("get_timezones")
