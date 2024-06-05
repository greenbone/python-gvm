# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm._enum import Enum
from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class FilterType(Enum):
    """Enum for filter types"""

    ALERT = "alert"
    ASSET = "asset"
    SCAN_CONFIG = "config"
    CREDENTIAL = "credential"
    FILTER = "filter"
    GROUP = "group"
    HOST = "host"
    NOTE = "note"
    OPERATING_SYSTEM = "os"
    OVERRIDE = "override"
    PERMISSION = "permission"
    PORT_LIST = "port_list"
    REPORT = "report"
    REPORT_FORMAT = "report_format"
    RESULT = "result"
    ROLE = "role"
    SCHEDULE = "schedule"
    ALL_SECINFO = "secinfo"
    TAG = "tag"
    TARGET = "target"
    TASK = "task"
    TICKET = "ticket"
    TLS_CERTIFICATE = "tls_certificate"
    USER = "user"
    VULNERABILITY = "vuln"

    @classmethod
    def from_string(
        cls,
        filter_type: Optional[str],
    ) -> Optional["FilterType"]:
        """Convert a filter type string to an actual FilterType instance

        Args:
            filter_type (str): Filter type string to convert to a FilterType
        """
        if filter_type == "vuln":
            return cls.VULNERABILITY

        if filter_type == "os":
            return cls.OPERATING_SYSTEM

        if filter_type == "config":
            return cls.SCAN_CONFIG

        if filter_type == "secinfo":
            return cls.ALL_SECINFO

        return super().from_string(filter_type)


class Filters:
    @classmethod
    def clone_filter(cls, filter_id: EntityID) -> Request:
        """Clone a filter

        Args:
            filter_id: ID of the filter to clone
        """
        if not filter_id:
            raise RequiredArgument(
                function=cls.clone_filter.__name__, argument="filter_id"
            )

        cmd = XmlCommand("create_filter")
        cmd.add_element("copy", str(filter_id))
        return cmd

    @classmethod
    def create_filter(
        cls,
        name: str,
        *,
        filter_type: Optional[FilterType] = None,
        comment: Optional[str] = None,
        term: Optional[str] = None,
    ) -> Request:
        """Create a new filter

        Args:
            name: Name of the new filter
            filter_type: Filter for entity type
            comment: Comment for the filter
            term: Filter term e.g. 'name=foo'
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_filter.__name__, argument="name"
            )

        cmd = XmlCommand("create_filter")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if term:
            cmd.add_element("term", term)

        if filter_type:
            if not isinstance(filter_type, FilterType):
                filter_type = FilterType(filter_type)

            cmd.add_element("type", filter_type.value)

        return cmd

    @classmethod
    def delete_filter(
        cls, filter_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Deletes an existing filter

        Args:
            filter_id: UUID of the filter to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not filter_id:
            raise RequiredArgument(
                function=cls.delete_filter.__name__, argument="filter_id"
            )

        cmd = XmlCommand("delete_filter")
        cmd.set_attribute("filter_id", str(filter_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @staticmethod
    def get_filters(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        alerts: Optional[bool] = None,
    ) -> Request:
        """Request a list of filters

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan filters instead
            alerts: Whether to include list of alerts that use the filter.
        """
        cmd = XmlCommand("get_filters")

        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if alerts is not None:
            cmd.set_attribute("alerts", to_bool(alerts))

        return cmd

    @classmethod
    def get_filter(
        cls, filter_id: EntityID, *, alerts: Optional[bool] = None
    ) -> Request:
        """Request a single filter

        Args:
            filter_id: UUID of an existing filter
            alerts: Whether to include list of alerts that use the filter.
        """
        cmd = XmlCommand("get_filters")

        if not filter_id:
            raise RequiredArgument(
                function=cls.get_filter.__name__, argument="filter_id"
            )

        cmd.set_attribute("filter_id", str(filter_id))

        if alerts is not None:
            cmd.set_attribute("alerts", to_bool(alerts))

        return cmd

    @classmethod
    def modify_filter(
        cls,
        filter_id: EntityID,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        term: Optional[str] = None,
        filter_type: Optional[FilterType] = None,
    ) -> Request:
        """Modifies an existing filter.

        Args:
            filter_id: UUID of the filter to be modified
            comment: Comment on filter.
            name: Name of filter.
            term: Filter term.
            filter_type: Resource type filter applies to.
        """
        if not filter_id:
            raise RequiredArgument(
                function=cls.modify_filter.__name__, argument="filter_id"
            )

        cmd = XmlCommand("modify_filter")
        cmd.set_attribute("filter_id", str(filter_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if term:
            cmd.add_element("term", term)

        if filter_type:
            if not isinstance(filter_type, FilterType):
                filter_type = FilterType(filter_type)

            cmd.add_element("type", filter_type.value)

        return cmd
