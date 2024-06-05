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


class InfoType(Enum):
    """Enum for info types"""

    CERT_BUND_ADV = "CERT_BUND_ADV"
    CPE = "CPE"
    CVE = "CVE"
    DFN_CERT_ADV = "DFN_CERT_ADV"
    OVALDEF = "OVALDEF"
    NVT = "NVT"


class SecInfo:
    @classmethod
    def get_info(cls, info_id: EntityID, info_type: InfoType) -> Request:
        """Request a single secinfo

        Arguments:
            info_id: ID of an existing secinfo
            info_type: Type must be either CERT_BUND_ADV, CPE, CVE,
                DFN_CERT_ADV, OVALDEF, NVT
        """
        if not info_type:
            raise RequiredArgument(
                function=cls.get_info.__name__, argument="info_type"
            )

        if not isinstance(info_type, InfoType):
            info_type = InfoType(info_type)

        if not info_id:
            raise RequiredArgument(
                function=cls.get_info.__name__, argument="info_id"
            )

        cmd = XmlCommand("get_info")
        cmd.set_attribute("info_id", str(info_id))

        cmd.set_attribute("type", info_type.value)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return cmd

    @classmethod
    def get_info_list(
        cls,
        info_type: InfoType,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        name: Optional[str] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of security information

        Args:
            info_type: Type must be either CERT_BUND_ADV, CPE, CVE,
                DFN_CERT_ADV, OVALDEF or NVT
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            name: Name or identifier of the requested information
            details: Whether to include information about references to this
                information
        """
        if not info_type:
            raise RequiredArgument(
                function=cls.get_info_list.__name__, argument="info_type"
            )

        if not isinstance(info_type, InfoType):
            info_type = InfoType(info_type)

        cmd = XmlCommand("get_info")

        cmd.set_attribute("type", info_type.value)

        cmd.add_filter(filter_string, filter_id)

        if name:
            cmd.set_attribute("name", name)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return cmd
