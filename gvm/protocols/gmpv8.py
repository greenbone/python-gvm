# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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

# pylint: disable=arguments-differ

"""
Module for communication with gvmd in `Greenbone Management Protocol version 8`_

**GMP Version 8 has not been released yet**

.. _Greenbone Management Protocol version 8:
    https://docs.greenbone.net/API/GMP/gmp-8.0.html
"""

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.utils import get_version_string
from gvm.xml import XmlCommand

from .gmpv7 import Gmp as Gmpv7, _to_bool

CREDENTIAL_TYPES = ("cc", "snmp", "up", "usk", "smime", "pgp")

PROTOCOL_VERSION = (8,)


class Gmp(Gmpv7):
    @staticmethod
    def get_protocol_version():
        """Allow to determine the Greenbone Management Protocol version.

            Returns:
                str: Implemented version of the Greenbone Management Protocol
        """
        return get_version_string(PROTOCOL_VERSION)

    def create_credential(
        self,
        name,
        credential_type,
        *,
        comment=None,
        allow_insecure=None,
        certificate=None,
        key_phrase=None,
        private_key=None,
        login=None,
        password=None,
        auth_algorithm=None,
        community=None,
        privacy_algorithm=None,
        privacy_password=None,
        public_key=None
    ):
        """Create a new credential

        Create a new credential e.g. to be used in the method of an alert.

        Currently the following credential types are supported:

            - 'up'    - Username + Password
            - 'usk'   - Username + private SSH-Key
            - 'cc'    - Client Certificates
            - 'snmp'  - SNMPv1 or SNMPv2c protocol
            - 'smime' - S/MIME Certificate
            - 'pgp'   - OpenPGP Key

        Arguments:
            name (str): Name of the new credential
            credential_type (str): The credential type. One of 'cc', 'snmp',
                'up', 'usk', 'smime', 'pgp'
            comment (str, optional): Comment for the credential
            allow_insecure (boolean, optional): Whether to allow insecure use of
                the credential
            certificate (str, optional): Certificate for the credential.
                Required for cc and smime credential types.
            key_phrase (str, optional): Key passphrase for the private key.
                Used for the usk credential type.
            private_key (str, optional): Private key to use for login. Required
                for usk credential type. Also used for the cc credential type.
                The supported key types (dsa, rsa, ecdsa, ...) and formats (PEM,
                PKC#12, OpenSSL, ...) depend on your installed GnuTLS version.
            login (str, optional): Username for the credential. Required for
                up, usk and snmp credential type.
            password (str, optional): Password for the credential. Used for
                up and snmp credential types.
            community (str, optional): The SNMP community
            auth_algorithm (str, optional): The SNMP authentication algorithm.
                Either 'md5' or 'sha1'. Required for snmp credential type.
            privacy_algorithm (str, optional): The SNMP privacy algorithm,
                either aes or des.
            privacy_password (str, optional): The SNMP privacy password
            public_key: (str, optional): PGP public key in *armor* plain text
                format. Required for pgp credential type.

        Examples:
            Creating a Username + Password credential

            .. code-block:: python

                gmp.create_credential(
                    name='UP Credential',
                    credential_type='up',
                    login='foo',
                    password='bar',
                );

            Creating a Username + SSH Key credential

            .. code-block:: python

                with open('path/to/private-ssh-key') as f:
                    key = f.read()

                gmp.create_credential(
                    name='USK Credential',
                    credential_type='usk',
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
                    credential_type='pgp',
                    public_key=key,
                )

            Creating a S/MIME credential

            .. code-block:: python

                with open('path/to/smime-cert') as f:
                    cert = f.read()

                gmp.create_credential(
                    name='SMIME Credential',
                    credential_type='smime',
                    certificate=cert,
                )

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_credential requires name argument")

        if credential_type not in CREDENTIAL_TYPES:
            raise InvalidArgument(
                "create_credential requires type to be either cc, snmp, up,"
                "smime, pgp or usk"
            )

        cmd = XmlCommand("create_credential")
        cmd.add_element("name", name)

        cmd.add_element("type", credential_type)

        if comment:
            cmd.add_element("comment", comment)

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", _to_bool(allow_insecure))

        if credential_type == "cc" or credential_type == "smime":
            if not certificate:
                raise RequiredArgument(
                    "create_credential requires certificate argument for "
                    "credential_type {0}".format(credential_type)
                )

            cmd.add_element("certificate", certificate)

        if (
            credential_type == "up"
            or credential_type == "usk"
            or credential_type == "snmp"
        ):
            if not login:
                raise RequiredArgument(
                    "create_credential requires login argument for "
                    "credential_type {0}".format(credential_type)
                )

            cmd.add_element("login", login)

        if (credential_type == "up" or credential_type == "snmp") and password:
            cmd.add_element("password", password)

        if credential_type == "usk":
            if not private_key:
                raise RequiredArgument(
                    "create_credential requires certificate argument for "
                    "credential_type usk"
                )

            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("private", private_key)

            if key_phrase:
                _xmlkey.add_element("phrase", key_phrase)

        if credential_type == "cc" and private_key:
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("private", private_key)

        if credential_type == "snmp":
            if auth_algorithm not in ("md5", "sha1"):
                raise InvalidArgument(
                    "create_credential requires auth_algorithm to be either "
                    "md5 or sha1"
                )

            cmd.add_element("auth_algorithm", auth_algorithm)

            if community:
                cmd.add_element("community", community)

            if privacy_algorithm is not None or privacy_password:
                _xmlprivacy = cmd.add_element("privacy")

                if privacy_algorithm is not None:
                    if privacy_algorithm not in ("aes", "des"):
                        raise InvalidArgument(
                            "create_credential requires algorithm to be either "
                            "aes or des"
                        )

                    _xmlprivacy.add_element("algorithm", privacy_algorithm)

                if privacy_password:
                    _xmlprivacy.add_element("password", privacy_password)

        if credential_type == "pgp":
            if not public_key:
                raise RequiredArgument(
                    "Creating a pgp credential requires a public_key argument"
                )

            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("public", public_key)

        return self._send_xml_command(cmd)

    def modify_credential(
        self,
        credential_id,
        name=None,
        comment=None,
        allow_insecure=None,
        certificate=None,
        key_phrase=None,
        private_key=None,
        login=None,
        password=None,
        auth_algorithm=None,
        community=None,
        privacy_algorithm=None,
        privacy_password=None,
        credential_type=None,
        public_key=None,
    ):
        """Modifies an existing credential.

        Arguments:
            credential_id (str): UUID of the credential
            name (str, optional): Name of the credential
            comment (str, optional): Comment for the credential
            allow_insecure (boolean, optional): Whether to allow insecure use of
                 the credential
            certificate (str, optional): Certificate for the credential
            key_phrase (str, optional): Key passphrase for the private key
            private_key (str, optional): Private key to use for login
            login (str, optional): Username for the credential
            password (str, optional): Password for the credential
            auth_algorithm (str, optional): The auth_algorithm,
                either md5 or sha1.
            community (str, optional): The SNMP community
            privacy_algorithm (str, optional): The SNMP privacy algorithm,
                either aes or des.
            privacy_password (str, optional): The SNMP privacy password
            credential_type (str, optional): The credential type. One of 'cc',
                'snmp', 'up', 'usk', 'smime', 'pgp'
            public_key: (str, optional): PGP public key in *armor* plain text
                format

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                "modify_credential requires " "a credential_id attribute"
            )

        cmd = XmlCommand("modify_credential")
        cmd.set_attribute("credential_id", credential_id)

        if credential_type:
            if credential_type not in CREDENTIAL_TYPES:
                raise InvalidArgument(
                    "modify_credential requires type to be either cc, snmp, up "
                    "smime, pgp or usk"
                )
            cmd.add_element("type", credential_type)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", _to_bool(allow_insecure))

        if certificate:
            cmd.add_element("certificate", certificate)

        if key_phrase or private_key:
            if not key_phrase or not private_key:
                raise RequiredArgument(
                    "modify_credential requires "
                    "a key_phrase and private_key arguments"
                )
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("phrase", key_phrase)
            _xmlkey.add_element("private", private_key)

        if login:
            cmd.add_element("login", login)

        if password:
            cmd.add_element("password", password)

        if auth_algorithm:
            if auth_algorithm not in ("md5", "sha1"):
                raise InvalidArgument(
                    "modify_credential requires "
                    "auth_algorithm to be either "
                    "md5 or sha1"
                )
            cmd.add_element("auth_algorithm", auth_algorithm)

        if community:
            cmd.add_element("community", community)

        if privacy_algorithm is not None or privacy_password is not None:
            _xmlprivacy = cmd.add_element("privacy")

            if privacy_algorithm is not None:
                if privacy_algorithm not in ("aes", "des"):
                    raise InvalidArgument(
                        "modify_credential requires privacy_algorithm to be "
                        "either aes or des"
                    )

                _xmlprivacy.add_element("algorithm", privacy_algorithm)

            if privacy_password is not None:
                _xmlprivacy.add_element("password", privacy_password)

        if public_key:
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("public", public_key)

        return self._send_xml_command(cmd)
