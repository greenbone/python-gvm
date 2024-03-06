# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.xml import XmlCommand

from .._request import Request


class Version:
    @staticmethod
    def get_version() -> Request:
        """Get the Greenbone Vulnerability Manager Protocol version used
        by the remote gvmd.
        """
        return XmlCommand("get_version")
