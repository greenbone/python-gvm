# -*- coding: utf-8 -*-
# Copyright (C) 2023 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from enum import Enum
from typing import Any, Optional

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.utils import add_filter
from gvm.xml import XmlCommand


class ResourceType(Enum):
    """Enum for resource types"""

    ALERT = "ALERT"
    CERT_BUND_ADV = "CERT_BUND_ADV"
    CONFIG = "CONFIG"
    CPE = "CPE"
    CREDENTIAL = "CREDENTIAL"
    CVE = "CVE"
    DFN_CERT_ADV = "DFN_CERT_ADV"
    FILTER = "FILTER"
    GROUP = "GROUP"
    HOST = "HOST"
    NOTE = "NOTE"
    NVT = "NVT"
    OS = "OS"
    OVERRIDE = "OVERRIDE"
    PERMISSION = "PERMISSION"
    PORT_LIST = "PORT_LIST"
    REPORT_FORMAT = "REPORT_FORMAT"
    REPORT = "REPORT"
    RESULT = "RESULT"
    ROLE = "ROLE"
    SCANNER = "SCANNER"
    SCHEDULE = "SCHEDULE"
    TARGET = "TARGET"
    TASK = "TASK"
    TLS_CERTIFICATE = "TLS_CERTIFICATE"
    USER = "USER"

    @classmethod
    def from_string(
        cls,
        resource_type: Optional[str],
    ) -> Optional["ResourceType"]:
        """Convert a resource type string to an actual ResourceType instance

        Arguments:
            resource_type: Resource type string to convert to a ResourceType
        """
        if not resource_type:
            return None
        try:
            return cls[resource_type.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="resource_type", function=cls.from_string.__name__
            ) from None


class ResourceNamesMixin:
    def get_resource_names_list(
        self,
        resource_type: ResourceType,
        filter_string: Optional[str] = None,
    ) -> Any:
        """Request a list of resource names and IDs

        Arguments:
            resource_type: Type must be either ALERT, CERT_BUND_ADV,
            CONFIG, CPE, CREDENTIAL, CVE, DFN_CERT_ADV, FILTER,
            GROUP, HOST, NOTE, NVT, OS, OVERRIDE, PERMISSION,
            PORT_LIST, REPORT_FORMAT, REPORT, RESULT, ROLE,
            SCANNER, SCHEDULE, TARGET, TASK, TLS_CERTIFICATE
            or USER
            filter_string: Filter term to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not resource_type:
            raise RequiredArgument(
                function=self.get_resource_names_list.__name__,
                argument="resource_type",
            )

        if not isinstance(resource_type, ResourceType):
            raise InvalidArgumentType(
                function=self.get_resource_names_list.__name__,
                argument="resource_type",
                arg_type=ResourceType.__name__,
            )

        cmd = XmlCommand("get_resource_names")

        cmd.set_attribute("type", resource_type.value)

        add_filter(cmd, filter_string, None)

        return self._send_xml_command(cmd)

    def get_resource_name(
        self, resource_id: str, resource_type: ResourceType
    ) -> Any:
        """Request a single resource name

        Arguments:
            resource_id: ID of an existing resource
            resource_type: Type must be either ALERT, CERT_BUND_ADV,
            CONFIG, CPE, CREDENTIAL, CVE, DFN_CERT_ADV, FILTER,
            GROUP, HOST, NOTE, NVT, OS, OVERRIDE, PERMISSION,
            PORT_LIST, REPORT_FORMAT, REPORT, RESULT, ROLE,
            SCANNER, SCHEDULE, TARGET, TASK, TLS_CERTIFICATE
            or USER

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not resource_type:
            raise RequiredArgument(
                function=self.get_resource_name.__name__,
                argument="resource_type",
            )

        if not isinstance(resource_type, ResourceType):
            raise InvalidArgumentType(
                function=self.get_resource_name.__name__,
                argument="resource_type",
                arg_type=ResourceType.__name__,
            )

        if not resource_id:
            raise RequiredArgument(
                function=self.get_resource_name.__name__, argument="resource_id"
            )

        cmd = XmlCommand("get_resource_names")
        cmd.set_attribute("resource_id", resource_id)

        cmd.set_attribute("type", resource_type.value)

        return self._send_xml_command(cmd)
