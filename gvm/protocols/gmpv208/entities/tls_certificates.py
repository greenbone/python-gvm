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


from typing import Any, Optional

from gvm.errors import RequiredArgument
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class TLSCertificateMixin:
    def clone_tls_certificate(self, tls_certificate_id: str) -> Any:
        """Modifies an existing TLS certificate.

        Arguments:
            tls_certificate_id: The UUID of an existing TLS certificate

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tls_certificate_id:
            raise RequiredArgument(
                function=self.clone_tls_certificate.__name__,
                argument="tls_certificate_id",
            )

        cmd = XmlCommand("create_tls_certificate")

        cmd.add_element("copy", tls_certificate_id)

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
                function=self.create_tls_certificate.__name__, argument="name"
            )
        if not certificate:
            raise RequiredArgument(
                function=self.create_tls_certificate.__name__,
                argument="certificate",
            )

        cmd = XmlCommand("create_tls_certificate")

        if comment:
            cmd.add_element("comment", comment)

        cmd.add_element("name", name)
        cmd.add_element("certificate", certificate)

        if trust:
            cmd.add_element("trust", to_bool(trust))

        return self._send_xml_command(cmd)

    def delete_tls_certificate(self, tls_certificate_id: str) -> Any:
        """Deletes an existing tls certificate

        Arguments:
            tls_certificate_id: UUID of the tls certificate to be deleted.
        """
        if not tls_certificate_id:
            raise RequiredArgument(
                function=self.delete_tls_certificate.__name__,
                argument="tls_certificate_id",
            )

        cmd = XmlCommand("delete_tls_certificate")
        cmd.set_attribute("tls_certificate_id", tls_certificate_id)

        return self._send_xml_command(cmd)

    def get_tls_certificates(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        include_certificate_data: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of TLS certificates

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            include_certificate_data: Whether to include the certificate data in
                the response
            details: Whether to include additional details of the
                tls certificates

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        cmd = XmlCommand("get_tls_certificates")

        add_filter(cmd, filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if include_certificate_data is not None:
            cmd.set_attribute(
                "include_certificate_data", to_bool(include_certificate_data)
            )

        return self._send_xml_command(cmd)

    def get_tls_certificate(self, tls_certificate_id: str) -> Any:
        """Request a single TLS certificate

        Arguments:
            tls_certificate_id: UUID of an existing TLS certificate

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tls_certificates")

        if not tls_certificate_id:
            raise RequiredArgument(
                function=self.get_tls_certificate.__name__,
                argument="tls_certificate_id",
            )

        cmd.set_attribute("tls_certificate_id", tls_certificate_id)

        # for single tls certificate always request cert data
        cmd.set_attribute("include_certificate_data", "1")

        # for single entity always request all details
        cmd.set_attribute("details", "1")

        return self._send_xml_command(cmd)

    def modify_tls_certificate(
        self,
        tls_certificate_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        trust: Optional[bool] = None,
    ) -> Any:
        """Modifies an existing TLS certificate.

        Arguments:
            tls_certificate_id: UUID of the TLS certificate to be modified.
            name: Name of the TLS certificate, defaulting to the MD5 fingerprint
            comment: Comment for the TLS certificate.
            trust: Whether the certificate is trusted.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tls_certificate_id:
            raise RequiredArgument(
                function=self.modify_tls_certificate.__name__,
                argument="tls_certificate_id",
            )

        cmd = XmlCommand("modify_tls_certificate")
        cmd.set_attribute("tls_certificate_id", str(tls_certificate_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if trust:
            cmd.add_element("trust", to_bool(trust))

        return self._send_xml_command(cmd)
