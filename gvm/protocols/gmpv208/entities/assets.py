# -*- coding: utf-8 -*-
# Copyright (C) 2021 Greenbone Networks GmbH
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

# pylint:  disable=redefined-builtin

from enum import Enum
from typing import Any, Optional

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class AssetType(Enum):
    """ "Enum for asset types"""

    OPERATING_SYSTEM = 'os'
    HOST = 'host'


def get_asset_type_from_string(
    asset_type: Optional[str],
) -> Optional[AssetType]:
    if not asset_type:
        return None

    if asset_type == 'os':
        return AssetType.OPERATING_SYSTEM

    try:
        return AssetType[asset_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='asset_type', function=get_asset_type_from_string.__name__
        ) from None


class AssetsMixin:
    """AssetsMixin contains Hosts, OperatingSystems and TLSCertificates"""

    def create_host(self, name: str, *, comment: Optional[str] = None) -> Any:
        """Create a new host asset

        Arguments:
            name: Name for the new host asset
            comment: Comment for the new host asset

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_host.__name__, argument='name'
            )

        cmd = XmlCommand("create_asset")
        asset = cmd.add_element("asset")
        asset.add_element("type", "host")  # ignored for gmp7, required for gmp8
        asset.add_element("name", name)

        if comment:
            asset.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def create_tls_certificate(
        self,
        name: str,
        certificate: str,
        *,
        comment: Optional[str] = None,
        trust: Optional[bool] = None,
    ) -> Any:
        """Create a new TLS certificate

        Arguments:
            name: Name of the TLS certificate, defaulting to the MD5
                fingerprint.
            certificate: The Base64 encoded certificate data (x.509 DER or PEM).
            comment: Comment for the TLS certificate.
            trust: Whether the certificate is trusted.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_tls_certificate.__name__, argument='name'
            )
        if not certificate:
            raise RequiredArgument(
                function=self.create_tls_certificate.__name__,
                argument='certificate',
            )

        cmd = XmlCommand("create_tls_certificate")

        if comment:
            cmd.add_element("comment", comment)

        cmd.add_element("name", name)
        cmd.add_element("certificate", certificate)

        if trust:
            cmd.add_element("trust", to_bool(trust))

        return self._send_xml_command(cmd)

    def delete_asset(
        self, *, asset_id: Optional[str] = None, report_id: Optional[str] = None
    ) -> Any:
        """Deletes an existing asset

        Arguments:
            asset_id: UUID of the single asset to delete.
            report_id: UUID of report from which to get all
                assets to delete.
        """
        if not asset_id and not report_id:
            raise RequiredArgument(
                function=self.delete_asset.__name__,
                argument='asset_id or report_id',
            )

        cmd = XmlCommand("delete_asset")
        if asset_id:
            cmd.set_attribute("asset_id", asset_id)
        else:
            cmd.set_attribute("report_id", report_id)

        return self._send_xml_command(cmd)

    def get_assets(
        self,
        asset_type: AssetType,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
    ) -> Any:
        """Request a list of assets

        Arguments:
            asset_type: Either 'os' or 'host'
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not isinstance(asset_type, AssetType):
            raise InvalidArgumentType(
                function=self.get_assets.__name__,
                argument='asset_type',
                arg_type=AssetType.__name__,
            )

        cmd = XmlCommand("get_assets")

        cmd.set_attribute("type", asset_type.value)

        add_filter(cmd, filter, filter_id)

        return self._send_xml_command(cmd)

    def get_asset(self, asset_id: str, asset_type: AssetType) -> Any:
        """Request a single asset

        Arguments:
            asset_id: UUID of an existing asset
            asset_type: Either 'os' or 'host'

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_assets")

        if not isinstance(asset_type, AssetType):
            raise InvalidArgumentType(
                function=self.get_asset.__name__,
                argument='asset_type',
                arg_type=AssetType.__name__,
            )

        if not asset_id:
            raise RequiredArgument(
                function=self.get_asset.__name__, argument='asset_id'
            )

        cmd.set_attribute("asset_id", asset_id)
        cmd.set_attribute("type", asset_type.value)

        return self._send_xml_command(cmd)

    def modify_asset(self, asset_id: str, comment: Optional[str] = "") -> Any:
        """Modifies an existing asset.

        Arguments:
            asset_id: UUID of the asset to be modified.
            comment: Comment for the asset.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not asset_id:
            raise RequiredArgument(
                function=self.modify_asset.__name__, argument='asset_id'
            )

        cmd = XmlCommand("modify_asset")
        cmd.set_attribute("asset_id", asset_id)
        cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)
