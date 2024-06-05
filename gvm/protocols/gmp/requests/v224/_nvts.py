# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class Nvts:

    @staticmethod
    def get_nvt_families(*, sort_order: Optional[str] = None) -> Request:
        """Request a list of nvt families

        Args:
            sort_order: Sort order
        """
        cmd = XmlCommand("get_nvt_families")

        if sort_order:
            cmd.set_attribute("sort_order", sort_order)

        return cmd

    @staticmethod
    def get_scan_config_nvts(
        *,
        details: Optional[bool] = None,
        preferences: Optional[bool] = None,
        preference_count: Optional[bool] = None,
        timeout: Optional[bool] = None,
        config_id: Optional[EntityID] = None,
        preferences_config_id: Optional[EntityID] = None,
        family: Optional[str] = None,
        sort_order: Optional[str] = None,
        sort_field: Optional[str] = None,
    ) -> Request:
        """Request a list of nvts

        Args:
            details: Whether to include full details
            preferences: Whether to include nvt preferences
            preference_count: Whether to include preference count
            timeout: Whether to include the special timeout preference
            config_id: UUID of scan config to which to limit the NVT listing
            preferences_config_id: UUID of scan config to use for preference
                values
            family: Family to which to limit NVT listing
            sort_order: Sort order
            sort_field: Sort field
        """
        cmd = XmlCommand("get_nvts")

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if preferences is not None:
            cmd.set_attribute("preferences", to_bool(preferences))

        if preference_count is not None:
            cmd.set_attribute("preference_count", to_bool(preference_count))

        if timeout is not None:
            cmd.set_attribute("timeout", to_bool(timeout))

        if config_id:
            cmd.set_attribute("config_id", str(config_id))

        if preferences_config_id:
            cmd.set_attribute(
                "preferences_config_id", str(preferences_config_id)
            )

        if family:
            cmd.set_attribute("family", family)

        if sort_order:
            cmd.set_attribute("sort_order", sort_order)

        if sort_field:
            cmd.set_attribute("sort_field", sort_field)

        return cmd

    @classmethod
    def get_scan_config_nvt(cls, nvt_oid: str) -> Request:
        """Request a single nvt

        Args:
            nvt_oid: OID of an existing nvt
        """
        cmd = XmlCommand("get_nvts")

        if not nvt_oid:
            raise RequiredArgument(
                function=cls.get_scan_config_nvt.__name__, argument="nvt_oid"
            )

        cmd.set_attribute("nvt_oid", nvt_oid)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        cmd.set_attribute("preferences", "1")
        cmd.set_attribute("preference_count", "1")

        return cmd

    @classmethod
    def get_nvts(
        cls,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        name: Optional[str] = None,
        details: Optional[bool] = None,
        extended: Optional[bool] = None,
        preferences: Optional[bool] = None,
        preference_count: Optional[bool] = None,
        timeout: Optional[bool] = None,
        config_id: Optional[str] = None,
        preferences_config_id: Optional[str] = None,
        family: Optional[str] = None,
        sort_order: Optional[str] = None,
        sort_field: Optional[str] = None,
    ) -> Request:
        """Request a list of NVTs

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            name: Name or identifier of the requested information
            details: Whether to include information about references to this
                information
            extended: Whether to receive extended NVT information
                (calls get_nvts, instead of get_info)
            preferences: Whether to include NVT preferences (only for extended)
            preference_count: Whether to include preference count (only for extended)
            timeout: Whether to include the special timeout preference (only for extended)
            config_id: UUID of scan config to which to limit the NVT listing (only for extended)
            preferences_config_id: UUID of scan config to use for preference
                values (only for extended)
            family: Family to which to limit NVT listing (only for extended)
            sort_order: Sort order (only for extended)
            sort_field: Sort field (only for extended)
        """
        if extended:
            return cls.get_scan_config_nvts(
                details=details,
                preferences=preferences,
                preference_count=preference_count,
                timeout=timeout,
                config_id=config_id,
                preferences_config_id=preferences_config_id,
                family=family,
                sort_order=sort_order,
                sort_field=sort_field,
            )

        cmd = XmlCommand("get_info")

        cmd.set_attribute("type", "NVT")

        cmd.add_filter(filter_string, filter_id)

        if name:
            cmd.set_attribute("name", name)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return cmd

    @classmethod
    def get_nvt(
        cls, nvt_id: str, *, extended: Optional[bool] = None
    ) -> Request:
        """Request a single NVT

        Args:
            nvt_id: ID of an existing NVT
            extended: Whether to receive extended NVT information
                (calls get_nvts, instead of get_info)
        """
        if not nvt_id:
            raise RequiredArgument(
                function=cls.get_nvt.__name__, argument="nvt_id"
            )

        if extended:
            return cls.get_scan_config_nvt(nvt_id)

        cmd = XmlCommand("get_info")
        cmd.set_attribute("info_id", nvt_id)

        cmd.set_attribute("type", "NVT")

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return cmd

    @staticmethod
    def get_nvt_preferences(
        *,
        nvt_oid: Optional[str] = None,
    ) -> Request:
        """Request a list of preferences

        The preference element includes just the
        name and value, with the NVT and type built into the name.

        Args:
            nvt_oid: OID of nvt
        """
        cmd = XmlCommand("get_preferences")

        if nvt_oid:
            cmd.set_attribute("nvt_oid", nvt_oid)

        return cmd

    @classmethod
    def get_nvt_preference(
        cls,
        name: str,
        *,
        nvt_oid: Optional[str] = None,
    ) -> Request:
        """Request a nvt preference

        Args:
            name: name of a particular preference
            nvt_oid: OID of nvt
            config_id: UUID of scan config of which to show preference values
        """
        cmd = XmlCommand("get_preferences")

        if not name:
            raise RequiredArgument(
                function=cls.get_nvt_preference.__name__, argument="name"
            )

        cmd.set_attribute("preference", name)

        if nvt_oid:
            cmd.set_attribute("nvt_oid", nvt_oid)

        return cmd
