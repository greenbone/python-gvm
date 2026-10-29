# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later


from gvm._enum import Enum
from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.xml import XmlCommand

from .._entity_id import EntityID
from ..v224._credentials import (
    Credentials as CredentialsV224,
)


class CredentialStoreCredentialType(Enum):
    """Enum for credential store credential types"""

    CLIENT_CERTIFICATE = "cs_cc"
    SNMP = "cs_snmp"
    USERNAME_PASSWORD = "cs_up"
    USERNAME_SSH_KEY = "cs_usk"
    SMIME_CERTIFICATE = "cs_smime"
    PGP_ENCRYPTION_KEY = "cs_pgp"
    PASSWORD_ONLY = "cs_pw"


class CredentialType(Enum):
    """Enum for credential types"""

    CLIENT_CERTIFICATE = "cc"
    SNMP = "snmp"
    USERNAME_PASSWORD = "up"
    USERNAME_SSH_KEY = "usk"
    SMIME_CERTIFICATE = "smime"
    PGP_ENCRYPTION_KEY = "pgp"
    PASSWORD_ONLY = "pw"
    ACTIVE_DIRECTORY = "ad"


class Credentials(CredentialsV224):
    @classmethod
    def create_active_directory_credential(
        cls,
        name: str,
        *,
        host: str,
        bind_dn: str,
        base_dn: str,
        bind_password: str,
        tls_mode: str,
        comment: str | None = None,
        port: int | None = None,
        ca_certificate: str | None = None,
    ) -> Request:
        """Create an Active Directory credential.

        Requires AD integration to be enabled in gvmd.

        Args:
            name: Name of the credential.
            host: Active Directory server hostname or IP address.
            bind_dn: Distinguished name used to bind to the directory.
            base_dn: Base distinguished name for directory searches.
            bind_password: Password used to bind to the directory.
            tls_mode: TLS mode, either "ldaps" or "starttls".
            comment: Optional comment for the credential.
            port: Server port (1 to 65535). Omit to use the connector default.
            ca_certificate: Optional CA certificate in PEM format.
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_active_directory_credential.__name__,
                argument="name",
            )

        if not host:
            raise RequiredArgument(
                function=cls.create_active_directory_credential.__name__,
                argument="host",
            )

        if not bind_dn:
            raise RequiredArgument(
                function=cls.create_active_directory_credential.__name__,
                argument="bind_dn",
            )

        if not base_dn:
            raise RequiredArgument(
                function=cls.create_active_directory_credential.__name__,
                argument="base_dn",
            )

        if not bind_password:
            raise RequiredArgument(
                function=cls.create_active_directory_credential.__name__,
                argument="bind_password",
            )

        if not tls_mode:
            raise RequiredArgument(
                function=cls.create_active_directory_credential.__name__,
                argument="tls_mode",
            )

        if tls_mode not in ("ldaps", "starttls"):
            raise InvalidArgument(
                function=cls.create_active_directory_credential.__name__,
                argument="tls_mode",
            )

        if port is not None and (
            not isinstance(port, int) or not 1 <= port <= 65535
        ):
            raise InvalidArgument(
                function=cls.create_active_directory_credential.__name__,
                argument="port",
            )

        cmd = XmlCommand("create_credential")
        cmd.add_element("name", name)
        cmd.add_element("type", CredentialType.ACTIVE_DIRECTORY.value)
        if comment is not None:
            cmd.add_element("comment", comment)
        cmd.add_element("host", host)
        cmd.add_element("bind_dn", bind_dn)
        cmd.add_element("base_dn", base_dn)
        cmd.add_element("bind_password", bind_password)
        cmd.add_element("tls_mode", tls_mode)
        if port is not None:
            cmd.add_element("port", str(port))
        if ca_certificate is not None:
            cmd.add_element("ca_certificate", ca_certificate)
        return cmd

    @classmethod
    def modify_active_directory_credential(
        cls,
        credential_id: EntityID,
        *,
        name: str | None = None,
        comment: str | None = None,
        host: str | None = None,
        bind_dn: str | None = None,
        base_dn: str | None = None,
        bind_password: str | None = None,
        tls_mode: str | None = None,
        port: int | str | None = None,
        ca_certificate: str | None = None,
    ) -> Request:
        """Modify an Active Directory credential.

        Requires AD integration to be enabled in gvmd. Fields set to None
        are left unchanged.

        Args:
            credential_id: UUID of the credential to modify.
            name: New name of the credential.
            comment: New comment. An empty string clears the comment.
            host: Active Directory server hostname or IP address.
            bind_dn: Distinguished name used to bind to the directory.
            base_dn: Base distinguished name for directory searches.
            bind_password: Password used to bind to the directory.
            tls_mode: TLS mode, either "ldaps" or "starttls".
            port: Server port (1 to 65535), or an empty string to restore
                the connector default. Nonempty strings are not accepted.
            ca_certificate: CA certificate in PEM format. An empty string
                clears the certificate.
        """
        if not credential_id:
            raise RequiredArgument(
                function=cls.modify_active_directory_credential.__name__,
                argument="credential_id",
            )

        if name is not None and not name:
            raise RequiredArgument(
                function=cls.modify_active_directory_credential.__name__,
                argument="name",
            )

        if host is not None and not host:
            raise RequiredArgument(
                function=cls.modify_active_directory_credential.__name__,
                argument="host",
            )

        if bind_dn is not None and not bind_dn:
            raise RequiredArgument(
                function=cls.modify_active_directory_credential.__name__,
                argument="bind_dn",
            )

        if base_dn is not None and not base_dn:
            raise RequiredArgument(
                function=cls.modify_active_directory_credential.__name__,
                argument="base_dn",
            )

        if bind_password is not None and not bind_password:
            raise RequiredArgument(
                function=cls.modify_active_directory_credential.__name__,
                argument="bind_password",
            )

        if tls_mode is not None and not tls_mode:
            raise RequiredArgument(
                function=cls.modify_active_directory_credential.__name__,
                argument="tls_mode",
            )

        if tls_mode is not None and tls_mode not in ("ldaps", "starttls"):
            raise InvalidArgument(
                function=cls.modify_active_directory_credential.__name__,
                argument="tls_mode",
            )

        if (
            port is not None
            and port != ""
            and (not isinstance(port, int) or not 1 <= port <= 65535)
        ):
            raise InvalidArgument(
                function=cls.modify_active_directory_credential.__name__,
                argument="port",
            )

        cmd = XmlCommand("modify_credential")
        cmd.set_attribute("credential_id", str(credential_id))
        if name is not None:
            cmd.add_element("name", str(name))
        if comment is not None:
            cmd.add_element("comment", str(comment))
        if host is not None:
            cmd.add_element("host", str(host))
        if bind_dn is not None:
            cmd.add_element("bind_dn", str(bind_dn))
        if base_dn is not None:
            cmd.add_element("base_dn", str(base_dn))
        if bind_password is not None:
            cmd.add_element("bind_password", str(bind_password))
        if tls_mode is not None:
            cmd.add_element("tls_mode", str(tls_mode))
        if port is not None:
            cmd.add_element("port", str(port))
        if ca_certificate is not None:
            cmd.add_element("ca_certificate", str(ca_certificate))
        return cmd

    @classmethod
    def verify_active_directory_credential(
        cls,
        *,
        credential_id: EntityID | None = None,
        host: str | None = None,
        bind_dn: str | None = None,
        bind_password: str | None = None,
        base_dn: str | None = None,
        tls_mode: str | None = None,
        port: int | None = None,
        ca_certificate: str | None = None,
    ) -> Request:
        """Verify a saved AD credential or supplied AD connection settings."""
        function = cls.verify_active_directory_credential.__name__

        has_inline_fields = (
            host is not None
            or bind_dn is not None
            or bind_password is not None
            or base_dn is not None
            or tls_mode is not None
            or port is not None
            or ca_certificate is not None
        )

        if credential_id is not None:
            if not credential_id:
                raise RequiredArgument(
                    function=function, argument="credential_id"
                )
            if has_inline_fields:
                raise InvalidArgument(
                    function=function, argument="credential_id"
                )

            cmd = XmlCommand("verify_active_directory_credential")
            cmd.set_attribute("credential_id", str(credential_id))
            return cmd

        if not host:
            raise RequiredArgument(function=function, argument="host")
        if not bind_dn:
            raise RequiredArgument(function=function, argument="bind_dn")
        if not bind_password:
            raise RequiredArgument(function=function, argument="bind_password")
        if not base_dn:
            raise RequiredArgument(function=function, argument="base_dn")
        if not tls_mode:
            raise RequiredArgument(function=function, argument="tls_mode")

        if tls_mode not in ("ldaps", "starttls"):
            raise InvalidArgument(function=function, argument="tls_mode")

        if port is not None and (
            not isinstance(port, int) or not 1 <= port <= 65535
        ):
            raise InvalidArgument(function=function, argument="port")

        cmd = XmlCommand("verify_active_directory_credential")
        cmd.add_element("host", host)
        if port is not None:
            cmd.add_element("port", str(port))
        cmd.add_element("bind_dn", bind_dn)
        cmd.add_element("bind_password", bind_password)
        cmd.add_element("base_dn", base_dn)
        cmd.add_element("tls_mode", tls_mode)
        if ca_certificate is not None:
            cmd.add_element("ca_certificate", ca_certificate)
        return cmd

    @classmethod
    def create_credential_store_credential(
        cls,
        name: str,
        credential_type: CredentialStoreCredentialType | str,
        *,
        comment: str | None = None,
        credential_store_id: EntityID | None = None,
        vault_id: str | None = None,
        host_identifier: str | None = None,
    ) -> Request:
        """Create a new credential that is fetched from a credential store

        Create a new credential e.g. to be used in the method of an alert.

        Currently the following credential types are supported:

            - Username + Password
            - Username + SSH-Key
            - Client Certificates
            - SNMPv1 or SNMPv2c protocol
            - S/MIME Certificate
            - OpenPGP Key
            - Password only

        Arguments:
            name: Name of the new credential
            credential_type: The credential type.
            comment: Comment for the credential
            credential_store_id: Optional id of the credential store to use
                (gvmd will pick default one if none is provided)
            vault_id: Vault-ID used to access the secret in credential store
            host_identifier: Host-Identifier used to access the secret in credential store

        Examples:
            Creating a Password-Only credential stored in a Credential Store

            .. code-block:: python

                request = Credentials.create_credential(
                    name="Credential-Store Password-Only Credential",
                    credential_type=CredentialType.CREDENTIAL_STOREPASSWORD_ONLY,
                    vault_id="a5f84dd4-da18-447c-a9fb-b77b5df49076",
                    host_identifier="/My/Secret",
                )
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_credential.__name__, argument="name"
            )

        if not credential_type:
            raise RequiredArgument(
                function=cls.create_credential.__name__,
                argument="credential_type",
            )

        if not isinstance(credential_type, CredentialStoreCredentialType):
            credential_type = CredentialStoreCredentialType(credential_type)

        cmd = XmlCommand("create_credential")
        cmd.add_element("name", name)

        cmd.add_element("type", credential_type.value)

        if comment:
            cmd.add_element("comment", comment)

        if (
            credential_type != CredentialStoreCredentialType.CLIENT_CERTIFICATE
            and credential_type != CredentialStoreCredentialType.SNMP
            and credential_type
            != CredentialStoreCredentialType.USERNAME_PASSWORD
            and credential_type
            != CredentialStoreCredentialType.USERNAME_SSH_KEY
            and credential_type
            != CredentialStoreCredentialType.SMIME_CERTIFICATE
            and credential_type
            != CredentialStoreCredentialType.PGP_ENCRYPTION_KEY
            and credential_type != CredentialStoreCredentialType.PASSWORD_ONLY
        ):
            raise InvalidArgument(
                function=cls.create_credential.__name__,
                argument="credential_type",
            )

        if not vault_id:
            raise RequiredArgument(
                function=cls.create_credential.__name__,
                argument="vault_id",
            )
        if not host_identifier:
            raise RequiredArgument(
                function=cls.create_credential.__name__,
                argument="host_identifier",
            )

        if credential_store_id:
            cmd.add_element("credential_store_id", str(credential_store_id))

        cmd.add_element("vault_id", vault_id)
        cmd.add_element("host_identifier", host_identifier)

        return cmd

    @classmethod
    def modify_credential_store_credential(
        cls,
        credential_id: EntityID,
        *,
        name: str | None = None,
        comment: str | None = None,
        credential_store_id: EntityID | None = None,
        vault_id: str | None = None,
        host_identifier: str | None = None,
    ) -> Request:
        """Modifies an existing credential.

        Arguments:
            credential_id: UUID of the credential
            name: Name of the credential
            comment: Comment for the credential
            credential_store_id: Optional id of the credential store to use
                (gvmd will pick default one if none is provided)
            vault_id: Vault-ID used to access the secret in credential store
            host_identifier: Host-Identifier used to access the secret in credential store
        """
        if not credential_id:
            raise RequiredArgument(
                function=cls.modify_credential.__name__,
                argument="credential_id",
            )

        cmd = XmlCommand("modify_credential")
        cmd.set_attribute("credential_id", str(credential_id))

        if name:
            cmd.add_element("name", name)
        if comment:
            cmd.add_element("comment", comment)

        if credential_store_id:
            cmd.add_element("credential_store_id", str(credential_store_id))
        if vault_id:
            cmd.add_element("vault_id", vault_id)
        if host_identifier:
            cmd.add_element("host_identifier", host_identifier)

        return cmd
