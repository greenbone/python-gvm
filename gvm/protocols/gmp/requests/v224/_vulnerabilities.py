# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class Vulnerabilities:
    @staticmethod
    def get_vulnerabilities(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
    ) -> Request:
        """Request a list of vulnerabilities

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
        """
        cmd = XmlCommand("get_vulns")
        cmd.add_filter(filter_string, filter_id)
        return cmd

    @classmethod
    def get_vulnerability(cls, vulnerability_id: EntityID) -> Request:
        """Request a single vulnerability

        Args:
            vulnerability_id: ID of an existing vulnerability
        """
        if not vulnerability_id:
            raise RequiredArgument(
                function=cls.get_vulnerability.__name__,
                argument="vulnerability_id",
            )

        cmd = XmlCommand("get_vulns")
        cmd.set_attribute("vuln_id", str(vulnerability_id))
        return cmd
