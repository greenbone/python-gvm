# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class Cpes:

    @staticmethod
    def get_cpes(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        name: Optional[str] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of CPEs

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            name: Name or identifier of the requested information
            details: Whether to include information about references to this
                information
        """
        cmd = XmlCommand("get_info")

        cmd.set_attribute("type", "CPE")

        cmd.add_filter(filter_string, filter_id)

        if name:
            cmd.set_attribute("name", name)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return cmd

    @classmethod
    def get_cpe(cls, cpe_id: str) -> Request:
        """Request a single CPE

        Args:
            cpe_id: ID of an existing CPE
        """
        if not cpe_id:
            raise RequiredArgument(
                function=cls.get_cpe.__name__, argument="cpe_id"
            )

        cmd = XmlCommand("get_info")
        cmd.set_attribute("info_id", cpe_id)

        cmd.set_attribute("type", "CPE")

        # for single entity always request all details
        cmd.set_attribute("details", "1")

        return cmd
