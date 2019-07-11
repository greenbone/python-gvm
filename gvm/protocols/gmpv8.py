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

# pylint: disable=arguments-differ, redefined-builtin, too-many-lines

"""
Module for communication with gvmd in `Greenbone Management Protocol version 8`_

.. _Greenbone Management Protocol version 8:
    https://docs.greenbone.net/API/GMP/gmp-8.0.html
"""
from enum import Enum
from typing import Any, List, Optional

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.utils import get_version_string
from gvm.xml import XmlCommand

from gvm.protocols.gmpv7 import (
    AlertCondition,
    AlertEvent,
    AlertMethod,
    AliveTest,
    Gmp as Gmpv7,
    HostsOrdering,
    _to_bool,
    _add_filter,
    PermissionSubjectType,
    PortRangeType,
    ScannerType,
    SeverityLevel,
    SnmpAuthAlgorithm,
    SnmpPrivacyAlgorithm,
    get_hosts_ordering_from_string,
    get_permission_subject_type_from_string,
    get_severity_level_from_string,
    get_snmp_auth_algorithm_from_string,
    get_snmp_privacy_algorithm_from_string,
)

__all__ = [
    "AlertCondition",
    "AlertEvent",
    "AlertMethod",
    "AliveTest",
    "CredentialType",
    "FilterType",
    "Gmp",
    "HostsOrdering",
    "PermissionSubjectType",
    "PortRangeType",
    "ScannerType",
    "SeverityLevel",
    "SnmpAuthAlgorithm",
    "SnmpPrivacyAlgorithm",
    "get_credential_type_from_string",
    "get_filter_type_from_string",
    "get_hosts_ordering_from_string",
    "get_permission_subject_type_from_string",
    "get_severity_level_from_string",
    "get_snmp_auth_algorithm_from_string",
    "get_snmp_privacy_algorithm_from_string",
    "get_ticket_status_from_string",
]

PROTOCOL_VERSION = (8,)


class FilterType(Enum):
    """ Enum for filter types """

    AGENT = "agent"
    ALERT = "alert"
    ASSET = "asset"
    SCAN_CONFIG = "config"
    CREDENTIAL = "credential"
    FILTER = "filter"
    GROUP = "group"
    HOST = "host"
    NOTE = "note"
    OPERATING_SYSTEM = "os"
    OVERRIDE = "override"
    PERMISSION = "permission"
    PORT_LIST = "port_list"
    REPORT = "report"
    REPORT_FORMAT = "report_format"
    RESULT = "result"
    ROLE = "role"
    SCHEDULE = "schedule"
    ALL_SECINFO = "secinfo"
    TAG = "tag"
    TARGET = "target"
    TASK = "task"
    TICKET = "ticket"
    USER = "user"
    VULNERABILITY = "vuln"


def get_filter_type_from_string(
    filter_type: Optional[str]
) -> Optional[FilterType]:
    """ Convert a filter type string to an actual FilterType instance

    Arguments:
        filter_type (str): Filter type string to convert to a FilterType
    """
    if not filter_type:
        return None

    if filter_type == 'vuln':
        return FilterType.VULNERABILITY

    if filter_type == 'os':
        return FilterType.OPERATING_SYSTEM

    if filter_type == 'config':
        return FilterType.SCAN_CONFIG

    if filter_type == 'secinfo':
        return FilterType.ALL_SECINFO

    try:
        return FilterType[filter_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='filter_type',
            function=get_filter_type_from_string.__name__,
        )


class CredentialType(Enum):
    """ Enum for credential types """

    CLIENT_CERTIFICATE = 'cc'
    SNMP = 'snmp'
    USERNAME_PASSWORD = 'up'
    USERNAME_SSH_KEY = 'usk'
    SMIME_CERTIFICATE = 'smime'
    PGP_ENCRYPTION_KEY = 'pgp'
    PASSWORD_ONLY = 'pw'


def get_credential_type_from_string(
    credential_type: Optional[str]
) -> Optional[CredentialType]:
    """ Convert a credential type string into a CredentialType instance
    """
    if not credential_type:
        return None

    try:
        return CredentialType[credential_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='credential_type',
            function=get_credential_type_from_string.__name__,
        )


class TicketStatus(Enum):
    """ Enum for ticket status """

    OPEN = 'Open'
    FIXED = 'Fixed'
    CLOSED = 'Closed'


def get_ticket_status_from_string(
    ticket_status: Optional[str]
) -> Optional[TicketStatus]:
    """ Convert a ticket status string into a TicketStatus instance
    """
    if not ticket_status:
        return None

    try:
        return TicketStatus[ticket_status.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='ticket_status',
            function=get_ticket_status_from_string.__name__,
        )


class Gmp(Gmpv7):

    _filter_type = FilterType

    @staticmethod
    def get_protocol_version() -> str:
        """Determine the Greenbone Management Protocol version.

        Returns:
            str: Implemented version of the Greenbone Management Protocol
        """
        return get_version_string(PROTOCOL_VERSION)

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
        public_key: Optional[str] = None
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
                );

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
                function="create_credential", argument="name"
            )

        if not isinstance(credential_type, CredentialType):
            raise InvalidArgument(
                "create_credential requires type to be a CredentialType "
                "instance",
                function="create_credential",
                argument="credential_type",
            )

        cmd = XmlCommand("create_credential")
        cmd.add_element("name", name)

        cmd.add_element("type", credential_type.value)

        if comment:
            cmd.add_element("comment", comment)

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", _to_bool(allow_insecure))

        if (
            credential_type == CredentialType.CLIENT_CERTIFICATE
            or credential_type == CredentialType.SMIME_CERTIFICATE
        ):
            if not certificate:
                raise RequiredArgument(
                    "create_credential requires certificate argument for "
                    "credential_type {0}".format(credential_type.name),
                    function="create_credential",
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
                    "create_credential requires login argument for "
                    "credential_type {0}".format(credential_type.name),
                    function="create_credential",
                    argument="login",
                )

            cmd.add_element("login", login)

        if credential_type == CredentialType.PASSWORD_ONLY and not password:
            raise RequiredArgument(
                "create_credential requires password argument for "
                "credential_type {0}".format(credential_type.name),
                function="create_credential",
                argument="password",
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
                    "create_credential requires private_key argument for "
                    "credential_type {0}".format(credential_type.name),
                    function="create_credential",
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
                raise InvalidArgument(
                    "create_credential requires auth_algorithm to be a "
                    "SnmpAuthAlgorithm instance",
                    function="create_credential",
                    argument="auth_algorithm",
                )

            cmd.add_element("auth_algorithm", auth_algorithm.value)

            if community:
                cmd.add_element("community", community)

            if privacy_algorithm is not None or privacy_password:
                _xmlprivacy = cmd.add_element("privacy")

                if privacy_algorithm is not None:
                    if not isinstance(privacy_algorithm, SnmpPrivacyAlgorithm):
                        raise InvalidArgument(
                            "create_credential requires algorithm to be a "
                            "SnmpPrivacyAlgorithm instance",
                            function="create_credential",
                            argument="privacy_algorithm",
                        )

                    _xmlprivacy.add_element(
                        "algorithm", privacy_algorithm.value
                    )

                if privacy_password:
                    _xmlprivacy.add_element("password", privacy_password)

        if credential_type == CredentialType.PGP_ENCRYPTION_KEY:
            if not public_key:
                raise RequiredArgument(
                    "Creating a pgp credential requires a public_key argument",
                    argument="public_key",
                    function="create_credential",
                )

            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("public", public_key)

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
        credential_type: Optional[CredentialType] = None,
        public_key: Optional[str] = None
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
            credential_type: The credential type.
            public_key: PGP public key in *armor* plain text format

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                argument="credential_id", function="modify_credential"
            )

        cmd = XmlCommand("modify_credential")
        cmd.set_attribute("credential_id", credential_id)

        if credential_type:
            if not isinstance(credential_type, CredentialType):
                raise InvalidArgument(
                    "modify_credential requires type to be a CredentialType "
                    "instance",
                    argument="type",
                    function="modify_credential",
                )
            cmd.add_element("type", credential_type.value)

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
                    "a key_phrase and private_key arguments",
                    function="modify_credential",
                )
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("phrase", key_phrase)
            _xmlkey.add_element("private", private_key)

        if login:
            cmd.add_element("login", login)

        if password:
            cmd.add_element("password", password)

        if auth_algorithm:
            if not isinstance(auth_algorithm, SnmpAuthAlgorithm):
                raise InvalidArgument(
                    "modify_credential requires auth_algorithm to be a "
                    "SnmpAuthAlgorithm instance",
                    argument="auth_algorithm",
                    function="modify_credential",
                )
            cmd.add_element("auth_algorithm", auth_algorithm.value)

        if community:
            cmd.add_element("community", community)

        if privacy_algorithm is not None or privacy_password is not None:
            _xmlprivacy = cmd.add_element("privacy")

            if privacy_algorithm is not None:
                if not isinstance(privacy_algorithm, SnmpPrivacyAlgorithm):
                    raise InvalidArgument(
                        "modify_credential requires privacy_algorithm to be "
                        "a SnmpPrivacyAlgorithm instance",
                        argument="privacy_algorithm",
                        function="modify_credential",
                    )

                _xmlprivacy.add_element("algorithm", privacy_algorithm.value)

            if privacy_password is not None:
                _xmlprivacy.add_element("password", privacy_password)

        if public_key:
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("public", public_key)

        return self._send_xml_command(cmd)

    def create_tag(
        self,
        name: str,
        resource_type: str,
        *,
        resource_filter: Optional[str] = None,
        resource_ids: Optional[List[str]] = None,
        value: Optional[str] = None,
        comment: Optional[str] = None,
        active: Optional[bool] = None
    ) -> Any:
        """Create a tag.

        Arguments:
            name: Name of the tag. A full tag name consisting of namespace and
                predicate e.g. `foo:bar`.
            resource_type: Entity type the tag is to be attached to.
            resource_filter: Filter term to select resources the tag is to be
                attached to. Only one of resource_filter or resource_ids can be
                provided.
            resource_ids: IDs of the resources the tag is to be attached to.
                Only one of resource_filter or resource_ids can be provided.
            value: Value associated with the tag.
            comment: Comment for the tag.
            active: Whether the tag should be active.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(function="create_tag", argument="name")

        if resource_filter and resource_ids:
            raise InvalidArgument(
                "create_tag accepts either resource_filter or resource_ids "
                "argument",
                function="create_tag",
            )

        if not resource_type:
            raise RequiredArgument(
                function="create_tag", argument="resource_type"
            )

        cmd = XmlCommand('create_tag')
        cmd.add_element('name', name)

        _xmlresources = cmd.add_element("resources")
        if resource_filter is not None:
            _xmlresources.set_attribute("filter", resource_filter)

        for resource_id in resource_ids or []:
            _xmlresources.add_element(
                "resource", attrs={"id": str(resource_id)}
            )

        _xmlresources.add_element("type", resource_type)

        if comment:
            cmd.add_element("comment", comment)

        if value:
            cmd.add_element("value", value)

        if active is not None:
            if active:
                cmd.add_element("active", "1")
            else:
                cmd.add_element("active", "0")

        return self._send_xml_command(cmd)

    def modify_tag(
        self,
        tag_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        value=None,
        active=None,
        resource_action: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_filter: Optional[str] = None,
        resource_ids: Optional[List[str]] = None
    ) -> Any:
        """Modifies an existing tag.

        Arguments:
            tag_id: UUID of the tag.
            comment: Comment to add to the tag.
            name: Name of the tag.
            value: Value of the tag.
            active: Whether the tag is active.
            resource_action: Whether to add or remove resources instead of
                overwriting. One of '', 'add', 'set' or 'remove'.
            resource_type: Type of the resources to which to attach the tag.
                Required if resource_filter is set.
            resource_filter: Filter term to select resources the tag is to be
                attached to.
            resource_ids: IDs of the resources to which to attach the tag.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tag_id:
            raise RequiredArgument("modify_tag requires a tag_id element")

        cmd = XmlCommand("modify_tag")
        cmd.set_attribute("tag_id", str(tag_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if value:
            cmd.add_element("value", value)

        if active is not None:
            cmd.add_element("active", _to_bool(active))

        if resource_action or resource_filter or resource_ids or resource_type:
            if resource_filter and not resource_type:
                raise RequiredArgument(
                    "modify_tag requires resource_type argument when "
                    "resource_filter is set",
                    function="modify_tag",
                    argument="resource_type",
                )

            _xmlresources = cmd.add_element("resources")
            if resource_action is not None:
                _xmlresources.set_attribute("action", resource_action)

            if resource_filter is not None:
                _xmlresources.set_attribute("filter", resource_filter)

            for resource_id in resource_ids or []:
                _xmlresources.add_element(
                    "resource", attrs={"id": str(resource_id)}
                )

            if resource_type is not None:
                _xmlresources.add_element("type", resource_type)

        return self._send_xml_command(cmd)

    def clone_ticket(self, ticket_id: str) -> Any:
        """Clone an existing ticket

        Arguments:
            ticket_id: UUID of an existing ticket to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not ticket_id:
            raise RequiredArgument(
                function="clone_ticket", argument="ticket_id"
            )

        cmd = XmlCommand("create_ticket")

        _copy = cmd.add_element("copy", ticket_id)

        return self._send_xml_command(cmd)

    def create_ticket(
        self,
        *,
        result_id: str,
        assigned_to_user_id: str,
        note: str,
        comment: Optional[str] = None
    ) -> Any:
        """Create a new ticket

        Arguments:
            result_id: UUID of the result the ticket applies to
            assigned_to_user_id: UUID of a user the ticket should be assigned to
            note: A note about opening the ticket
            comment: Comment for the ticket

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not result_id:
            raise RequiredArgument(
                function="create_ticket", argument="result_id"
            )

        if not assigned_to_user_id:
            raise RequiredArgument(
                function="create_ticket", argument="assigned_to_user_id"
            )

        if not note:
            raise RequiredArgument(function="create_ticket", argument="note")

        cmd = XmlCommand("create_ticket")

        _result = cmd.add_element("result")
        _result.set_attribute("id", result_id)

        _assigned = cmd.add_element("assigned_to")
        _user = _assigned.add_element("user")
        _user.set_attribute("id", assigned_to_user_id)

        _note = cmd.add_element("open_note", note)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def delete_ticket(
        self, ticket_id: str, *, ultimate: Optional[bool] = False
    ):
        """Deletes an existing ticket

        Arguments:
            ticket_id: UUID of the ticket to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not ticket_id:
            raise RequiredArgument(
                function="delete_ticket", argument="ticket_id"
            )

        cmd = XmlCommand("delete_ticket")
        cmd.set_attribute("ticket_id", ticket_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_tickets(
        self,
        *,
        trash: Optional[bool] = None,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None
    ) -> Any:
        """Request a list of tickets

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: True to request the tickets in the trashcan

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tickets")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        return self._send_xml_command(cmd)

    def get_ticket(self, ticket_id: str) -> Any:
        """Request a single ticket

        Arguments:
            ticket_id: UUID of an existing ticket

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not ticket_id:
            raise RequiredArgument(function="get_ticket", argument="ticket_id")

        cmd = XmlCommand("get_tickets")
        cmd.set_attribute("ticket_id", ticket_id)
        return self._send_xml_command(cmd)

    def get_vulnerabilities(
        self, *, filter: Optional[str] = None, filter_id: Optional[str] = None
    ) -> Any:
        """Request a list of vulnerabilities

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_vulns")

        _add_filter(cmd, filter, filter_id)

        return self._send_xml_command(cmd)

    def get_vulnerability(self, vulnerability_id: str) -> Any:
        """Request a single vulnerability

        Arguments:
            vulnerability_id: ID of an existing vulnerability

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not vulnerability_id:
            raise RequiredArgument(
                function="get_vulnerability", argument="vulnerability_id"
            )

        cmd = XmlCommand("get_vulns")
        cmd.set_attribute("vuln_id", vulnerability_id)
        return self._send_xml_command(cmd)

    def modify_ticket(
        self,
        ticket_id: str,
        *,
        status: Optional[TicketStatus] = None,
        note: Optional[str] = None,
        assigned_to_user_id: Optional[str] = None,
        comment: Optional[str] = None
    ) -> Any:
        """Modify a single ticket

        Arguments:
            ticket_id: UUID of an existing ticket
            status: New status for the ticket
            note: Note for the status change. Required if status is set.
            assigned_to_user_id: UUID of the user the ticket should be assigned
                to
            comment: Comment for the ticket

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not ticket_id:
            raise RequiredArgument(
                function="modify_ticket", argument="ticket_id"
            )

        if status and not note:
            raise RequiredArgument(
                "setting a status in modify_ticket requires a note argument",
                function="modify_ticket",
                argument="note",
            )

        if note and not status:
            raise RequiredArgument(
                "setting a note in modify_ticket requires a status argument",
                function="modify_ticket",
                argument="status",
            )

        cmd = XmlCommand("modify_ticket")
        cmd.set_attribute("ticket_id", ticket_id)

        if assigned_to_user_id:
            _assigned = cmd.add_element("assigned_to")
            _user = _assigned.add_element("user")
            _user.set_attribute("id", assigned_to_user_id)

        if status:
            if not isinstance(status, TicketStatus):
                raise InvalidArgument(
                    "status argument of modify_ticket needs to be a "
                    "TicketStatus",
                    function="modify_ticket",
                    argument="status",
                )

            cmd.add_element('status', status.value)
            cmd.add_element('{}_note'.format(status.name.lower()), note)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def create_filter(
        self,
        name: str,
        *,
        filter_type: Optional[FilterType] = None,
        comment: Optional[str] = None,
        term: Optional[str] = None
    ) -> Any:
        """Create a new filter

        Arguments:
            name: Name of the new filter
            filter_type: Filter for entity type
            comment: Comment for the filter
            term: Filter term e.g. 'name=foo'

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return super().create_filter(
            name, filter_type=filter_type, comment=comment, term=term
        )

    def modify_filter(
        self,
        filter_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        term: Optional[str] = None,
        filter_type: Optional[FilterType] = None
    ) -> Any:
        """Modifies an existing filter.

        Arguments:
            filter_id: UUID of the filter to be modified
            comment: Comment on filter.
            name: Name of filter.
            term: Filter term.
            filter_type: Resource type filter applies to.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not filter_id:
            raise RequiredArgument(
                function="modify_filter", argument="filter_id"
            )

        cmd = XmlCommand("modify_filter")
        cmd.set_attribute("filter_id", filter_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if term:
            cmd.add_element("term", term)

        if filter_type:
            if not isinstance(filter_type, FilterType):
                raise InvalidArgument(
                    "modify_filter requires type to be a FilterType instance. "
                    "was {}".format(filter_type),
                    function="modify_filter",
                    argument="filter_type",
                )
            cmd.add_element("type", filter_type.value)

        return self._send_xml_command(cmd)
