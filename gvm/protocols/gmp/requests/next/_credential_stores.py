# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from base64 import b64encode
from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class CredentialStores:
    @classmethod
    def get_credential_stores(
        cls,
        *,
        credential_store_id: Optional[EntityID] = None,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of credential stores

        Args:
            credential_store_id: ID of credential store to fetch
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to exclude results
        """

        cmd = XmlCommand("get_credential_stores")
        cmd.add_filter(filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if credential_store_id:
            cmd.add_element("credential_store_id", str(credential_store_id))

        return cmd

    @classmethod
    def modify_credential_store(
        cls,
        credential_store_id: EntityID,
        *,
        active: Optional[bool] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        path: Optional[str] = None,
        app_id: Optional[str] = None,
        client_cert: Optional[str] = None,
        client_key: Optional[str] = None,
        client_pkcs12_file: Optional[str] = None,
        passphrase: Optional[str] = None,
        server_ca_cert: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> Request:
        """Modify a credential store

        Args:
            credential_store_id: ID of credential store to fetch
            active: Whether the credential store is active
            host: The host to use for reaching the credential store
            port: The port to use for reaching the credential store
            path: The URI path the credential store is using
            app_id: Depends on the credential store used. Usually called the same in the credential store
            client_cert: The client certificate to use for authorization, as a plain string
            client_key: The client key to use for authorization, as a plain string
            client_pkcs12_file: The pkcs12 file contents to use for authorization, as a plain string
                (alternative to using client_cert and client_key)
            passphrase: The passphrase to use to decrypt client_pkcs12_file or client_key file
            server_ca_cert: The server certificate, so the credential store can be trusted
            comment: An optional comment to store alongside the credential store
        """

        if not credential_store_id:
            raise RequiredArgument(
                function=cls.verify_credential_store.__name__,
                argument="credential_store_id",
            )

        cmd = XmlCommand("modify_credential_store")
        cmd.set_attribute("credential_store_id", str(credential_store_id))

        if active is not None:
            cmd.add_element("active", to_bool(active))
        if host:
            cmd.add_element("host", host)
        if port:
            cmd.add_element("port", str(port))
        if path:
            cmd.add_element("path", path)
        if comment:
            cmd.add_element("comment", comment)

        preferences = cmd.add_element("preferences")

        if app_id:
            preferences.add_element("app_id", app_id)
        if client_cert:
            preferences.add_element(
                "client_cert",
                b64encode(client_cert.encode("ascii")).decode("ascii"),
            )
        if client_key:
            preferences.add_element(
                "client_key",
                b64encode(client_key.encode("ascii")).decode("ascii"),
            )
        if client_pkcs12_file:
            preferences.add_element(
                "client_pkcs12_file",
                b64encode(client_pkcs12_file.encode("ascii")).decode("ascii"),
            )
        if passphrase:
            preferences.add_element("passphrase", passphrase)
        if server_ca_cert:
            preferences.add_element(
                "server_ca_cert",
                b64encode(server_ca_cert.encode("ascii")).decode("ascii"),
            )

        return cmd

    @classmethod
    def verify_credential_store(
        cls,
        credential_store_id: EntityID,
    ) -> Request:
        """Verify that the connection to a credential store works

        Args:
            credential_store_id: The uuid of the credential store to verify
        """
        if not credential_store_id:
            raise RequiredArgument(
                function=cls.verify_credential_store.__name__,
                argument="credential_store_id",
            )

        cmd = XmlCommand("verify_credential_store")
        cmd.set_attribute("credential_store_id", str(credential_store_id))
        return cmd
