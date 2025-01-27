# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm._enum import Enum
from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class ResourceType(Enum):
    """Enum for resource types"""

    ALERT = "ALERT"
    AUDIT = "TASK"
    AUDIT_REPORT = "REPORT"
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
    REPORT_CONFIG = "REPORT_CONFIG"
    RESULT = "RESULT"
    ROLE = "ROLE"
    SCANNER = "SCANNER"
    SCHEDULE = "SCHEDULE"
    TARGET = "TARGET"
    TASK = "TASK"
    TLS_CERTIFICATE = "TLS_CERTIFICATE"
    USER = "USER"


class ResourceNames:
    @classmethod
    def get_resource_names(
        cls,
        resource_type: Union[ResourceType, str],
        *,
        filter_string: Optional[str] = None,
    ) -> Request:
        """Request a list of resource names and IDs

        Args:
            resource_type: Type must be either ALERT, CERT_BUND_ADV,
                CONFIG, CPE, CREDENTIAL, CVE, DFN_CERT_ADV, FILTER,
                GROUP, HOST, NOTE, NVT, OS, OVERRIDE, PERMISSION,
                PORT_LIST, REPORT_FORMAT, REPORT, REPORT_CONFIG, RESULT, ROLE,
                SCANNER, SCHEDULE, TARGET, TASK, TLS_CERTIFICATE
                or USER
            filter_string: Filter term to use for the query
        """
        cmd = XmlCommand("get_resource_names")

        if not resource_type:
            raise RequiredArgument(
                function=cls.get_resource_names.__name__,
                argument="resource_type",
            )

        if not isinstance(resource_type, ResourceType):
            resource_type = ResourceType(resource_type)

        cmd.set_attribute("type", resource_type.value)
        cmd.add_filter(filter_string, None)
        return cmd

    @classmethod
    def get_resource_name(
        cls,
        resource_id: EntityID,
        resource_type: Union[ResourceType, str],
    ) -> Request:
        """Request a single resource name

        Args:
            resource_id: ID of an existing resource
            resource_type: Type must be either ALERT, CERT_BUND_ADV,
                CONFIG, CPE, CREDENTIAL, CVE, DFN_CERT_ADV, FILTER,
                GROUP, HOST, NOTE, NVT, OS, OVERRIDE, PERMISSION,
                PORT_LIST, REPORT_FORMAT, REPORT, REPORT_CONFIG, RESULT, ROLE,
                SCANNER, SCHEDULE, TARGET, TASK, TLS_CERTIFICATE
                or USER
        """
        if not resource_type:
            raise RequiredArgument(
                function=cls.get_resource_name.__name__,
                argument="resource_type",
            )

        if not isinstance(resource_type, ResourceType):
            resource_type = ResourceType(resource_type)

        if not resource_id:
            raise RequiredArgument(
                function=cls.get_resource_name.__name__, argument="resource_id"
            )

        cmd = XmlCommand("get_resource_names")
        cmd.set_attribute("resource_id", str(resource_id))
        cmd.set_attribute("type", resource_type.value)
        return cmd
