# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.protocols.core import Request
from gvm.xml import XmlCommand


class Version:
    @staticmethod
    def get_version() -> Request:
        """Get the Greenbone Vulnerability Management Protocol (GMP) version
        used by the remote gvmd.
        """
        return XmlCommand("get_version")
