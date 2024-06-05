# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class TLSCertificates:
    @classmethod
    def clone_tls_certificate(cls, tls_certificate_id: EntityID) -> Request:
        """Modifies an existing TLS certificate.

        Args:
            tls_certificate_id: The UUID of an existing TLS certificate
        """
        if not tls_certificate_id:
            raise RequiredArgument(
                function=cls.clone_tls_certificate.__name__,
                argument="tls_certificate_id",
            )

        cmd = XmlCommand("create_tls_certificate")

        cmd.add_element("copy", str(tls_certificate_id))

        return cmd

    @classmethod
    def create_tls_certificate(
        cls,
        name: str,
        certificate: str,
        *,
        comment: Optional[str] = None,
        trust: Optional[bool] = None,
    ) -> Request:
        """Create a new TLS certificate

        Args:
            name: Name of the TLS certificate, defaulting to the MD5
                fingerprint.
            certificate: The Base64 encoded certificate data (x.509 DER or PEM).
            comment: Comment for the TLS certificate.
            trust: Whether the certificate is trusted.
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_tls_certificate.__name__, argument="name"
            )
        if not certificate:
            raise RequiredArgument(
                function=cls.create_tls_certificate.__name__,
                argument="certificate",
            )

        cmd = XmlCommand("create_tls_certificate")

        cmd.add_element("name", name)
        cmd.add_element("certificate", certificate)

        if comment:
            cmd.add_element("comment", comment)

        if trust is not None:
            cmd.add_element("trust", to_bool(trust))

        return cmd

    @classmethod
    def delete_tls_certificate(cls, tls_certificate_id: EntityID) -> Request:
        """Deletes an existing tls certificate

        Args:
            tls_certificate_id: UUID of the tls certificate to be deleted.
        """
        if not tls_certificate_id:
            raise RequiredArgument(
                function=cls.delete_tls_certificate.__name__,
                argument="tls_certificate_id",
            )

        cmd = XmlCommand("delete_tls_certificate")
        cmd.set_attribute("tls_certificate_id", str(tls_certificate_id))
        return cmd

    @staticmethod
    def get_tls_certificates(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        include_certificate_data: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of TLS certificates

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            include_certificate_data: Whether to include the certificate data in
                the response
            details: Whether to include additional details of the
                tls certificates
        """
        cmd = XmlCommand("get_tls_certificates")

        cmd.add_filter(filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if include_certificate_data is not None:
            cmd.set_attribute(
                "include_certificate_data", to_bool(include_certificate_data)
            )

        return cmd

    @classmethod
    def get_tls_certificate(cls, tls_certificate_id: EntityID) -> Request:
        """Request a single TLS certificate

        Args:
            tls_certificate_id: UUID of an existing TLS certificate
        """
        cmd = XmlCommand("get_tls_certificates")

        if not tls_certificate_id:
            raise RequiredArgument(
                function=cls.get_tls_certificate.__name__,
                argument="tls_certificate_id",
            )

        cmd.set_attribute("tls_certificate_id", str(tls_certificate_id))

        # for single tls certificate always request cert data
        cmd.set_attribute("include_certificate_data", "1")

        # for single entity always request all details
        cmd.set_attribute("details", "1")

        return cmd

    @classmethod
    def modify_tls_certificate(
        cls,
        tls_certificate_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        trust: Optional[bool] = None,
    ) -> Request:
        """Modifies an existing TLS certificate.

        Args:
            tls_certificate_id: UUID of the TLS certificate to be modified.
            name: Name of the TLS certificate, defaulting to the MD5 fingerprint
            comment: Comment for the TLS certificate.
            trust: Whether the certificate is trusted.
        """
        if not tls_certificate_id:
            raise RequiredArgument(
                function=cls.modify_tls_certificate.__name__,
                argument="tls_certificate_id",
            )

        cmd = XmlCommand("modify_tls_certificate")
        cmd.set_attribute("tls_certificate_id", str(tls_certificate_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if trust is not None:
            cmd.add_element("trust", to_bool(trust))

        return cmd
