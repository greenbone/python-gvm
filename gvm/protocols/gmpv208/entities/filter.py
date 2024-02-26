# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Any, Optional

from gvm._enum import Enum
from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


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

        Arguments:
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


class FiltersMixin:
    def clone_filter(self, filter_id: str) -> Any:
        """Clone an existing filter

        Arguments:
            filter_id: UUID of an existing filter to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not filter_id:
            raise RequiredArgument(
                function=self.clone_filter.__name__, argument="filter_id"
            )

        cmd = XmlCommand("create_filter")
        cmd.add_element("copy", filter_id)
        return self._send_xml_command(cmd)

    def create_filter(
        self,
        name: str,
        *,
        filter_type: Optional[FilterType] = None,
        comment: Optional[str] = None,
        term: Optional[str] = None,
    ) -> Any:
        """Create a new filter

        Arguments:
            name: Name of the new filter
            filter_type: Filter for entity type
            comment: Comment for the filter
            term: Filter term e.g. 'name=foo'

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_filter.__name__, argument="name"
            )

        cmd = XmlCommand("create_filter")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if term:
            cmd.add_element("term", term)

        if filter_type:
            if not isinstance(filter_type, FilterType):
                raise InvalidArgumentType(
                    function=self.create_filter.__name__,
                    argument="filter_type",
                    arg_type=FilterType.__name__,
                )

            cmd.add_element("type", filter_type.value)

        return self._send_xml_command(cmd)

    def delete_filter(
        self, filter_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing filter

        Arguments:
            filter_id: UUID of the filter to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not filter_id:
            raise RequiredArgument(
                function=self.delete_filter.__name__, argument="filter_id"
            )

        cmd = XmlCommand("delete_filter")
        cmd.set_attribute("filter_id", filter_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_filters(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        alerts: Optional[bool] = None,
    ) -> Any:
        """Request a list of filters

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan filters instead
            alerts: Whether to include list of alerts that use the filter.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_filters")

        add_filter(cmd, filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if alerts is not None:
            cmd.set_attribute("alerts", to_bool(alerts))

        return self._send_xml_command(cmd)

    def get_filter(
        self, filter_id: str, *, alerts: Optional[bool] = None
    ) -> Any:
        """Request a single filter

        Arguments:
            filter_id: UUID of an existing filter
            alerts: Whether to include list of alerts that use the filter.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_filters")

        if not filter_id:
            raise RequiredArgument(
                function=self.get_filter.__name__, argument="filter_id"
            )

        cmd.set_attribute("filter_id", filter_id)

        if alerts is not None:
            cmd.set_attribute("alerts", to_bool(alerts))

        return self._send_xml_command(cmd)

    def modify_filter(
        self,
        filter_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        term: Optional[str] = None,
        filter_type: Optional[FilterType] = None,
    ) -> Any:
        """Modifies an existing filter.

        Arguments:
            filter_id: UUID of the filter to be modified
            comment: Comment on filter.
            name: Name of filter.
            term: Filter term.
            filter_type: Resource type filter applies to.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not filter_id:
            raise RequiredArgument(
                function=self.modify_filter.__name__, argument="filter_id"
            )

        cmd = XmlCommand("modify_filter")
        cmd.set_attribute("filter_id", filter_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if term:
            cmd.add_element("term", term)

        if filter_type:
            if not isinstance(filter_type, FilterType):
                raise InvalidArgumentType(
                    function=self.modify_filter.__name__,
                    argument="filter_type",
                    arg_type=FilterType.__name__,
                )
            cmd.add_element("type", filter_type.value)

        return self._send_xml_command(cmd)
