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


class CredentialFormat(Enum):
    """Enum for credential format"""

    KEY = "key"
    RPM = "rpm"
    DEB = "deb"
    EXE = "exe"
    PEM = "pem"

    @classmethod
    def from_string(
        cls,
        credential_format: Optional[str],
    ) -> Optional["CredentialFormat"]:
        if not credential_format:
            return None

        try:
            return cls[credential_format.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="credential_format",
                function=cls.from_string.__name__,
            ) from None


class CredentialType(Enum):
    """Enum for credential types"""

    CLIENT_CERTIFICATE = "cc"
    SNMP = "snmp"
    USERNAME_PASSWORD = "up"
    USERNAME_SSH_KEY = "usk"
    SMIME_CERTIFICATE = "smime"
    PGP_ENCRYPTION_KEY = "pgp"
    PASSWORD_ONLY = "pw"

    @classmethod
    def from_string(
        cls,
        credential_type: Optional[str],
    ) -> Optional["CredentialType"]:
        """Convert a credential type string into a CredentialType instance"""
        if not credential_type:
            return None

        try:
            return cls[credential_type.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="credential_type",
                function=cls.from_string.__name__,
            ) from None


class SnmpAuthAlgorithm(Enum):
    """Enum for SNMP auth algorithm"""

    SHA1 = "sha1"
    MD5 = "md5"

    @classmethod
    def from_string(
        cls,
        algorithm: Optional[str],
    ) -> Optional["SnmpAuthAlgorithm"]:
        """Convert a SNMP auth algorithm string into a
        SnmpAuthAlgorithm instance"""
        if not algorithm:
            return None

        try:
            return cls[algorithm.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="algorithm",
                function=cls.from_string.__name__,
            ) from None


class SnmpPrivacyAlgorithm(Enum):
    """Enum for SNMP privacy algorithm"""

    AES = "aes"
    DES = "des"

    @classmethod
    def from_string(
        cls,
        algorithm: Optional[str],
    ) -> Optional["SnmpPrivacyAlgorithm"]:
        """Convert a SNMP privacy algorithm string into a SnmpPrivacyAlgorithm
        instance
        """
        if not algorithm:
            return None

        try:
            return cls[algorithm.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="algorithm",
                function=cls.from_string.__name__,
            ) from None


class CredentialsMixin:
    def clone_credential(self, credential_id: str) -> Any:
        """Clone an existing credential

        Arguments:
            credential_id: UUID of an existing credential to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                function=self.clone_credential.__name__,
                argument="credential_id",
            )

        cmd = XmlCommand("create_credential")
        cmd.add_element("copy", credential_id)
        return self._send_xml_command(cmd)

    def create_credential(
        self,
        name: str,
        credential_type: CredentialType,
        *,
        comment: Optional[str] = None,
        allow_insecure: Optional[bool] = None,
        certificate: Optional[str] = None,
        key_phrase: Optional[str] = None,
        private_key: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        auth_algorithm: Optional[SnmpAuthAlgorithm] = None,
        community: Optional[str] = None,
        privacy_algorithm: Optional[SnmpPrivacyAlgorithm] = None,
        privacy_password: Optional[str] = None,
        public_key: Optional[str] = None,
    ) -> Any:
        """Create a new credential

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
            certificate: Certificate for the credential.
                Required for client-certificate and smime credential types.
            key_phrase: Key passphrase for the private key.
                Used for the username+ssh-key credential type.
            private_key: Private key to use for login. Required
                for usk credential type. Also used for the cc credential type.
                The supported key types (dsa, rsa, ecdsa, ...) and formats (PEM,
                PKC#12, OpenSSL, ...) depend on your installed GnuTLS version.
            login: Username for the credential. Required for username+password,
                username+ssh-key and snmp credential type.
            password: Password for the credential. Used for username+password
                and snmp credential types.
            community: The SNMP community
            auth_algorithm: The SNMP authentication algorithm. Required for snmp
                credential type.
            privacy_algorithm: The SNMP privacy algorithm
            privacy_password: The SNMP privacy password
            public_key: PGP public key in *armor* plain text format. Required
                for pgp credential type.

        Examples:
            Creating a Username + Password credential

            .. code-block:: python

                gmp.create_credential(
                    name='UP Credential',
                    credential_type=CredentialType.USERNAME_PASSWORD,
                    login='foo',
                    password='bar',
                )

            Creating a Username + SSH Key credential

            .. code-block:: python

                with open('path/to/private-ssh-key') as f:
                    key = f.read()

                gmp.create_credential(
                    name='USK Credential',
                    credential_type=CredentialType.USERNAME_SSH_KEY,
                    login='foo',
                    key_phrase='foobar',
                    private_key=key,
                )

            Creating a PGP credential

            .. note::

                A compatible public pgp key file can be exported with GnuPG via
                ::

                    $ gpg --armor --export alice@cyb.org > alice.asc

            .. code-block:: python

                with open('path/to/pgp.key.asc') as f:
                    key = f.read()

                gmp.create_credential(
                    name='PGP Credential',
                    credential_type=CredentialType.PGP_ENCRYPTION_KEY,
                    public_key=key,
                )

            Creating a S/MIME credential

            .. code-block:: python

                with open('path/to/smime-cert') as f:
                    cert = f.read()

                gmp.create_credential(
                    name='SMIME Credential',
                    credential_type=CredentialType.SMIME_CERTIFICATE,
                    certificate=cert,
                )

            Creating a Password-Only credential

            .. code-block:: python

                gmp.create_credential(
                    name='Password-Only Credential',
                    credential_type=CredentialType.PASSWORD_ONLY,
                    password='foo',
                )
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_credential.__name__, argument="name"
            )

        if not isinstance(credential_type, CredentialType):
            raise InvalidArgumentType(
                function=self.create_credential.__name__,
                argument="credential_type",
                arg_type=CredentialType.__name__,
            )

        cmd = XmlCommand("create_credential")
        cmd.add_element("name", name)

        cmd.add_element("type", credential_type.value)

        if comment:
            cmd.add_element("comment", comment)

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", to_bool(allow_insecure))

        if (
            credential_type == CredentialType.CLIENT_CERTIFICATE
            or credential_type == CredentialType.SMIME_CERTIFICATE
        ):
            if not certificate:
                raise RequiredArgument(
                    function=self.create_credential.__name__,
                    argument="certificate",
                )

            cmd.add_element("certificate", certificate)

        if (
            credential_type == CredentialType.USERNAME_PASSWORD
            or credential_type == CredentialType.USERNAME_SSH_KEY
            or credential_type == CredentialType.SNMP
        ):
            if not login:
                raise RequiredArgument(
                    function=self.create_credential.__name__, argument="login"
                )

            cmd.add_element("login", login)

        if credential_type == CredentialType.PASSWORD_ONLY and not password:
            raise RequiredArgument(
                function=self.create_credential.__name__, argument="password"
            )

        if (
            credential_type == CredentialType.USERNAME_PASSWORD
            or credential_type == CredentialType.SNMP
            or credential_type == CredentialType.PASSWORD_ONLY
        ) and password:
            cmd.add_element("password", password)

        if credential_type == CredentialType.USERNAME_SSH_KEY:
            if not private_key:
                raise RequiredArgument(
                    function=self.create_credential.__name__,
                    argument="private_key",
                )

            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("private", private_key)

            if key_phrase:
                _xmlkey.add_element("phrase", key_phrase)

        if credential_type == CredentialType.CLIENT_CERTIFICATE and private_key:
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("private", private_key)

        if credential_type == CredentialType.SNMP:
            if not isinstance(auth_algorithm, SnmpAuthAlgorithm):
                raise InvalidArgumentType(
                    function=self.create_credential.__name__,
                    argument="auth_algorithm",
                    arg_type=SnmpAuthAlgorithm.__name__,
                )

            cmd.add_element("auth_algorithm", auth_algorithm.value)

            if community:
                cmd.add_element("community", community)

            if privacy_algorithm is not None or privacy_password:
                _xmlprivacy = cmd.add_element("privacy")

                if privacy_algorithm is not None:
                    if not isinstance(privacy_algorithm, SnmpPrivacyAlgorithm):
                        raise InvalidArgumentType(
                            function=self.create_credential.__name__,
                            argument="privacy_algorithm",
                            arg_type=SnmpPrivacyAlgorithm.__name__,
                        )

                    _xmlprivacy.add_element(
                        "algorithm", privacy_algorithm.value
                    )

                if privacy_password:
                    _xmlprivacy.add_element("password", privacy_password)

        if credential_type == CredentialType.PGP_ENCRYPTION_KEY:
            if not public_key:
                raise RequiredArgument(
                    function=self.create_credential.__name__,
                    argument="public_key",
                )

            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("public", public_key)

        return self._send_xml_command(cmd)

    def delete_credential(
        self, credential_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing credential

        Arguments:
            credential_id: UUID of the credential to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not credential_id:
            raise RequiredArgument(
                function=self.delete_credential.__name__,
                argument="credential_id",
            )

        cmd = XmlCommand("delete_credential")
        cmd.set_attribute("credential_id", credential_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_credentials(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        scanners: Optional[bool] = None,
        trash: Optional[bool] = None,
        targets: Optional[bool] = None,
    ) -> Any:
        """Request a list of credentials

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            scanners: Whether to include a list of scanners using the
                credentials
            trash: Whether to get the trashcan credentials instead
            targets: Whether to include a list of targets using the credentials

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_credentials")

        add_filter(cmd, filter_string, filter_id)

        if scanners is not None:
            cmd.set_attribute("scanners", to_bool(scanners))

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if targets is not None:
            cmd.set_attribute("targets", to_bool(targets))

        return self._send_xml_command(cmd)

    def get_credential(
        self,
        credential_id: str,
        *,
        scanners: Optional[bool] = None,
        targets: Optional[bool] = None,
        credential_format: Optional[CredentialFormat] = None,
    ) -> Any:
        """Request a single credential

        Arguments:
            credential_id: UUID of an existing credential
            scanners: Whether to include a list of scanners using the
                credentials
            targets: Whether to include a list of targets using the credentials
            credential_format: One of "key", "rpm", "deb", "exe" or "pem"

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                function=self.get_credential.__name__, argument="credential_id"
            )

        cmd = XmlCommand("get_credentials")
        cmd.set_attribute("credential_id", credential_id)

        if credential_format:
            if not isinstance(credential_format, CredentialFormat):
                raise InvalidArgumentType(
                    function=self.get_credential.__name__,
                    argument="credential_format",
                    arg_type=CredentialFormat.__name__,
                )

            cmd.set_attribute("format", credential_format.value)

        if scanners is not None:
            cmd.set_attribute("scanners", to_bool(scanners))

        if targets is not None:
            cmd.set_attribute("targets", to_bool(targets))

        return self._send_xml_command(cmd)

    def modify_credential(
        self,
        credential_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        allow_insecure: Optional[bool] = None,
        certificate: Optional[str] = None,
        key_phrase: Optional[str] = None,
        private_key: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        auth_algorithm: Optional[SnmpAuthAlgorithm] = None,
        community: Optional[str] = None,
        privacy_algorithm: Optional[SnmpPrivacyAlgorithm] = None,
        privacy_password: Optional[str] = None,
        public_key: Optional[str] = None,
    ) -> Any:
        """Modifies an existing credential.

        Arguments:
            credential_id: UUID of the credential
            name: Name of the credential
            comment: Comment for the credential
            allow_insecure: Whether to allow insecure use of the credential
            certificate: Certificate for the credential
            key_phrase: Key passphrase for the private key
            private_key: Private key to use for login
            login: Username for the credential
            password: Password for the credential
            auth_algorithm: The authentication algorithm for SNMP
            community: The SNMP community
            privacy_algorithm: The privacy algorithm for SNMP
            privacy_password: The SNMP privacy password
            public_key: PGP public key in *armor* plain text format

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                function=self.modify_credential.__name__,
                argument="credential_id",
            )

        cmd = XmlCommand("modify_credential")
        cmd.set_attribute("credential_id", credential_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", to_bool(allow_insecure))

        if certificate:
            cmd.add_element("certificate", certificate)

        if key_phrase and private_key:
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("phrase", key_phrase)
            _xmlkey.add_element("private", private_key)
        elif (not key_phrase and private_key) or (
            key_phrase and not private_key
        ):
            raise RequiredArgument(
                function=self.modify_credential.__name__,
                argument="key_phrase and private_key",
            )

        if login:
            cmd.add_element("login", login)

        if password:
            cmd.add_element("password", password)

        if auth_algorithm:
            if not isinstance(auth_algorithm, SnmpAuthAlgorithm):
                raise InvalidArgumentType(
                    function=self.modify_credential.__name__,
                    argument="auth_algorithm",
                    arg_type=SnmpAuthAlgorithm.__name__,
                )
            cmd.add_element("auth_algorithm", auth_algorithm.value)

        if community:
            cmd.add_element("community", community)

        if privacy_algorithm is not None or privacy_password is not None:
            _xmlprivacy = cmd.add_element("privacy")

            if privacy_algorithm is not None:
                if not isinstance(privacy_algorithm, SnmpPrivacyAlgorithm):
                    raise InvalidArgumentType(
                        function=self.modify_credential.__name__,
                        argument="privacy_algorithm",
                        arg_type=SnmpPrivacyAlgorithm.__name__,
                    )

                _xmlprivacy.add_element("algorithm", privacy_algorithm.value)

            if privacy_password is not None:
                _xmlprivacy.add_element("password", privacy_password)

        if public_key:
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("public", public_key)

        return self._send_xml_command(cmd)
