# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm._enum import Enum
from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
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


class Credentials(CredentialsV224):
    @classmethod
    def create_credential_store_credential(
        cls,
        name: str,
        credential_type: Union[CredentialStoreCredentialType, str],
        *,
        comment: Optional[str] = None,
        allow_insecure: Optional[bool] = None,
        credential_store_id: Optional[EntityID] = None,
        vault_id: Optional[str] = None,
        host_identifier: Optional[str] = None,
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
            allow_insecure: Whether to allow insecure use of the credential
            credential_store_id: Optional id of the credential store to use
                (gvmd will pick default one if none is provided)
            vault_id: Vault-ID used to access the secret in credential store
            host_identifier: Host-Identifier used to access the secret in credential store

        Examples:
            Creating a Password-Only credential stored in a Credential Store

            .. code-block:: python

                request = Credentials.create_credential(
                    name='Credential-Store Password-Only Credential',
                    credential_type=CredentialType.CREDENTIAL_STOREPASSWORD_ONLY,
                    vault_id='a5f84dd4-da18-447c-a9fb-b77b5df49076',
                    host_identifier='/My/Secret',
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

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", to_bool(allow_insecure))

        if (
            credential_type == CredentialStoreCredentialType.CLIENT_CERTIFICATE
            or credential_type == CredentialStoreCredentialType.SNMP
            or credential_type
            == CredentialStoreCredentialType.USERNAME_PASSWORD
            or credential_type == CredentialStoreCredentialType.USERNAME_SSH_KEY
            or credential_type
            == CredentialStoreCredentialType.SMIME_CERTIFICATE
            or credential_type
            == CredentialStoreCredentialType.PGP_ENCRYPTION_KEY
            or credential_type == CredentialStoreCredentialType.PASSWORD_ONLY
        ):
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
        name: Optional[str] = None,
        comment: Optional[str] = None,
        allow_insecure: Optional[bool] = None,
        credential_store_id: Optional[EntityID] = None,
        vault_id: Optional[str] = None,
        host_identifier: Optional[str] = None,
    ) -> Request:
        """Modifies an existing credential.

        Arguments:
            credential_id: UUID of the credential
            name: Name of the credential
            comment: Comment for the credential
            allow_insecure: Whether to allow insecure use of the credential
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

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", to_bool(allow_insecure))

        if credential_store_id:
            cmd.add_element("credential_store_id", str(credential_store_id))
        if vault_id:
            cmd.add_element("vault_id", vault_id)
        if host_identifier:
            cmd.add_element("host_identifier", host_identifier)

        return cmd
