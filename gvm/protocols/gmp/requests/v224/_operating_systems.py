# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class OperatingSystems:

    @classmethod
    def delete_operating_system(
        cls,
        operating_system_id: EntityID,
    ) -> Request:
        """Deletes an existing operating system

        Args:
            operating_system_id: UUID of the single operating_system to delete.
        """
        if not operating_system_id:
            raise RequiredArgument(
                function=cls.delete_operating_system.__name__,
                argument="operating_system_id",
            )

        cmd = XmlCommand("delete_asset")
        cmd.set_attribute("asset_id", str(operating_system_id))

        return cmd

    @staticmethod
    def get_operating_systems(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of operating systems

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include additional information (e.g. tags)
        """

        cmd = XmlCommand("get_assets")

        cmd.set_attribute("type", "os")

        cmd.add_filter(filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return cmd

    @classmethod
    def get_operating_system(
        cls, operating_system_id: EntityID, *, details: Optional[bool] = None
    ) -> Request:
        """Request a single operating system

        Args:
            operating_system_id: UUID of an existing operating_system
            details: Whether to include additional information (e.g. tags)
        """
        cmd = XmlCommand("get_assets")

        if not operating_system_id:
            raise RequiredArgument(
                function=cls.get_operating_system.__name__,
                argument="operating_system_id",
            )

        cmd.set_attribute("asset_id", str(operating_system_id))
        cmd.set_attribute("type", "os")

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return cmd

    @classmethod
    def modify_operating_system(
        cls, operating_system_id: EntityID, *, comment: Optional[str] = None
    ) -> Request:
        """Modifies an existing operating system.

        Args:
            operating_system_id: UUID of the operating_system to be modified.
            comment: Comment for the operating_system. Not passing a comment
                arguments clears the comment for this operating system.
        """
        if not operating_system_id:
            raise RequiredArgument(
                function=cls.modify_operating_system.__name__,
                argument="operating_system_id",
            )

        cmd = XmlCommand("modify_asset")
        cmd.set_attribute("asset_id", str(operating_system_id))
        if not comment:
            comment = ""
        cmd.add_element("comment", comment)

        return cmd
