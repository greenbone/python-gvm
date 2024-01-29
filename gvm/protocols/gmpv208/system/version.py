# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Any

from gvm.xml import XmlCommand

PROTOCOL_VERSION = (20, 8)


class VersionMixin:
    def get_version(self) -> Any:
        """Get the Greenbone Vulnerability Manager Protocol version used
        by the remote gvmd.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("get_version"))

    @staticmethod
    def get_protocol_version() -> tuple:
        """Determine the Greenbone Management Protocol (gmp) version used
        by python-gvm version.

        Returns:
            tuple: Implemented version of the Greenbone Management Protocol
        """
        return PROTOCOL_VERSION
