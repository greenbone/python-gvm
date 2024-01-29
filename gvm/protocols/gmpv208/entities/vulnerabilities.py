# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Any, Optional

from gvm.errors import RequiredArgument
from gvm.utils import add_filter
from gvm.xml import XmlCommand


class VulnerabilitiesMixin:
    def get_vulnerabilities(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
    ) -> Any:
        """Request a list of vulnerabilities

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_vulns")

        add_filter(cmd, filter_string, filter_id)

        return self._send_xml_command(cmd)

    def get_vulnerability(self, vulnerability_id: str) -> Any:
        """Request a single vulnerability

        Arguments:
            vulnerability_id: ID of an existing vulnerability

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not vulnerability_id:
            raise RequiredArgument(
                function=self.get_vulnerability.__name__,
                argument="vulnerability_id",
            )

        cmd = XmlCommand("get_vulns")
        cmd.set_attribute("vuln_id", vulnerability_id)
        return self._send_xml_command(cmd)
