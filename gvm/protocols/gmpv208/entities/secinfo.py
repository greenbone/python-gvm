# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
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
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class InfoType(Enum):
    """Enum for info types"""

    CERT_BUND_ADV = "CERT_BUND_ADV"
    CPE = "CPE"
    CVE = "CVE"
    DFN_CERT_ADV = "DFN_CERT_ADV"
    OVALDEF = "OVALDEF"
    NVT = "NVT"

    @classmethod
    def from_string(cls, info_type: Optional[str]) -> Optional["InfoType"]:
        """Convert a info type string to an actual InfoType instance

        Arguments:
            info_type: Info type string to convert to a InfoType
        """
        if not info_type:
            return None
        try:
            return cls[info_type.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="info_type", function=cls.from_string.__name__
            ) from None


class SecInfoMixin:
    def get_nvt_families(self, *, sort_order: Optional[str] = None):
        """Request a list of nvt families

        Arguments:
            sort_order: Sort order

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_nvt_families")

        if sort_order:
            cmd.set_attribute("sort_order", sort_order)

        return self._send_xml_command(cmd)

    def get_scan_config_nvts(
        self,
        *,
        details: Optional[bool] = None,
        preferences: Optional[bool] = None,
        preference_count: Optional[bool] = None,
        timeout: Optional[bool] = None,
        config_id: Optional[str] = None,
        preferences_config_id: Optional[str] = None,
        family: Optional[str] = None,
        sort_order: Optional[str] = None,
        sort_field: Optional[str] = None,
    ):
        """Request a list of nvts

        Arguments:
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

        Returns:
            The response. See :py:meth:`send_command` for details.
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
            cmd.set_attribute("config_id", config_id)

        if preferences_config_id:
            cmd.set_attribute("preferences_config_id", preferences_config_id)

        if family:
            cmd.set_attribute("family", family)

        if sort_order:
            cmd.set_attribute("sort_order", sort_order)

        if sort_field:
            cmd.set_attribute("sort_field", sort_field)

        return self._send_xml_command(cmd)

    def get_scan_config_nvt(self, nvt_oid: str):
        """Request a single nvt

        Arguments:
            nvt_oid: OID of an existing nvt

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_nvts")

        if not nvt_oid:
            raise RequiredArgument(
                function=self.get_scan_config_nvt.__name__, argument="nvt_oid"
            )

        cmd.set_attribute("nvt_oid", nvt_oid)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        cmd.set_attribute("preferences", "1")
        cmd.set_attribute("preference_count", "1")
        return self._send_xml_command(cmd)

    def get_cves(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        name: Optional[str] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of CVEs

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            name: Name or identifier of the requested information
            details: Whether to include information about references to this
                information

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        return self.get_info_list(
            info_type=InfoType.CVE,
            filter_string=filter_string,
            filter_id=filter_id,
            name=name,
            details=details,
        )

    def get_cpes(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        name: Optional[str] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of CPEs

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            name: Name or identifier of the requested information
            details: Whether to include information about references to this
                information

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        return self.get_info_list(
            info_type=InfoType.CPE,
            filter_string=filter_string,
            filter_id=filter_id,
            name=name,
            details=details,
        )

    def get_nvts(
        self,
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
    ) -> Any:
        """Request a list of NVTs

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            name: Name or identifier of the requested information
            details: Whether to include information about references to this
                information
            extended: Whether to receive extended NVT information
                (calls get_nvts, instead of get_info)
            preferences: Whether to include NVT preferences
            preference_count: Whether to include preference count
            timeout: Whether to include the special timeout preference
            config_id: UUID of scan config to which to limit the NVT listing
            preferences_config_id: UUID of scan config to use for preference
                values
            family: Family to which to limit NVT listing
            sort_order: Sort order
            sort_field: Sort field

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        if extended:
            return self._get_nvt_details(
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

        return self.get_info_list(
            info_type=InfoType.NVT,
            filter_string=filter_string,
            filter_id=filter_id,
            name=name,
            details=details,
        )

    def _get_nvt_details(
        self,
        *,
        details: Optional[bool] = None,
        preferences: Optional[bool] = None,
        preference_count: Optional[bool] = None,
        timeout: Optional[bool] = None,
        config_id: Optional[str] = None,
        preferences_config_id: Optional[str] = None,
        family: Optional[str] = None,
        sort_order: Optional[str] = None,
        sort_field: Optional[str] = None,
    ):
        """Request a list of NVTs with extended details
        Arguments:
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
        Returns:
            The response. See :py:meth:`send_command` for details.
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
            cmd.set_attribute("config_id", config_id)

        if preferences_config_id:
            cmd.set_attribute("preferences_config_id", preferences_config_id)

        if family:
            cmd.set_attribute("family", family)

        if sort_order:
            cmd.set_attribute("sort_order", sort_order)

        if sort_field:
            cmd.set_attribute("sort_field", sort_field)

        return self._send_xml_command(cmd)

    def get_dfn_cert_advisories(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        name: Optional[str] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of DFN-CERT Advisories

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            name: Name or identifier of the requested information
            details: Whether to include information about references to this
                information

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        return self.get_info_list(
            info_type=InfoType.DFN_CERT_ADV,
            filter_string=filter_string,
            filter_id=filter_id,
            name=name,
            details=details,
        )

    def get_cert_bund_advisories(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        name: Optional[str] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of CERT-BUND Advisories

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            name: Name or identifier of the requested information
            details: Whether to include information about references to this
                information

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        return self.get_info_list(
            info_type=InfoType.CERT_BUND_ADV,
            filter_string=filter_string,
            filter_id=filter_id,
            name=name,
            details=details,
        )

    def get_oval_definitions(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        name: Optional[str] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of OVAL definitions

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            name: Name or identifier of the requested information
            details: Whether to include information about references to this
                information

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        return self.get_info_list(
            info_type=InfoType.OVALDEF,
            filter_string=filter_string,
            filter_id=filter_id,
            name=name,
            details=details,
        )

    def get_info_list(
        self,
        info_type: InfoType,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        name: Optional[str] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of security information

        Arguments:
            info_type: Type must be either CERT_BUND_ADV, CPE, CVE,
                DFN_CERT_ADV, OVALDEF or NVT
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            name: Name or identifier of the requested information
            details: Whether to include information about references to this
                information

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not info_type:
            raise RequiredArgument(
                function=self.get_info_list.__name__, argument="info_type"
            )

        if not isinstance(info_type, InfoType):
            raise InvalidArgumentType(
                function=self.get_info_list.__name__,
                argument="info_type",
                arg_type=InfoType.__name__,
            )

        cmd = XmlCommand("get_info")

        cmd.set_attribute("type", info_type.value)

        add_filter(cmd, filter_string, filter_id)

        if name:
            cmd.set_attribute("name", name)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return self._send_xml_command(cmd)

    def get_cve(self, cve_id: str) -> Any:
        """Request a single CVE

        Arguments:
            cve_id: ID of an existing CVE

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        return self.get_info(cve_id, InfoType.CVE)

    def get_cpe(self, cpe_id: str) -> Any:
        """Request a single CPE

        Arguments:
            cpe_id: ID of an existing CPE

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        return self.get_info(cpe_id, InfoType.CPE)

    def get_nvt(self, nvt_id: str, *, extended: Optional[bool] = None) -> Any:
        """Request a single NVT

        Arguments:
            nvt_id: ID of an existing NVT
            extended: Whether to receive extended NVT information
                (calls get_nvts, instead of get_info)

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        if extended:
            cmd = XmlCommand("get_nvts")

            if not nvt_id:
                raise RequiredArgument(
                    function=self.get_nvt.__name__, argument="nvt_oid"
                )

            cmd.set_attribute("nvt_oid", nvt_id)

            # for single entity always request all details
            cmd.set_attribute("details", "1")
            cmd.set_attribute("preferences", "1")
            cmd.set_attribute("preference_count", "1")
            return self._send_xml_command(cmd)

        return self.get_info(nvt_id, InfoType.NVT)

    def get_dfn_cert_advisory(self, cert_id: str) -> Any:
        """Request a single DFN-CERT Advisory

        Arguments:
            cert_id: ID of an existing DFN-CERT Advisory

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        return self.get_info(cert_id, InfoType.DFN_CERT_ADV)

    def get_cert_bund_advisory(self, cert_id: str) -> Any:
        """Request a single CERT-BUND Advisory

        Arguments:
            cert_id: ID of an existing CERT-BUND Advisory

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        return self.get_info(cert_id, InfoType.CERT_BUND_ADV)

    def get_oval_definition(self, oval_id: str) -> Any:
        """Request a single Oval definition

        Arguments:
            oval_id: ID of an existing Oval definition

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        return self.get_info(oval_id, InfoType.OVALDEF)

    def get_info(self, info_id: str, info_type: InfoType) -> Any:
        """Request a single secinfo

        Arguments:
            info_id: ID of an existing secinfo
            info_type: Type must be either CERT_BUND_ADV, CPE, CVE,
                DFN_CERT_ADV, OVALDEF, NVT

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not info_type:
            raise RequiredArgument(
                function=self.get_info.__name__, argument="info_type"
            )

        if not isinstance(info_type, InfoType):
            raise InvalidArgumentType(
                function=self.get_info.__name__,
                argument="info_type",
                arg_type=InfoType.__name__,
            )

        if not info_id:
            raise RequiredArgument(
                function=self.get_info.__name__, argument="info_id"
            )

        cmd = XmlCommand("get_info")
        cmd.set_attribute("info_id", info_id)

        cmd.set_attribute("type", info_type.value)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_nvt_preferences(
        self,
        *,
        nvt_oid: Optional[str] = None,
    ) -> Any:
        """Request a list of preferences

        The preference element includes just the
        name and value, with the NVT and type built into the name.

        Arguments:
            nvt_oid: OID of nvt

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_preferences")

        if nvt_oid:
            cmd.set_attribute("nvt_oid", nvt_oid)

        return self._send_xml_command(cmd)

    def get_nvt_preference(
        self,
        name: str,
        *,
        nvt_oid: Optional[str] = None,
    ) -> Any:
        """Request a nvt preference

        Arguments:
            name: name of a particular preference
            nvt_oid: OID of nvt
            config_id: UUID of scan config of which to show preference values

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_preferences")

        if not name:
            raise RequiredArgument(
                function=self.get_nvt_preference.__name__, argument="name"
            )

        cmd.set_attribute("preference", name)

        if nvt_oid:
            cmd.set_attribute("nvt_oid", nvt_oid)

        return self._send_xml_command(cmd)
