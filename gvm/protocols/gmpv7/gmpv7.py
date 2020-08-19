# -*- coding: utf-8 -*-
# Copyright (C) 2018 - 2019 Greenbone Networks GmbH
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

# pylint: disable=too-many-lines,redefined-builtin
"""
Module for communication with gvmd in `Greenbone Management Protocol version 7`_

.. _Greenbone Management Protocol version 7:
    https://docs.greenbone.net/API/GMP/gmp-7.0.html
"""
import base64
import collections
import logging
import numbers

from typing import Any, List, Optional, Callable

from lxml import etree

from gvm.connections import GvmConnection
from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.utils import deprecation

from gvm.xml import create_parser, XmlCommand

from gvm.protocols.base import GvmProtocol

from . import types
from .types import *  # pylint: disable=unused-wildcard-import, wildcard-import


logger = logging.getLogger(__name__)

Severity = numbers.Real


def _check_command_status(xml: str) -> bool:
    """Check gmp response

    Look into the gmp response and check for the status in the root element

    Arguments:
        xml: XML-Source

    Returns:
        True if valid, otherwise False
    """

    if xml == 0 or xml is None:
        logger.error("XML Command is empty")
        return False

    try:
        root = etree.XML(xml, parser=create_parser())
        status = root.attrib["status"]
        return status is not None and status[0] == "2"

    except etree.Error as e:
        logger.error("etree.XML(xml): %s", e)
        return False


def _to_bool(value: bool) -> str:
    return "1" if value else "0"


def _to_base64(value: str) -> bytes:
    return base64.b64encode(value.encode("utf-8"))


def _to_comma_list(value: List) -> str:
    return ",".join(value)


def _add_filter(cmd, filter, filter_id):
    if filter:
        cmd.set_attribute("filter", filter)

    if filter_id:
        cmd.set_attribute("filt_id", filter_id)


def _is_list_like(value: Any) -> bool:
    return isinstance(value, (list, tuple))


def _check_event(
    event: AlertEvent, condition: AlertCondition, method: AlertMethod
):
    if event == AlertEvent.TASK_RUN_STATUS_CHANGED:
        if not condition:
            raise RequiredArgument(
                "condition is required for event {}".format(event.name),
            )

        if not method:
            raise RequiredArgument(
                "method is required for event {}".format(event.name),
            )

        if condition not in (
            AlertCondition.ALWAYS,
            AlertCondition.FILTER_COUNT_CHANGED,
            AlertCondition.FILTER_COUNT_AT_LEAST,
            AlertCondition.SEVERITY_AT_LEAST,
        ):
            raise InvalidArgument(
                "Invalid condition {} for event {}".format(
                    condition.name, event.name
                )
            )
        if method not in (
            AlertMethod.SCP,
            AlertMethod.SEND,
            AlertMethod.SMB,
            AlertMethod.SNMP,
            AlertMethod.SYSLOG,
            AlertMethod.EMAIL,
            AlertMethod.START_TASK,
            AlertMethod.HTTP_GET,
            AlertMethod.SOURCEFIRE_CONNECTOR,
            AlertMethod.VERINICE_CONNECTOR,
        ):
            raise InvalidArgument(
                "Invalid method {} for event {}".format(method.name, event.name)
            )
    elif event in (
        AlertEvent.NEW_SECINFO_ARRIVED,
        AlertEvent.UPDATED_SECINFO_ARRIVED,
    ):
        if not condition:
            raise RequiredArgument(
                "condition is required for event {}".format(event.name),
            )

        if not method:
            raise RequiredArgument(
                "method is required for event {}".format(event.name),
            )

        if condition not in (AlertCondition.ALWAYS,):
            raise InvalidArgument(
                "Invalid condition {} for event {}".format(
                    condition.name, event.name
                )
            )
        if method not in (
            AlertMethod.SCP,
            AlertMethod.SEND,
            AlertMethod.SMB,
            AlertMethod.SNMP,
            AlertMethod.SYSLOG,
            AlertMethod.EMAIL,
        ):
            raise InvalidArgument(
                "Invalid method {} for event {}".format(method.name, event.name)
            )
    elif event is not None:
        raise InvalidArgument('Invalid event "{}"'.format(event.name))


class GmpV7Mixin(GvmProtocol):
    """Python interface for Greenbone Management Protocol

    This class implements the `Greenbone Management Protocol version 7`_

    Arguments:
        connection: Connection to use to talk with the gvmd daemon. See
            :mod:`gvm.connections` for possible connection types.
        transform: Optional transform `callable`_ to convert response data.
            After each request the callable gets passed the plain response data
            which can be used to check the data and/or conversion into different
            representations like a xml dom.

            See :mod:`gvm.transforms` for existing transforms.

    .. _Greenbone Management Protocol version 7:
        https://docs.greenbone.net/API/GMP/gmp-7.0.html
    .. _callable:
        https://docs.python.org/3/library/functions.html#callable
    """

    types = types

    def __init__(
        self,
        connection: GvmConnection,
        *,
        transform: Optional[Callable[[str], Any]] = None
    ):
        super().__init__(connection, transform=transform)

        # Is authenticated on gvmd
        self._authenticated = False

    def is_authenticated(self) -> bool:
        """Checks if the user is authenticated

        If the user is authenticated privileged GMP commands like get_tasks
        may be send to gvmd.

        Returns:
            bool: True if an authenticated connection to gvmd has been
            established.
        """
        return self._authenticated

    def authenticate(self, username: str, password: str) -> Any:
        """Authenticate to gvmd.

        The generated authenticate command will be send to server.
        Afterwards the response is read, transformed and returned.

        Arguments:
            username: Username
            password: Password

        Returns:
            Transformed response from server.
        """
        cmd = XmlCommand("authenticate")

        if not username:
            raise RequiredArgument(
                function=self.authenticate.__name__, argument='username'
            )

        if not password:
            raise RequiredArgument(
                function=self.authenticate.__name__, argument='password'
            )

        credentials = cmd.add_element("credentials")
        credentials.add_element("username", username)
        credentials.add_element("password", password)

        self._send(cmd.to_string())
        response = self._read()

        if _check_command_status(response):
            self._authenticated = True

        return self._transform(response)

    def create_agent(
        self,
        installer: str,
        signature: str,
        name: str,
        *,
        comment: Optional[str] = None,
        howto_install: Optional[str] = None,
        howto_use: Optional[str] = None
    ) -> Any:
        """Create a new agent

        Arguments:
            installer: A base64 encoded file that installs the agent on a
                target machine
            signature: A detached OpenPGP signature of the installer
            name: A name for the agent
            comment: A comment for the agent
            howto_install: A file that describes how to install the agent
            howto_use: A file that describes how to use the agent

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_agent.__name__, argument='name'
            )

        if not installer:
            raise RequiredArgument(
                function=self.create_agent.__name__, argument='installer'
            )

        if not signature:
            raise RequiredArgument(
                function=self.create_agent.__name__, argument='signature'
            )

        cmd = XmlCommand("create_agent")
        cmd.add_element("installer", installer)
        cmd.add_element("signature", signature)
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if howto_install:
            cmd.add_element("howto_install", howto_install)

        if howto_use:
            cmd.add_element("howto_use", howto_use)

        return self._send_xml_command(cmd)

    def clone_agent(self, agent_id: str) -> Any:
        """Clone an existing agent

        Arguments:
            agent_id: UUID of an existing agent to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not agent_id:
            raise RequiredArgument(
                function=self.clone_agent.__name__, argument='agent_id'
            )

        cmd = XmlCommand("create_agent")
        cmd.add_element("copy", agent_id)
        return self._send_xml_command(cmd)

    def create_alert(
        self,
        name: str,
        condition: AlertCondition,
        event: AlertEvent,
        method: AlertMethod,
        *,
        method_data: Optional[dict] = None,
        event_data: Optional[dict] = None,
        condition_data: Optional[dict] = None,
        filter_id: Optional[int] = None,
        comment: Optional[str] = None
    ) -> Any:
        """Create a new alert

        Arguments:
            name: Name of the new Alert
            condition: The condition that must be satisfied for the alert
                to occur; if the event is either 'Updated SecInfo arrived' or
                'New SecInfo arrived', condition must be 'Always'. Otherwise,
                condition can also be on of 'Severity at least', 'Filter count
                changed' or 'Filter count at least'.
            event: The event that must happen for the alert to occur, one
                of 'Task run status changed', 'Updated SecInfo arrived' or 'New
                SecInfo arrived'
            method: The method by which the user is alerted, one of 'SCP',
                'Send', 'SMB', 'SNMP', 'Syslog' or 'Email'; if the event is
                neither 'Updated SecInfo arrived' nor 'New SecInfo arrived',
                method can also be one of 'Start Task', 'HTTP Get', 'Sourcefire
                Connector' or 'verinice Connector'.
            condition_data: Data that defines the condition
            event_data: Data that defines the event
            method_data: Data that defines the method
            filter_id: Filter to apply when executing alert
            comment: Comment for the alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument='name'
            )

        if not condition:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument='condition'
            )

        if not event:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument='event'
            )

        if not method:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument='method'
            )

        if not isinstance(condition, AlertCondition):
            raise InvalidArgumentType(
                function=self.create_alert.__name__,
                argument='condition',
                arg_type=AlertCondition.__name__,
            )

        if not isinstance(event, AlertEvent):
            raise InvalidArgumentType(
                function=self.create_alert.__name__,
                argument='even',
                arg_type=AlertEvent.__name__,
            )

        if not isinstance(method, AlertMethod):
            raise InvalidArgumentType(
                function=self.create_alert.__name__,
                argument='method',
                arg_type=AlertMethod.__name__,
            )

        _check_event(event, condition, method)

        cmd = XmlCommand("create_alert")
        cmd.add_element("name", name)

        conditions = cmd.add_element("condition", condition.value)

        if condition_data is not None:
            for key, value in condition_data.items():
                _data = conditions.add_element("data", value)
                _data.add_element("name", key)

        events = cmd.add_element("event", event.value)

        if event_data is not None:
            for key, value in event_data.items():
                _data = events.add_element("data", value)
                _data.add_element("name", key)

        methods = cmd.add_element("method", method.value)

        if method_data is not None:
            for key, value in method_data.items():
                _data = methods.add_element("data", value)
                _data.add_element("name", key)

        if filter_id:
            cmd.add_element("filter", attrs={"id": filter_id})

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def clone_alert(self, alert_id: str) -> Any:
        """Clone an existing alert

        Arguments:
            alert_id: UUID of an existing alert to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not alert_id:
            raise RequiredArgument(
                function=self.clone_alert.__name__, argument='alert_id'
            )

        cmd = XmlCommand("create_alert")
        cmd.add_element("copy", alert_id)
        return self._send_xml_command(cmd)

    def create_config(self, config_id: str, name: str) -> Any:
        """Create a new scan config from an existing one

        Arguments:
            config_id: UUID of the existing scan config
            name: Name of the new scan config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_config.__name__, argument='name'
            )

        if not config_id:
            raise RequiredArgument(
                function=self.create_config.__name__, argument='config_id'
            )

        cmd = XmlCommand("create_config")
        cmd.add_element("copy", config_id)
        cmd.add_element("name", name)
        return self._send_xml_command(cmd)

    def clone_config(self, config_id: str) -> Any:
        """Clone a scan config from an existing one

        Arguments:
            config_id: UUID of the existing scan config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.clone_config.__name__, argument='config_id'
            )

        cmd = XmlCommand("create_config")
        cmd.add_element("copy", config_id)
        return self._send_xml_command(cmd)

    def import_config(self, config: str) -> Any:
        """Import a scan config from XML

        Arguments:
            config: Scan Config XML as string to import. This XML must
                contain a :code:`<get_configs_response>` root element.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config:
            raise RequiredArgument(
                function=self.import_config.__name__, argument='config'
            )

        cmd = XmlCommand("create_config")

        try:
            cmd.append_xml_str(config)
        except etree.XMLSyntaxError:
            raise InvalidArgument(
                function=self.import_config.__name__, argument='config'
            )

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
        privacy_password: Optional[str] = None
    ) -> Any:
        """Create a new credential

        Create a new credential e.g. to be used in the method of an alert.

        Currently the following credential types are supported:

            - Username + Password
            - Username + private SSH-Key
            - Client Certificates
            - SNMPv1 or SNMPv2c protocol

        Arguments:
            name: Name of the new credential
            credential_type: The credential type.
            comment: Comment for the credential
            allow_insecure: Whether to allow insecure use of the credential
            certificate: Certificate for the credential.
                Required for cc credential type.
            key_phrase: Key passphrase for the private key.
                Used for the usk credential type.
            private_key: Private key to use for login. Required
                for usk credential type. Also used for the cc credential type.
                The supported key types (dsa, rsa, ecdsa, ...) and formats (PEM,
                PKC#12, OpenSSL, ...) depend on your installed GnuTLS version.
            login: Username for the credential. Required for
                up, usk and snmp credential type.
            password: Password for the credential. Used for
                up and snmp credential types.
            community: The SNMP community.
            auth_algorithm: The SNMP authentication algorithm.
                Required for snmp credential type.
            privacy_algorithm: The SNMP privacy algorithm.
            privacy_password: The SNMP privacy password

        Examples:
            Creating a Username + Password credential

            .. code-block:: python

                gmp.create_credential(
                    name='UP Credential',
                    credential_type=CredentialType.USENAME_PASSWORD,
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

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_credential.__name__, argument='name'
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
            cmd.add_element("allow_insecure", _to_bool(allow_insecure))

        if credential_type == CredentialType.CLIENT_CERTIFICATE:
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
                    function=self.create_credential.__name__, argument="login",
                )

            cmd.add_element("login", login)

        if (
            credential_type == CredentialType.USERNAME_PASSWORD
            or credential_type == CredentialType.SNMP
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

        return self._send_xml_command(cmd)

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
                argument='credential_id',
            )

        cmd = XmlCommand("create_credential")
        cmd.add_element("copy", credential_id)
        return self._send_xml_command(cmd)

    def create_filter(
        self,
        name: str,
        *,
        make_unique: Optional[bool] = None,
        filter_type: Optional[FilterType] = None,
        comment: Optional[str] = None,
        term: Optional[str] = None
    ) -> Any:
        """Create a new filter

        Arguments:
            name: Name of the new filter
            make_unique:
            filter_type: Filter for entity type
            comment: Comment for the filter
            term: Filter term e.g. 'name=foo'

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_filter.__name__, argument="name"
            )

        cmd = XmlCommand("create_filter")
        _xmlname = cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if term:
            cmd.add_element("term", term)

        if make_unique is not None:
            cmd.add_element("make_unique", _to_bool(make_unique))

        if filter_type:
            if not isinstance(filter_type, self.types.FilterType):
                raise InvalidArgumentType(
                    function=self.create_filter.__name__,
                    argument="filter_type",
                    arg_type=self.types.FilterType.__name__,
                )

            cmd.add_element("type", filter_type.value)

        return self._send_xml_command(cmd)

    def clone_filter(self, filter_id: str) -> Any:
        """Clone an existing filter

        Arguments:
            filter_id: UUID of an existing filter to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not filter_id:
            raise RequiredArgument(
                function=self.clone_filter.__name__, argument='filter_id'
            )

        cmd = XmlCommand("create_filter")
        cmd.add_element("copy", filter_id)
        return self._send_xml_command(cmd)

    def create_group(
        self,
        name: str,
        *,
        comment: Optional[str] = None,
        special: Optional[bool] = False,
        users: Optional[List[str]] = None
    ) -> Any:
        """Create a new group

        Arguments:
            name: Name of the new group
            comment: Comment for the group
            special: Create permission giving members full access to each
                other's entities
            users: List of user names to be in the group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_group.__name__, argument='name'
            )

        cmd = XmlCommand("create_group")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if special:
            _xmlspecial = cmd.add_element("specials")
            _xmlspecial.add_element("full")

        if users:
            cmd.add_element("users", _to_comma_list(users))

        return self._send_xml_command(cmd)

    def clone_group(self, group_id: str) -> Any:
        """Clone an existing group

        Arguments:
            group_id: UUID of an existing group to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_id:
            raise RequiredArgument(
                function=self.clone_group.__name__, argument='group_id'
            )

        cmd = XmlCommand("create_group")
        cmd.add_element("copy", group_id)
        return self._send_xml_command(cmd)

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

    def create_note(
        self,
        text: str,
        nvt_oid: str,
        *,
        seconds_active: Optional[int] = None,
        hosts: Optional[List[str]] = None,
        port: Optional[int] = None,
        result_id: Optional[str] = None,
        severity: Optional[Severity] = None,
        task_id: Optional[str] = None,
        threat: Optional[SeverityLevel] = None
    ) -> Any:
        """Create a new note

        Arguments:
            text: Text of the new note
            nvt_id: OID of the nvt to which note applies
            seconds_active: Seconds note will be active. -1 on
                always, 0 off
            hosts: A list of hosts addresses
            port: Port to which the note applies
            result_id: UUID of a result to which note applies
            severity: Severity to which note applies
            task_id: UUID of task to which note applies
            threat: Severity level to which note applies. Will be converted to
                severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not text:
            raise RequiredArgument(
                function=self.create_note.__name__, argument='text'
            )

        if not nvt_oid:
            raise RequiredArgument(
                function=self.create_note.__name__, argument='nvt_oid'
            )

        cmd = XmlCommand("create_note")
        cmd.add_element("text", text)
        cmd.add_element("nvt", attrs={"oid": nvt_oid})

        if seconds_active is not None:
            cmd.add_element("active", str(seconds_active))

        if hosts:
            cmd.add_element("hosts", _to_comma_list(hosts))

        if port:
            cmd.add_element("port", str(port))

        if result_id:
            cmd.add_element("result", attrs={"id": result_id})

        if severity:
            cmd.add_element("severity", str(severity))

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})

        if threat is not None:
            if not isinstance(threat, SeverityLevel):
                raise InvalidArgumentType(
                    function="create_note",
                    argument="threat",
                    arg_type=SeverityLevel.__name__,
                )

            cmd.add_element("threat", threat.value)

        return self._send_xml_command(cmd)

    def clone_note(self, note_id: str) -> Any:
        """Clone an existing note

        Arguments:
            note_id: UUID of an existing note to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not note_id:
            raise RequiredArgument(
                function=self.clone_note.__name__, argument='note_id'
            )

        cmd = XmlCommand("create_note")
        cmd.add_element("copy", note_id)
        return self._send_xml_command(cmd)

    def create_override(
        self,
        text: str,
        nvt_oid: str,
        *,
        seconds_active: Optional[int] = None,
        hosts: Optional[List[str]] = None,
        port: Optional[int] = None,
        result_id: Optional[str] = None,
        severity: Optional[Severity] = None,
        new_severity: Optional[Severity] = None,
        task_id: Optional[str] = None,
        threat: Optional[SeverityLevel] = None,
        new_threat: Optional[SeverityLevel] = None
    ) -> Any:
        """Create a new override

        Arguments:
            text: Text of the new override
            nvt_id: OID of the nvt to which override applies
            seconds_active: Seconds override will be active. -1 on always, 0 off
            hosts: A list of host addresses
            port: Port to which the override applies
            result_id: UUID of a result to which override applies
            severity: Severity to which override applies
            new_severity: New severity for result
            task_id: UUID of task to which override applies
            threat: Severity level to which override applies. Will be converted
                to severity.
            new_threat: New severity level for results. Will be converted to
                new_severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not text:
            raise RequiredArgument(
                function=self.create_override.__name__, argument='text'
            )

        if not nvt_oid:
            raise RequiredArgument(
                function=self.create_override.__name__, argument='nvt_oid'
            )

        cmd = XmlCommand("create_override")
        cmd.add_element("text", text)
        cmd.add_element("nvt", attrs={"oid": nvt_oid})

        if seconds_active is not None:
            cmd.add_element("active", str(seconds_active))

        if hosts:
            cmd.add_element("hosts", _to_comma_list(hosts))

        if port:
            cmd.add_element("port", str(port))

        if result_id:
            cmd.add_element("result", attrs={"id": result_id})

        if severity:
            cmd.add_element("severity", str(severity))

        if new_severity:
            cmd.add_element("new_severity", str(new_severity))

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})

        if threat is not None:
            if not isinstance(threat, SeverityLevel):
                raise InvalidArgumentType(
                    function=self.create_override.__name__,
                    argument="threat",
                    arg_type=SeverityLevel.__name__,
                )

            cmd.add_element("threat", threat.value)

        if new_threat is not None:
            if not isinstance(new_threat, SeverityLevel):
                raise InvalidArgumentType(
                    function=self.create_override.__name__,
                    argument="new_threat",
                    arg_type=SeverityLevel.__name__,
                )

            cmd.add_element("new_threat", new_threat.value)

        return self._send_xml_command(cmd)

    def clone_override(self, override_id: str) -> Any:
        """Clone an existing override

        Arguments:
            override_id: UUID of an existing override to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not override_id:
            raise RequiredArgument(
                function=self.clone_override.__name__, argument='override_id'
            )

        cmd = XmlCommand("create_override")
        cmd.add_element("copy", override_id)
        return self._send_xml_command(cmd)

    def create_permission(
        self,
        name: str,
        subject_id: str,
        subject_type: PermissionSubjectType,
        *,
        resource_id: Optional[str] = None,
        resource_type: Optional[EntityType] = None,
        comment: Optional[str] = None
    ) -> Any:
        """Create a new permission

        Arguments:
            name: Name of the new permission
            subject_id: UUID of subject to whom the permission is granted
            subject_type: Type of the subject user, group or role
            comment: Comment for the permission
            resource_id: UUID of entity to which the permission applies
            resource_type: Type of the resource. For Super permissions user,
                group or role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_permission.__name__, argument='name'
            )

        if not subject_id:
            raise RequiredArgument(
                function=self.create_permission.__name__, argument='subject_id'
            )

        if not isinstance(subject_type, PermissionSubjectType):
            raise InvalidArgumentType(
                function=self.create_permission.__name__,
                argument='subject_type',
                arg_type=PermissionSubjectType.__name__,
            )

        cmd = XmlCommand("create_permission")
        cmd.add_element("name", name)

        _xmlsubject = cmd.add_element("subject", attrs={"id": subject_id})
        _xmlsubject.add_element("type", subject_type.value)

        if comment:
            cmd.add_element("comment", comment)

        if resource_id or resource_type:
            if not resource_id:
                raise RequiredArgument(
                    function=self.create_permission.__name__,
                    argument='resource_id',
                )

            if not resource_type:
                raise RequiredArgument(
                    function=self.create_permission.__name__,
                    argument='resource_type',
                )

            if not isinstance(resource_type, self.types.EntityType):
                raise InvalidArgumentType(
                    function=self.create_permission.__name__,
                    argument='resource_type',
                    arg_type=self.types.EntityType.__name__,
                )

            _xmlresource = cmd.add_element(
                "resource", attrs={"id": resource_id}
            )
            _xmlresource.add_element("type", resource_type.value)

        return self._send_xml_command(cmd)

    def clone_permission(self, permission_id: str) -> Any:
        """Clone an existing permission

        Arguments:
            permission_id: UUID of an existing permission to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not permission_id:
            raise RequiredArgument(
                function=self.clone_permission.__name__,
                argument='permission_id',
            )

        cmd = XmlCommand("create_permission")
        cmd.add_element("copy", permission_id)
        return self._send_xml_command(cmd)

    def create_port_list(
        self, name: str, port_range: str, *, comment: Optional[str] = None
    ) -> Any:
        """Create a new port list

        Arguments:
            name: Name of the new port list
            port_range: Port list ranges e.g. `"T: 1-1234"` for tcp port
                1 - 1234
            comment: Comment for the port list

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_port_list.__name__, argument='name'
            )

        if not port_range:
            raise RequiredArgument(
                function=self.create_port_list.__name__, argument='port_range'
            )

        cmd = XmlCommand("create_port_list")
        cmd.add_element("name", name)
        cmd.add_element("port_range", port_range)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def clone_port_list(self, port_list_id: str) -> Any:
        """Clone an existing port list

        Arguments:
            port_list_id: UUID of an existing port list to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument(
                function=self.clone_port_list.__name__, argument='port_list_id'
            )

        cmd = XmlCommand("create_port_list")
        cmd.add_element("copy", port_list_id)
        return self._send_xml_command(cmd)

    def create_port_range(
        self,
        port_list_id: str,
        start: int,
        end: int,
        port_range_type: PortRangeType,
        *,
        comment: Optional[str] = None
    ) -> Any:
        """Create new port range

        Arguments:
            port_list_id: UUID of the port list to which to add the range
            start: The first port in the range
            end: The last port in the range
            port_range_type: The type of the ports: TCP, UDP, ...
            comment: Comment for the port range

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument(
                function=self.create_port_range.__name__,
                argument='port_list_id',
            )

        if not port_range_type:
            raise RequiredArgument(
                function=self.create_port_range.__name__,
                argument='port_range_type',
            )

        if not start:
            raise RequiredArgument(
                function=self.create_port_range.__name__, argument='start'
            )

        if not end:
            raise RequiredArgument(
                function=self.create_port_range.__name__, argument='end'
            )

        if not isinstance(port_range_type, PortRangeType):
            raise InvalidArgumentType(
                function=self.create_port_range.__name__,
                argument='port_range_type',
                arg_type=PortRangeType.__name__,
            )

        cmd = XmlCommand("create_port_range")
        cmd.add_element("port_list", attrs={"id": port_list_id})
        cmd.add_element("start", str(start))
        cmd.add_element("end", str(end))
        cmd.add_element("type", port_range_type.value)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def import_report(
        self,
        report: str,
        *,
        task_id: Optional[str] = None,
        task_name: Optional[str] = None,
        task_comment: Optional[str] = None,
        in_assets: Optional[bool] = None
    ) -> Any:
        """Import a Report from XML

        Arguments:
            report: Report XML as string to import. This XML must contain
                a :code:`<report>` root element.
            task_id: UUID of task to import report to
            task_name: Name of task to be created if task_id is not present.
                Either task_id or task_name must be passed
            task_comment: Comment for task to be created if task_id is not
                present
            in_asset: Whether to create or update assets using the report

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report:
            raise RequiredArgument(
                function=self.import_report.__name__, argument='report'
            )

        cmd = XmlCommand("create_report")

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})
        elif task_name:
            _xmltask = cmd.add_element("task")
            _xmltask.add_element("name", task_name)

            if task_comment:
                _xmltask.add_element("comment", task_comment)
        else:
            raise RequiredArgument(
                function=self.import_report.__name__,
                argument='task_id or task_name',
            )

        if in_assets is not None:
            cmd.add_element("in_assets", _to_bool(in_assets))

        try:
            cmd.append_xml_str(report)
        except etree.XMLSyntaxError as e:
            raise InvalidArgument(
                "Invalid xml passed as report to import_report {}".format(e)
            )

        return self._send_xml_command(cmd)

    def create_role(
        self,
        name: str,
        *,
        comment: Optional[str] = None,
        users: Optional[List[str]] = None
    ) -> Any:
        """Create a new role

        Arguments:
            name: Name of the role
            comment: Comment for the role
            users: List of user names to add to the role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        if not name:
            raise RequiredArgument(
                function=self.create_role.__name__, argument='name'
            )

        cmd = XmlCommand("create_role")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if users:
            cmd.add_element("users", _to_comma_list(users))

        return self._send_xml_command(cmd)

    def clone_role(self, role_id: str) -> Any:
        """Clone an existing role

        Arguments:
            role_id: UUID of an existing role to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not role_id:
            raise RequiredArgument(
                function=self.clone_role.__name__, argument='role_id'
            )

        cmd = XmlCommand("create_role")
        cmd.add_element("copy", role_id)
        return self._send_xml_command(cmd)

    def create_scanner(
        self,
        name: str,
        host: str,
        port: int,
        scanner_type: ScannerType,
        credential_id: str,
        *,
        ca_pub: Optional[str] = None,
        comment: Optional[str] = None
    ) -> Any:
        """Create a new scanner

        Arguments:
            name: Name of the scanner
            host: The host of the scanner
            port: The port of the scanner
            scanner_type: Type of the scanner.
            credential_id: UUID of client certificate credential for the
                scanner
            ca_pub: Certificate of CA to verify scanner certificate
            comment: Comment for the scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument='name'
            )

        if not host:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument='host'
            )

        if not port:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument='port'
            )

        if not scanner_type:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument='scanner_type'
            )

        if not credential_id:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument='credential_id'
            )

        if not isinstance(scanner_type, ScannerType):
            raise InvalidArgumentType(
                function=self.create_scanner.__name__,
                argument='scanner_type',
                arg_type=ScannerType.__name__,
            )

        cmd = XmlCommand("create_scanner")
        cmd.add_element("name", name)
        cmd.add_element("host", host)
        cmd.add_element("port", str(port))
        cmd.add_element("type", scanner_type.value)

        if ca_pub:
            cmd.add_element("ca_pub", ca_pub)

        cmd.add_element("credential", attrs={"id": str(credential_id)})

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def clone_scanner(self, scanner_id: str) -> Any:
        """Clone an existing scanner

        Arguments:
            scanner_id: UUID of an existing scanner to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.clone_scanner.__name__, argument='scanner_id'
            )

        cmd = XmlCommand("create_scanner")
        cmd.add_element("copy", scanner_id)
        return self._send_xml_command(cmd)

    def create_schedule(
        self,
        name: str,
        *,
        comment: Optional[str] = None,
        first_time_minute: Optional[int] = None,
        first_time_hour: Optional[int] = None,
        first_time_day_of_month: Optional[int] = None,
        first_time_month: Optional[int] = None,
        first_time_year: Optional[int] = None,
        duration: Optional[int] = None,
        duration_unit: Optional[TimeUnit] = None,
        period: Optional[int] = None,
        period_unit: Optional[TimeUnit] = None,
        timezone: Optional[str] = None
    ) -> Any:
        """Create a new schedule

        Arguments:
            name: Name of the schedule
            comment: Comment for the schedule
            first_time_minute: First time minute the schedule will run. Must be
                an integer >= 0.
            first_time_hour: First time hour the schedule will run. Must be an
                integer >= 0.
            first_time_day_of_month: First time day of month the schedule will
                run. Must be an integer > 0 <= 31.
            first_time_month: First time month the schedule will run. Must be an
                integer >= 1 <= 12.
            first_time_year: First time year the schedule will run. Must be an
                integer >= 1970.
            duration: How long the Manager will run the scheduled task for until
                it gets paused if not finished yet. Must be an integer > 0.
            duration_unit: Unit of the duration. One of second,
                minute, hour, day, week, month, year, decade. Required if
                duration is set.
            period: How often the Manager will repeat the
                scheduled task. Must be an integer > 0.
            period_unit: Unit of the period. One of second,
                minute, hour, day, week, month, year, decade. Required if
                period is set.
            timezone: The timezone the schedule will follow

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_schedule.__name__, argument='name'
            )

        cmd = XmlCommand("create_schedule")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if (
            first_time_minute is not None
            or first_time_hour is not None
            or first_time_day_of_month is not None
            or first_time_month is not None
            or first_time_year is not None
        ):

            if first_time_minute is None:
                raise RequiredArgument(
                    function=self.create_schedule.__name__,
                    argument='first_time_minute',
                )
            elif (
                not isinstance(first_time_minute, numbers.Integral)
                or first_time_minute < 0
            ):
                raise InvalidArgument(
                    "first_time_minute argument of create_schedule needs to be "
                    "an integer greater or equal 0"
                )

            if first_time_hour is None:
                raise RequiredArgument(
                    function=self.create_schedule.__name__,
                    argument='first_time_hour',
                )
            elif (
                not isinstance(first_time_hour, numbers.Integral)
                or first_time_hour < 0
            ):
                raise InvalidArgument(
                    "first_time_hour argument of create_schedule needs to be "
                    "an integer greater or equal 0"
                )

            if first_time_day_of_month is None:
                raise RequiredArgument(
                    function=self.create_schedule.__name__,
                    argument='first_time_day_of_month',
                )
            elif (
                not isinstance(first_time_day_of_month, numbers.Integral)
                or first_time_day_of_month < 1
                or first_time_day_of_month > 31
            ):
                raise InvalidArgument(
                    "first_time_day_of_month argument of create_schedule needs "
                    "to be an integer between 1 and 31"
                )

            if first_time_month is None:
                raise RequiredArgument(
                    function=self.create_schedule.__name__,
                    argument='first_time_month',
                )
            elif (
                not isinstance(first_time_month, numbers.Integral)
                or first_time_month < 1
                or first_time_month > 12
            ):
                raise InvalidArgument(
                    "first_time_month argument of create_schedule needs "
                    "to be an integer between 1 and 12"
                )

            if first_time_year is None:
                raise RequiredArgument(
                    function=self.create_schedule.__name__,
                    argument='first_time_year',
                )
            elif (
                not isinstance(first_time_year, numbers.Integral)
                or first_time_year < 1970
            ):
                raise InvalidArgument(
                    "first_time_year argument of create_schedule needs "
                    "to be an integer greater or equal 1970"
                )

            _xmlftime = cmd.add_element("first_time")
            _xmlftime.add_element("minute", str(first_time_minute))
            _xmlftime.add_element("hour", str(first_time_hour))
            _xmlftime.add_element("day_of_month", str(first_time_day_of_month))
            _xmlftime.add_element("month", str(first_time_month))
            _xmlftime.add_element("year", str(first_time_year))

        if duration is not None:
            if not duration_unit:
                raise RequiredArgument(
                    function=self.create_schedule.__name__,
                    argument='duration_unit',
                )

            if not isinstance(duration_unit, TimeUnit):
                raise InvalidArgumentType(
                    function=self.create_schedule.__name__,
                    argument='duration_unit',
                    arg_type=TimeUnit.__name__,
                )

            if not isinstance(duration, numbers.Integral) or duration < 1:
                raise InvalidArgument(
                    "duration argument must be an integer greater than 0"
                )

            _xmlduration = cmd.add_element("duration", str(duration))
            _xmlduration.add_element("unit", duration_unit.value)

        if period is not None:
            if not period_unit:
                raise RequiredArgument(
                    function=self.create_schedule.__name__,
                    argument='period_unit',
                )

            if not isinstance(period_unit, TimeUnit):
                raise InvalidArgumentType(
                    function=self.create_schedule.__name__,
                    argument='period_unit',
                    arg_type=TimeUnit.__name__,
                )

            if not isinstance(period, numbers.Integral) or period < 0:
                raise InvalidArgument(
                    "period argument must be a positive integer"
                )

            _xmlperiod = cmd.add_element("period", str(period))
            _xmlperiod.add_element("unit", period_unit.value)

        if timezone:
            cmd.add_element("timezone", timezone)

        return self._send_xml_command(cmd)

    def clone_schedule(self, schedule_id: str) -> Any:
        """Clone an existing schedule

        Arguments:
            schedule_id: UUID of an existing schedule to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not schedule_id:
            raise RequiredArgument(
                function=self.clone_schedule.__name__, argument='schedule_id'
            )

        cmd = XmlCommand("create_schedule")
        cmd.add_element("copy", schedule_id)
        return self._send_xml_command(cmd)

    def create_tag(
        self,
        name: str,
        resource_type: EntityType,
        *,
        resource_id: Optional[str] = None,
        value: Optional[str] = None,
        comment: Optional[str] = None,
        active: Optional[bool] = None
    ) -> Any:
        """Create a new tag

        Arguments:
            name: Name of the tag. A full tag name consisting of namespace
                and predicate e.g. `foo:bar`.
            resource_id: ID of the resource the tag is to be attached to.
            resource_type: Entity type the tag is to be attached to
            value: Value associated with the tag
            comment: Comment for the tag
            active: Whether the tag should be active

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_tag.__name__, argument='name'
            )

        if not resource_type:
            raise RequiredArgument(
                function=self.create_tag.__name__, argument='resource_type'
            )

        if not isinstance(resource_type, self.types.EntityType):
            raise InvalidArgumentType(
                function=self.create_tag.__name__,
                argument='resource_type',
                arg_type=self.types.EntityType.__name__,
            )

        cmd = XmlCommand("create_tag")
        cmd.add_element("name", name)

        if not resource_id:
            resource_id = ''

        _xmlresource = cmd.add_element(
            "resource", attrs={"id": str(resource_id)}
        )
        _xmlresource.add_element("type", resource_type.value)

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

    def clone_tag(self, tag_id: str) -> Any:
        """Clone an existing tag

        Arguments:
            tag_id: UUID of an existing tag to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tag_id:
            raise RequiredArgument(
                function=self.clone_tag.__name__, argument='tag_id'
            )

        cmd = XmlCommand("create_tag")
        cmd.add_element("copy", tag_id)
        return self._send_xml_command(cmd)

    def create_target(
        self,
        name: str,
        *,
        make_unique: Optional[bool] = None,
        asset_hosts_filter: Optional[str] = None,
        hosts: Optional[List[str]] = None,
        comment: Optional[str] = None,
        exclude_hosts: Optional[List[str]] = None,
        ssh_credential_id: Optional[str] = None,
        ssh_credential_port: Optional[int] = None,
        smb_credential_id: Optional[str] = None,
        esxi_credential_id: Optional[str] = None,
        snmp_credential_id: Optional[str] = None,
        alive_test: Optional[AliveTest] = None,
        reverse_lookup_only: Optional[bool] = None,
        reverse_lookup_unify: Optional[bool] = None,
        port_range: Optional[str] = None,
        port_list_id: Optional[str] = None
    ) -> Any:
        """Create a new target

        Arguments:
            name: Name of the target
            make_unique: Append a unique suffix if the name already exists
            asset_hosts_filter: Filter to select target host from assets hosts
            hosts: List of hosts addresses to scan
            exclude_hosts: List of hosts addresses to exclude from scan
            comment: Comment for the target
            ssh_credential_id: UUID of a ssh credential to use on target
            ssh_credential_port: The port to use for ssh credential
            smb_credential_id: UUID of a smb credential to use on target
            snmp_credential_id: UUID of a snmp credential to use on target
            esxi_credential_id: UUID of a esxi credential to use on target
            alive_test: Which alive test to use
            reverse_lookup_only: Whether to scan only hosts that have names
            reverse_lookup_unify: Whether to scan only one IP when multiple IPs
                have the same name.
            port_range: Port range for the target
            port_list_id: UUID of the port list to use on target

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_target.__name__, argument='name'
            )

        cmd = XmlCommand("create_target")
        _xmlname = cmd.add_element("name", name)

        if make_unique is not None:
            _xmlname.add_element("make_unique", _to_bool(make_unique))

        if asset_hosts_filter:
            cmd.add_element(
                "asset_hosts", attrs={"filter": str(asset_hosts_filter)}
            )
        elif hosts:
            cmd.add_element("hosts", _to_comma_list(hosts))
        else:
            raise RequiredArgument(
                function=self.create_target.__name__,
                argument='hosts or asset_hosts_filter',
            )

        if comment:
            cmd.add_element("comment", comment)

        if exclude_hosts:
            cmd.add_element("exclude_hosts", _to_comma_list(exclude_hosts))

        if ssh_credential_id:
            _xmlssh = cmd.add_element(
                "ssh_credential", attrs={"id": ssh_credential_id}
            )
            if ssh_credential_port:
                _xmlssh.add_element("port", str(ssh_credential_port))

        if smb_credential_id:
            cmd.add_element("smb_credential", attrs={"id": smb_credential_id})

        if esxi_credential_id:
            cmd.add_element("esxi_credential", attrs={"id": esxi_credential_id})

        if snmp_credential_id:
            cmd.add_element("snmp_credential", attrs={"id": snmp_credential_id})

        if alive_test:
            if not isinstance(alive_test, AliveTest):
                raise InvalidArgumentType(
                    function=self.create_target.__name__,
                    argument='alive_test',
                    arg_type=AliveTest.__name__,
                )

            cmd.add_element("alive_tests", alive_test.value)

        if reverse_lookup_only is not None:
            cmd.add_element(
                "reverse_lookup_only", _to_bool(reverse_lookup_only)
            )

        if reverse_lookup_unify is not None:
            cmd.add_element(
                "reverse_lookup_unify", _to_bool(reverse_lookup_unify)
            )

        if port_range:
            cmd.add_element("port_range", port_range)

        if port_list_id:
            cmd.add_element("port_list", attrs={"id": port_list_id})

        return self._send_xml_command(cmd)

    def clone_target(self, target_id: str) -> Any:
        """Clone an existing target

        Arguments:
            target_id: UUID of an existing target to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not target_id:
            raise RequiredArgument(
                function=self.clone_target.__name__, argument='target_id'
            )

        cmd = XmlCommand("create_target")
        cmd.add_element("copy", target_id)
        return self._send_xml_command(cmd)

    def create_task(
        self,
        name: str,
        config_id: str,
        target_id: str,
        scanner_id: str,
        *,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[str] = None,
        alert_ids: Optional[List[str]] = None,
        comment: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        observers: Optional[List[str]] = None,
        preferences: Optional[dict] = None
    ) -> Any:
        """Create a new task

        Arguments:
            name: Name of the task
            config_id: UUID of scan config to use by the task
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: Comment for the task
            alterable: Whether the task should be alterable
            alert_ids: List of UUIDs for alerts to be applied to the task
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the task should be run.
            schedule_periods: A limit to the number of times the task will be
                scheduled, or 0 for no limit
            observers: List of names or ids of users which should be allowed to
                observe this task
            preferences: Name/Value pairs of scanner preferences.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_task.__name__, argument='name'
            )

        if not config_id:
            raise RequiredArgument(
                function=self.create_task.__name__, argument='config_id'
            )

        if not target_id:
            raise RequiredArgument(
                function=self.create_task.__name__, argument='target_id'
            )

        if not scanner_id:
            raise RequiredArgument(
                function=self.create_task.__name__, argument='scanner_id'
            )

        # don't allow to create a container task with create_task
        if target_id == '0':
            raise InvalidArgument(
                'Invalid argument {} for target_id'.format(target_id)
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("name", name)
        cmd.add_element("config", attrs={"id": config_id})
        cmd.add_element("target", attrs={"id": target_id})
        cmd.add_element("scanner", attrs={"id": scanner_id})

        if comment:
            cmd.add_element("comment", comment)

        if alterable is not None:
            cmd.add_element("alterable", _to_bool(alterable))

        if hosts_ordering:
            if not isinstance(hosts_ordering, HostsOrdering):
                raise InvalidArgumentType(
                    function=self.create_task.__name__,
                    argument='hosts_ordering',
                    arg_type=HostsOrdering.__name__,
                )
            cmd.add_element("hosts_ordering", hosts_ordering.value)

        if alert_ids:
            if isinstance(alert_ids, str):
                deprecation(
                    "Please pass a list as alert_ids parameter to create_task. "
                    "Passing a string is deprecated and will be removed in "
                    "future."
                )

                # if a single id is given as a string wrap it into a list
                alert_ids = [alert_ids]
            if _is_list_like(alert_ids):
                # parse all given alert id's
                for alert in alert_ids:
                    cmd.add_element("alert", attrs={"id": str(alert)})

        if schedule_id:
            cmd.add_element("schedule", attrs={"id": schedule_id})

            if schedule_periods is not None:
                if (
                    not isinstance(schedule_periods, numbers.Integral)
                    or schedule_periods < 0
                ):
                    raise InvalidArgument(
                        "schedule_periods must be an integer greater or equal "
                        "than 0"
                    )
                cmd.add_element("schedule_periods", str(schedule_periods))

        if observers is not None:
            if not _is_list_like(observers):
                raise InvalidArgumentType(
                    function=self.create_task.__name__,
                    argument='observers',
                    arg_type='list',
                )

            # gvmd splits by comma and space
            # gvmd tries to lookup each value as user name and afterwards as
            # user id. So both user name and user id are possible
            cmd.add_element("observers", _to_comma_list(observers))

        if preferences is not None:
            if not isinstance(preferences, collections.abc.Mapping):
                raise InvalidArgumentType(
                    function=self.create_task.__name__,
                    argument='preferences',
                    arg_type=collections.abc.Mapping.__name__,
                )

            _xmlprefs = cmd.add_element("preferences")
            for pref_name, pref_value in preferences.items():
                _xmlpref = _xmlprefs.add_element("preference")
                _xmlpref.add_element("scanner_name", pref_name)
                _xmlpref.add_element("value", str(pref_value))

        return self._send_xml_command(cmd)

    def create_container_task(
        self, name: str, *, comment: Optional[str] = None
    ) -> Any:
        """Create a new container task

        A container task is a "meta" task to import and view reports from other
        systems.

        Arguments:
            name: Name of the task
            comment: Comment for the task

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_container_task.__name__, argument='name'
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("name", name)
        cmd.add_element("target", attrs={"id": "0"})

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def clone_task(self, task_id: str) -> Any:
        """Clone an existing task

        Arguments:
            task_id: UUID of existing task to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.clone_task.__name__, argument='task_id'
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("copy", task_id)
        return self._send_xml_command(cmd)

    def create_user(
        self,
        name: str,
        *,
        password: Optional[str] = None,
        hosts: Optional[List[str]] = None,
        hosts_allow: Optional[bool] = False,
        ifaces: Optional[List[str]] = None,
        ifaces_allow: Optional[bool] = False,
        role_ids: Optional[List[str]] = None
    ) -> Any:
        """Create a new user

        Arguments:
            name: Name of the user
            password: Password of the user
            hosts: A list of host addresses (IPs, DNS names)
            hosts_allow: If True allow only access to passed hosts otherwise
                deny access. Default is False for deny hosts.
            ifaces: A list of interface names
            ifaces_allow: If True allow only access to passed interfaces
                otherwise deny access. Default is False for deny interfaces.
            role_ids: A list of role UUIDs for the user

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_user.__name__, argument='name'
            )

        cmd = XmlCommand("create_user")
        cmd.add_element("name", name)

        if password:
            cmd.add_element("password", password)

        if hosts:
            cmd.add_element(
                "hosts",
                _to_comma_list(hosts),
                attrs={"allow": _to_bool(hosts_allow)},
            )

        if ifaces:
            cmd.add_element(
                "ifaces",
                _to_comma_list(ifaces),
                attrs={"allow": _to_bool(ifaces_allow)},
            )

        if role_ids:
            for role in role_ids:
                cmd.add_element("role", attrs={"id": role})

        return self._send_xml_command(cmd)

    def clone_user(self, user_id: str) -> Any:
        """Clone an existing user

        Arguments:
            user_id: UUID of existing user to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not user_id:
            raise RequiredArgument(
                function=self.clone_user.__name__, argument='user_id'
            )

        cmd = XmlCommand("create_user")
        cmd.add_element("copy", user_id)
        return self._send_xml_command(cmd)

    def delete_agent(
        self, agent_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing agent

        Arguments:
            agent_id: UUID of the agent to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not agent_id:
            raise RequiredArgument(
                function=self.delete_agent.__name__, argument='agent_id'
            )

        cmd = XmlCommand("delete_agent")
        cmd.set_attribute("agent_id", agent_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_alert(
        self, alert_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing alert

        Arguments:
            alert_id: UUID of the alert to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not alert_id:
            raise RequiredArgument(
                function=self.delete_alert.__name__, argument='alert_id'
            )

        cmd = XmlCommand("delete_alert")
        cmd.set_attribute("alert_id", alert_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

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

    def delete_config(
        self, config_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing config

        Arguments:
            config_id: UUID of the config to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.delete_config.__name__, argument='config_id'
            )

        cmd = XmlCommand("delete_config")
        cmd.set_attribute("config_id", config_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

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
                argument='credential_id',
            )

        cmd = XmlCommand("delete_credential")
        cmd.set_attribute("credential_id", credential_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_filter(
        self, filter_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing filter

        Arguments:
            filter_id: UUID of the filter to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not filter_id:
            raise RequiredArgument(
                function=self.delete_filter.__name__, argument='filter_id'
            )

        cmd = XmlCommand("delete_filter")
        cmd.set_attribute("filter_id", filter_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_group(
        self, group_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing group

        Arguments:
            group_id: UUID of the group to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not group_id:
            raise RequiredArgument(
                function=self.delete_group.__name__, argument='group_id'
            )

        cmd = XmlCommand("delete_group")
        cmd.set_attribute("group_id", group_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_note(
        self, note_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing note

        Arguments:
            note_id: UUID of the note to be deleted.
            ultimate: Whether to remove entirely,or to the trashcan.
        """
        if not note_id:
            raise RequiredArgument(
                function=self.delete_note.__name__, argument='note_id'
            )

        cmd = XmlCommand("delete_note")
        cmd.set_attribute("note_id", note_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_override(
        self, override_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing override

        Arguments:
            override_id: UUID of the override to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not override_id:
            raise RequiredArgument(
                function=self.delete_override.__name__, argument='override_id'
            )

        cmd = XmlCommand("delete_override")
        cmd.set_attribute("override_id", override_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_permission(
        self, permission_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing permission

        Arguments:
            permission_id: UUID of the permission to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not permission_id:
            raise RequiredArgument(
                function=self.delete_permission.__name__,
                argument='permission_id',
            )

        cmd = XmlCommand("delete_permission")
        cmd.set_attribute("permission_id", permission_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_port_list(
        self, port_list_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing port list

        Arguments:
            port_list_id: UUID of the port list to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not port_list_id:
            raise RequiredArgument(
                function=self.delete_port_list.__name__, argument='port_list_id'
            )

        cmd = XmlCommand("delete_port_list")
        cmd.set_attribute("port_list_id", port_list_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_port_range(self, port_range_id: str) -> Any:
        """Deletes an existing port range

        Arguments:
            port_range_id: UUID of the port range to be deleted.
        """
        if not port_range_id:
            raise RequiredArgument(
                function=self.delete_port_range.__name__,
                argument='port_range_id',
            )

        cmd = XmlCommand("delete_port_range")
        cmd.set_attribute("port_range_id", port_range_id)

        return self._send_xml_command(cmd)

    def delete_report(self, report_id: str) -> Any:
        """Deletes an existing report

        Arguments:
            report_id: UUID of the report to be deleted.
        """
        if not report_id:
            raise RequiredArgument(
                function=self.delete_report.__name__, argument='report_id'
            )

        cmd = XmlCommand("delete_report")
        cmd.set_attribute("report_id", report_id)

        return self._send_xml_command(cmd)

    def delete_report_format(
        self, report_format_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing report format

        Arguments:
            report_format_id: UUID of the report format to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.delete_report_format.__name__,
                argument='report_format_id',
            )

        cmd = XmlCommand("delete_report_format")
        cmd.set_attribute("report_format_id", report_format_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_role(
        self, role_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing role

        Arguments:
            role_id: UUID of the role to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not role_id:
            raise RequiredArgument(
                function=self.delete_role.__name__, argument='role_id'
            )

        cmd = XmlCommand("delete_role")
        cmd.set_attribute("role_id", role_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_scanner(
        self, scanner_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing scanner

        Arguments:
            scanner_id: UUID of the scanner to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.delete_scanner.__name__, argument='scanner_id'
            )

        cmd = XmlCommand("delete_scanner")
        cmd.set_attribute("scanner_id", scanner_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_schedule(
        self, schedule_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing schedule

        Arguments:
            schedule_id: UUID of the schedule to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not schedule_id:
            raise RequiredArgument(
                function=self.delete_schedule.__name__, argument='schedule_id'
            )

        cmd = XmlCommand("delete_schedule")
        cmd.set_attribute("schedule_id", schedule_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_tag(
        self, tag_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing tag

        Arguments:
            tag_id: UUID of the tag to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not tag_id:
            raise RequiredArgument(
                function=self.delete_tag.__name__, argument='tag_id'
            )

        cmd = XmlCommand("delete_tag")
        cmd.set_attribute("tag_id", tag_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_target(
        self, target_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing target

        Arguments:
            target_id: UUID of the target to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not target_id:
            raise RequiredArgument(
                function=self.delete_target.__name__, argument='target_id'
            )

        cmd = XmlCommand("delete_target")
        cmd.set_attribute("target_id", target_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_task(
        self, task_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing task

        Arguments:
            task_id: UUID of the task to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.delete_task.__name__, argument='task_id'
            )

        cmd = XmlCommand("delete_task")
        cmd.set_attribute("task_id", task_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_user(
        self,
        user_id: str = None,
        *,
        name: Optional[str] = None,
        inheritor_id: Optional[str] = None,
        inheritor_name: Optional[str] = None
    ) -> Any:
        """Deletes an existing user

        Either user_id or name must be passed.

        Arguments:
            user_id: UUID of the task to be deleted.
            name: The name of the user to be deleted.
            inheritor_id: The ID of the inheriting user or "self". Overrides
                inheritor_name.
            inheritor_name: The name of the inheriting user.

        """
        if not user_id and not name:
            raise RequiredArgument(
                function=self.delete_user.__name__, argument='user_id or name'
            )

        cmd = XmlCommand("delete_user")

        if user_id:
            cmd.set_attribute("user_id", user_id)

        if name:
            cmd.set_attribute("name", name)

        if inheritor_id:
            cmd.set_attribute("inheritor_id", inheritor_id)

        if inheritor_name:
            cmd.set_attribute("inheritor_name", inheritor_name)

        return self._send_xml_command(cmd)

    def describe_auth(self) -> Any:
        """Describe authentication methods

        Returns a list of all used authentication methods if such a list is
        available.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("describe_auth"))

    def empty_trashcan(self) -> Any:
        """Empty the trashcan

        Remove all entities from the trashcan. **Attention:** this command can
        not be reverted

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("empty_trashcan"))

    def get_agents(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        format: Optional[str] = None
    ) -> Any:
        """Request a list of agents

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: True to request the agents in the trashcan
            details: Whether to include agents packageinformation when no format
                was provided
            format: One of "installer", "howto_install" or "howto_use"

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_agents")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        if format:
            if format not in ("installer", "howto_install", "howto_use"):
                raise InvalidArgument(
                    "installer argument needs to be one of installer, "
                    "howto_install or howto_use"
                )

            cmd.set_attribute("format", format)

        return self._send_xml_command(cmd)

    def get_agent(self, agent_id: str) -> Any:
        """Request a single agent

        Arguments:
            agent_id: UUID of an existing agent

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not agent_id:
            raise RequiredArgument(
                function=self.get_agent.__name__, argument='agent_id'
            )

        cmd = XmlCommand("get_agents")
        cmd.set_attribute("agent_id", agent_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_aggregates(self, resource_type: EntityType, **kwargs) -> Any:
        """Request aggregated information on a resource type

        Additional arguments can be set via the kwargs parameter, but are not
        yet validated.

        Arguments:
           resource_type: The entity type to gather data from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not resource_type:
            raise RequiredArgument(
                function=self.get_aggregates.__name__, argument='resource_type'
            )

        if not isinstance(resource_type, self.types.EntityType):
            raise InvalidArgumentType(
                function=self.get_aggregates.__name__,
                argument='resource_type',
                arg_type=self.types.EntityType.__name__,
            )

        cmd = XmlCommand("get_aggregates")

        cmd.set_attribute("type", resource_type.value)

        cmd.set_attributes(kwargs)
        return self._send_xml_command(cmd)

    def get_alerts(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None
    ) -> Any:
        """Request a list of alerts

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: True to request the alerts in the trashcan
            tasks: Whether to include the tasks using the alerts
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_alerts")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", _to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_alert(self, alert_id: str) -> Any:
        """Request a single alert

        Arguments:
            alert_id: UUID of an existing alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not alert_id:
            raise RequiredArgument(
                function=self.get_alert.__name__, argument='alert_id'
            )

        cmd = XmlCommand("get_alerts")
        cmd.set_attribute("alert_id", alert_id)
        return self._send_xml_command(cmd)

    def get_assets(
        self,
        asset_type: AssetType,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None
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

        _add_filter(cmd, filter, filter_id)

        return self._send_xml_command(cmd)

    def get_asset(self, asset_id: str, asset_type: AssetType) -> Any:
        """Request a single asset

        Arguments:
            asset_id: UUID of an existing asset
            asset_type: Either 'os' or 'host'

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
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

        cmd = XmlCommand("get_assets")
        cmd.set_attribute("asset_id", asset_id)
        cmd.set_attribute("type", asset_type.value)

        return self._send_xml_command(cmd)

    def get_credentials(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        scanners: Optional[bool] = None,
        trash: Optional[bool] = None,
        targets: Optional[bool] = None
    ) -> Any:
        """Request a list of credentials

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            scanners: Whether to include a list of scanners using the
                credentials
            trash: Whether to get the trashcan credentials instead
            targets: Whether to include a list of targets using the credentials

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_credentials")

        _add_filter(cmd, filter, filter_id)

        if scanners is not None:
            cmd.set_attribute("scanners", _to_bool(scanners))

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if targets is not None:
            cmd.set_attribute("targets", _to_bool(targets))

        return self._send_xml_command(cmd)

    def get_credential(
        self,
        credential_id: str,
        *,
        credential_format: Optional[CredentialFormat] = None
    ) -> Any:
        """Request a single credential

        Arguments:
            credential_id: UUID of an existing credential
            credential_format: One of "key", "rpm", "deb", "exe" or "pem"

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                function=self.get_credential.__name__, argument='credential_id'
            )

        cmd = XmlCommand("get_credentials")
        cmd.set_attribute("credential_id", credential_id)

        if credential_format:
            if not isinstance(credential_format, CredentialFormat):
                raise InvalidArgumentType(
                    function=self.get_credential.__name__,
                    argument='credential_format',
                    arg_type=CredentialFormat.__name__,
                )

            cmd.set_attribute("format", credential_format.value)
        return self._send_xml_command(cmd)

    def get_configs(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        families: Optional[bool] = None,
        preferences: Optional[bool] = None,
        tasks: Optional[bool] = None
    ) -> Any:
        """Request a list of scan configs

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scan configs instead
            details: Whether to get config families, preferences, nvt selectors
                and tasks.
            families: Whether to include the families if no details are
                requested
            preferences: Whether to include the preferences if no details are
                requested
            tasks: Whether to get tasks using this config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_configs")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        if families is not None:
            cmd.set_attribute("families", _to_bool(families))

        if preferences is not None:
            cmd.set_attribute("preferences", _to_bool(preferences))

        if tasks is not None:
            cmd.set_attribute("tasks", _to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_config(self, config_id: str) -> Any:
        """Request a single scan config

        Arguments:
            config_id: UUID of an existing scan config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.get_config.__name__, argument='config_id'
            )

        cmd = XmlCommand("get_configs")
        cmd.set_attribute("config_id", config_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_feeds(self) -> Any:
        """Request the list of feeds

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("get_feeds"))

    def get_feed(self, feed_type: Optional[FeedType]) -> Any:
        """Request a single feed

        Arguments:
            feed_type: Type of single feed to get: NVT, CERT or SCAP

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not feed_type:
            raise RequiredArgument(
                function=self.get_feed.__name__, argument='feed_type'
            )

        if not isinstance(feed_type, FeedType):
            raise InvalidArgumentType(
                function=self.get_feed.__name__,
                argument='feed_type',
                arg_type=FeedType.__name__,
            )

        cmd = XmlCommand("get_feeds")
        cmd.set_attribute("type", feed_type.value)

        return self._send_xml_command(cmd)

    def get_filters(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        alerts: Optional[bool] = None
    ) -> Any:
        """Request a list of filters

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan filters instead
            alerts: Whether to include list of alerts that use the filter.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_filters")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if alerts is not None:
            cmd.set_attribute("alerts", _to_bool(alerts))

        return self._send_xml_command(cmd)

    def get_filter(self, filter_id: str) -> Any:
        """Request a single filter

        Arguments:
            filter_id: UUID of an existing filter

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not filter_id:
            raise RequiredArgument(
                function=self.get_filter.__name__, argument='filter_id'
            )

        cmd = XmlCommand("get_filters")
        cmd.set_attribute("filter_id", filter_id)
        return self._send_xml_command(cmd)

    def get_groups(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None
    ) -> Any:
        """Request a list of groups

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan groups instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_groups")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        return self._send_xml_command(cmd)

    def get_group(self, group_id: str) -> Any:
        """Request a single group

        Arguments:
            group_id: UUID of an existing group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_id:
            raise RequiredArgument(
                function=self.get_group.__name__, argument='group_id'
            )

        cmd = XmlCommand("get_groups")
        cmd.set_attribute("group_id", group_id)
        return self._send_xml_command(cmd)

    def get_info_list(
        self,
        info_type: InfoType,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        name: Optional[str] = None,
        details: Optional[bool] = None
    ) -> Any:
        """Request a list of security information

        Arguments:
            info_type: Type must be either CERT_BUND_ADV, CPE, CVE,
                DFN_CERT_ADV, OVALDEF, NVT or ALLINFO
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            name: Name or identifier of the requested information
            details: Whether to include information about references to this
                information

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not info_type:
            raise RequiredArgument(
                function=self.get_info_list.__name__, argument='info_type'
            )

        if not isinstance(info_type, InfoType):
            raise InvalidArgumentType(
                function=self.get_info_list.__name__,
                argument='info_type',
                arg_type=InfoType.__name__,
            )

        cmd = XmlCommand("get_info")

        cmd.set_attribute("type", info_type.value)

        _add_filter(cmd, filter, filter_id)

        if name:
            cmd.set_attribute("name", name)

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        return self._send_xml_command(cmd)

    def get_info(self, info_id: str, info_type: InfoType) -> Any:
        """Request a single secinfo

        Arguments:
            info_id: UUID of an existing secinfo
            info_type: Type must be either CERT_BUND_ADV, CPE, CVE,
                DFN_CERT_ADV, OVALDEF, NVT or ALLINFO

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not info_type:
            raise RequiredArgument(
                function=self.get_info.__name__, argument='info_type'
            )

        if not isinstance(info_type, InfoType):
            raise InvalidArgumentType(
                function=self.get_info.__name__,
                argument='info_type',
                arg_type=InfoType.__name__,
            )

        if not info_id:
            raise RequiredArgument(
                function=self.get_info.__name__, argument='info_id'
            )

        cmd = XmlCommand("get_info")
        cmd.set_attribute("info_id", info_id)

        cmd.set_attribute("type", info_type.value)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_notes(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        details: Optional[bool] = None,
        result: Optional[bool] = None
    ) -> Any:
        """Request a list of notes

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Add info about connected results and tasks
            result: Return the details of possible connected results.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_notes")

        _add_filter(cmd, filter, filter_id)

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        if result is not None:
            cmd.set_attribute("result", _to_bool(result))

        return self._send_xml_command(cmd)

    def get_note(self, note_id: str) -> Any:
        """Request a single note

        Arguments:
            note_id: UUID of an existing note

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not note_id:
            raise RequiredArgument(
                function=self.get_note.__name__, argument='note_id'
            )

        cmd = XmlCommand("get_notes")
        cmd.set_attribute("note_id", note_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_nvts(
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
        sort_field: Optional[str] = None
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
            cmd.set_attribute("details", _to_bool(details))

        if preferences is not None:
            cmd.set_attribute("preferences", _to_bool(preferences))

        if preference_count is not None:
            cmd.set_attribute("preference_count", _to_bool(preference_count))

        if timeout is not None:
            cmd.set_attribute("timeout", _to_bool(timeout))

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

    def get_nvt(self, nvt_oid: str):
        """Request a single nvt

        Arguments:
            nvt_oid: OID of an existing nvt

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not nvt_oid:
            raise RequiredArgument(
                function=self.get_nvt.__name__, argument='nvt_oid'
            )

        cmd = XmlCommand("get_nvts")
        cmd.set_attribute("nvt_oid", nvt_oid)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

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

    def get_overrides(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        details: Optional[bool] = None,
        result: Optional[bool] = None
    ) -> Any:
        """Request a list of overrides

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include full details
            result: Whether to include results using the override

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_overrides")

        _add_filter(cmd, filter, filter_id)

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        if result is not None:
            cmd.set_attribute("result", _to_bool(result))

        return self._send_xml_command(cmd)

    def get_override(self, override_id: str) -> Any:
        """Request a single override

        Arguments:
            override_id: UUID of an existing override

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not override_id:
            raise RequiredArgument(
                function=self.get_override.__name__, argument='override_id'
            )

        cmd = XmlCommand("get_overrides")
        cmd.set_attribute("override_id", override_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_permissions(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None
    ) -> Any:
        """Request a list of permissions

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get permissions in the trashcan instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_permissions")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        return self._send_xml_command(cmd)

    def get_permission(self, permission_id: str) -> Any:
        """Request a single permission

        Arguments:
            permission_id: UUID of an existing permission

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not permission_id:
            raise RequiredArgument(
                function=self.get_permission.__name__, argument='permission_id'
            )

        cmd = XmlCommand("get_permissions")
        cmd.set_attribute("permission_id", permission_id)
        return self._send_xml_command(cmd)

    def get_port_lists(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        details: Optional[bool] = None,
        targets: Optional[bool] = None,
        trash: Optional[bool] = None
    ) -> Any:
        """Request a list of port lists

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include full port list details
            targets: Whether to include targets using this port list
            trash: Whether to get port lists in the trashcan instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_port_lists")

        _add_filter(cmd, filter, filter_id)

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        if targets is not None:
            cmd.set_attribute("targets", _to_bool(targets))

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        return self._send_xml_command(cmd)

    def get_port_list(self, port_list_id: str):
        """Request a single port list

        Arguments:
            port_list_id: UUID of an existing port list

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument(
                function=self.get_port_list.__name__, argument='port_list_id'
            )

        cmd = XmlCommand("get_port_lists")
        cmd.set_attribute("port_list_id", port_list_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_preferences(
        self, *, nvt_oid: Optional[str] = None, config_id: Optional[str] = None
    ) -> Any:
        """Request a list of preferences

        When the command includes a config_id attribute, the preference element
        includes the preference name, type and value, and the NVT to which the
        preference applies. Otherwise, the preference element includes just the
        name and value, with the NVT and type built into the name.

        Arguments:
            nvt_oid: OID of nvt
            config_id: UUID of scan config of which to show preference values

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_preferences")

        if nvt_oid:
            cmd.set_attribute("nvt_oid", nvt_oid)

        if config_id:
            cmd.set_attribute("config_id", config_id)

        return self._send_xml_command(cmd)

    def get_preference(self, name: str) -> Any:
        """Request a nvt preference


        Arguments:
            name: name of a particular preference

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.get_preference.__name__, argument='name'
            )

        cmd = XmlCommand("get_preferences")

        cmd.set_attribute("preference", name)

        return self._send_xml_command(cmd)

    def get_reports(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        note_details: Optional[bool] = None,
        override_details: Optional[bool] = None,
        no_details: Optional[bool] = None
    ) -> Any:
        """Request a list of reports

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            note_details: If notes are included, whether to include note details
            override_details: If overrides are included, whether to include
                override details
            no_details: Whether to exclude results

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_reports")

        if filter:
            cmd.set_attribute("report_filter", filter)

        if filter_id:
            cmd.set_attribute("report_filt_id", filter_id)

        if note_details is not None:
            cmd.set_attribute("note_details", _to_bool(note_details))

        if override_details is not None:
            cmd.set_attribute("override_details", _to_bool(override_details))

        if no_details is not None:
            cmd.set_attribute("details", _to_bool(not no_details))

        cmd.set_attribute("ignore_pagination", "1")

        return self._send_xml_command(cmd)

    def get_report(
        self,
        report_id: str,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        delta_report_id: Optional[str] = None,
        report_format_id: Optional[str] = None,
        ignore_pagination: Optional[bool] = None,
        details: Optional[bool] = None
    ) -> Any:
        """Request a single report

        Arguments:
            report_id: UUID of an existing report
            filter: Filter term to use to filter results in the report
            filter_id: UUID of filter to use to filter results in the report
            delta_report_id: UUID of an existing report to compare report to.
            report_format_id: UUID of report format to use
            ignore_pagination: Whether to ignore the filter terms "first" and
                "rows".
            details: Request additional report information details

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_id:
            raise RequiredArgument(
                function=self.get_report.__name__, argument='report_id'
            )

        cmd = XmlCommand("get_reports")
        cmd.set_attribute("report_id", report_id)

        _add_filter(cmd, filter, filter_id)

        if delta_report_id:
            cmd.set_attribute("delta_report_id", delta_report_id)

        if report_format_id:
            cmd.set_attribute("format_id", report_format_id)

        if ignore_pagination is not None:
            cmd.set_attribute("ignore_pagination", _to_bool(ignore_pagination))

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        return self._send_xml_command(cmd)

    def get_report_formats(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        alerts: Optional[bool] = None,
        params: Optional[bool] = None,
        details: Optional[bool] = None
    ) -> Any:
        """Request a list of report formats

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan report formats instead
            alerts: Whether to include alerts that use the report format
            params: Whether to include report format parameters
            details: Include report format file, signature and parameters

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_report_formats")

        _add_filter(cmd, filter, filter_id)

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        if alerts is not None:
            cmd.set_attribute("alerts", _to_bool(alerts))

        if params is not None:
            cmd.set_attribute("params", _to_bool(params))

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        return self._send_xml_command(cmd)

    def get_report_format(self, report_format_id: str) -> Any:
        """Request a single report format

        Arguments:
            report_format_id: UUID of an existing report format

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.get_report_format.__name__,
                argument='report_format_id',
            )

        cmd = XmlCommand("get_report_formats")
        cmd.set_attribute("report_format_id", report_format_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_results(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        task_id: Optional[str] = None,
        note_details: Optional[bool] = None,
        override_details: Optional[bool] = None,
        details: Optional[bool] = None
    ) -> Any:
        """Request a list of results

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            task_id: UUID of task for note and override handling
            note_details: If notes are included, whether to include note details
            override_details: If overrides are included, whether to include
                override details
            details: Whether to include additional details of the results

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_results")

        _add_filter(cmd, filter, filter_id)

        if task_id:
            cmd.set_attribute("task_id", task_id)

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        if note_details is not None:
            cmd.set_attribute("note_details", _to_bool(note_details))

        if override_details is not None:
            cmd.set_attribute("override_details", _to_bool(override_details))

        return self._send_xml_command(cmd)

    def get_result(self, result_id: str) -> Any:
        """Request a single result

        Arguments:
            result_id: UUID of an existing result

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not result_id:
            raise RequiredArgument(
                function=self.get_result.__name__, argument='result_id'
            )

        cmd = XmlCommand("get_results")
        cmd.set_attribute("result_id", result_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_roles(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None
    ) -> Any:
        """Request a list of roles

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan roles instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_roles")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        return self._send_xml_command(cmd)

    def get_role(self, role_id: str) -> Any:
        """Request a single role

        Arguments:
            role_id: UUID of an existing role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not role_id:
            raise RequiredArgument(
                function=self.get_role.__name__, argument='role_id'
            )

        cmd = XmlCommand("get_roles")
        cmd.set_attribute("role_id", role_id)
        return self._send_xml_command(cmd)

    def get_scanners(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None
    ) -> Any:
        """Request a list of scanners

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scanners instead
            details:  Whether to include extra details like tasks using this
                scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_scanners")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        return self._send_xml_command(cmd)

    def get_scanner(self, scanner_id: str) -> Any:
        """Request a single scanner

        Arguments:
            scanner_id: UUID of an existing scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.get_scanner.__name__, argument='scanner_id'
            )

        cmd = XmlCommand("get_scanners")
        cmd.set_attribute("scanner_id", scanner_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_schedules(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None
    ) -> Any:
        """Request a list of schedules

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan schedules instead
            tasks: Whether to include tasks using the schedules

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_schedules")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", _to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_schedule(self, schedule_id: str) -> Any:
        """Request a single schedule

        Arguments:
            schedule_id: UUID of an existing schedule

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not schedule_id:
            raise RequiredArgument(
                function=self.get_schedule.__name__, argument='schedule_id'
            )

        cmd = XmlCommand("get_schedules")
        cmd.set_attribute("schedule_id", schedule_id)
        return self._send_xml_command(cmd)

    def get_settings(self, *, filter: Optional[str] = None) -> Any:
        """Request a list of user settings

        Arguments:
            filter: Filter term to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_settings")

        if filter:
            cmd.set_attribute("filter", filter)

        return self._send_xml_command(cmd)

    def get_setting(self, setting_id: str) -> Any:
        """Request a single setting

        Arguments:
            setting_id: UUID of an existing setting

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not setting_id:
            raise RequiredArgument(
                function=self.get_setting.__name__, argument='setting_id'
            )

        cmd = XmlCommand("get_settings")
        cmd.set_attribute("setting_id", setting_id)
        return self._send_xml_command(cmd)

    def get_system_reports(
        self,
        *,
        name: Optional[str] = None,
        duration: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        brief: Optional[bool] = None,
        slave_id: Optional[str] = None
    ) -> Any:
        """Request a list of system reports

        Arguments:
            name: A string describing the required system report
            duration: The number of seconds into the past that the system report
                should include
            start_time: The start of the time interval the system report should
                include in ISO time format
            end_time: The end of the time interval the system report should
                include in ISO time format
            brief: Whether to include the actual system reports
            slave_id: UUID of GMP scanner from which to get the system reports

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_system_reports")

        if name:
            cmd.set_attribute("name", name)

        if duration is not None:
            if not isinstance(duration, numbers.Integral):
                raise InvalidArgument("duration needs to be an integer number")

            cmd.set_attribute("duration", str(duration))

        if start_time:
            cmd.set_attribute("start_time", str(start_time))

        if end_time:
            cmd.set_attribute("end_time", str(end_time))

        if brief is not None:
            cmd.set_attribute("brief", _to_bool(brief))

        if slave_id:
            cmd.set_attribute("slave_id", slave_id)

        return self._send_xml_command(cmd)

    def get_tags(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        names_only: Optional[bool] = None
    ) -> Any:
        """Request a list of tags

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get tags from the trashcan instead
            names_only: Whether to get only distinct tag names

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tags")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if names_only is not None:
            cmd.set_attribute("names_only", _to_bool(names_only))

        return self._send_xml_command(cmd)

    def get_tag(self, tag_id: str) -> Any:
        """Request a single tag

        Arguments:
            tag_id: UUID of an existing tag

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tag_id:
            raise RequiredArgument(
                function=self.get_tag.__name__, argument='tag_id'
            )

        cmd = XmlCommand("get_tags")
        cmd.set_attribute("tag_id", tag_id)
        return self._send_xml_command(cmd)

    def get_targets(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None
    ) -> Any:
        """Request a list of targets

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan targets instead
            tasks: Whether to include list of tasks that use the target

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_targets")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", _to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_target(self, target_id: str) -> Any:
        """Request a single target

        Arguments:
            target_id: UUID of an existing target

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not target_id:
            raise RequiredArgument(
                function=self.get_target.__name__, argument='target_id'
            )

        cmd = XmlCommand("get_targets")
        cmd.set_attribute("target_id", target_id)
        return self._send_xml_command(cmd)

    def get_tasks(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        schedules_only: Optional[bool] = None
    ) -> Any:
        """Request a list of tasks

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan tasks instead
            details: Whether to include full task details
            schedules_only: Whether to only include id, name and schedule
                details

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tasks")

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        if schedules_only is not None:
            cmd.set_attribute("schedules_only", _to_bool(schedules_only))

        return self._send_xml_command(cmd)

    def get_task(self, task_id: str) -> Any:
        """Request a single task

        Arguments:
            task_id: UUID of an existing task

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.get_task.__name__, argument='task_id'
            )

        cmd = XmlCommand("get_tasks")
        cmd.set_attribute("task_id", task_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_users(
        self, *, filter: Optional[str] = None, filter_id: Optional[str] = None
    ) -> Any:
        """Request a list of users

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_users")

        _add_filter(cmd, filter, filter_id)

        return self._send_xml_command(cmd)

    def get_user(self, user_id: str) -> Any:
        """Request a single user

        Arguments:
            user_id: UUID of an existing user

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not user_id:
            raise RequiredArgument(
                function=self.get_user.__name__, argument='user_id'
            )

        cmd = XmlCommand("get_users")
        cmd.set_attribute("user_id", user_id)
        return self._send_xml_command(cmd)

    def get_version(self) -> Any:
        """Get the Greenbone Manager Protocol version used by the remote gvmd

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("get_version"))

    def help(
        self, *, format: Optional[str] = None, help_type: Optional[str] = ""
    ) -> Any:
        """Get the help text

        Arguments:
            format: One of "html", "rnc", "text" or "xml
            help_type: One of "brief" or "". Default ""

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("help")

        if help_type not in ("", "brief"):
            raise InvalidArgument(
                'help_type argument must be an empty string or "brief"'
            )

        cmd.set_attribute("type", help_type)

        if format:
            if not format.lower() in ("html", "rnc", "text", "xml"):
                raise InvalidArgument(
                    "help format Argument must be one of html, rnc, text or "
                    "xml"
                )

            cmd.set_attribute("format", format)

        return self._send_xml_command(cmd)

    def modify_agent(
        self,
        agent_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None
    ) -> Any:
        """Modifies an existing agent

        Arguments:
            agent_id: UUID of the agent to be modified.
            name: Name of the new credential
            comment: Comment for the credential

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not agent_id:
            raise RequiredArgument(
                function=self.modify_agent.__name__, argument='agent_id'
            )

        cmd = XmlCommand("modify_agent")
        cmd.set_attribute("agent_id", str(agent_id))

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def modify_alert(
        self,
        alert_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        filter_id: Optional[str] = None,
        event: Optional[AlertEvent] = None,
        event_data: Optional[dict] = None,
        condition: Optional[AlertCondition] = None,
        condition_data: Optional[dict] = None,
        method: Optional[AlertMethod] = None,
        method_data: Optional[dict] = None
    ) -> Any:
        """Modifies an existing alert.

        Arguments:
            alert_id: UUID of the alert to be modified.
            name: Name of the Alert.
            condition: The condition that must be satisfied for the alert to
                occur. If the event is either 'Updated SecInfo
                arrived' or 'New SecInfo arrived', condition must be 'Always'.
                Otherwise, condition can also be on of 'Severity at least',
                'Filter count changed' or 'Filter count at least'.
            condition_data: Data that defines the condition
            event: The event that must happen for the alert to occur, one of
                'Task run status changed', 'Updated SecInfo arrived' or
                'New SecInfo arrived'
            event_data: Data that defines the event
            method: The method by which the user is alerted, one of 'SCP',
                'Send', 'SMB', 'SNMP', 'Syslog' or 'Email';
                if the event is neither 'Updated SecInfo arrived' nor
                'New SecInfo arrived', method can also be one of 'Start Task',
                'HTTP Get', 'Sourcefire Connector' or 'verinice Connector'.
            method_data: Data that defines the method
            filter_id: Filter to apply when executing alert
            comment: Comment for the alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        if not alert_id:
            raise RequiredArgument(
                function=self.modify_alert.__name__, argument='alert_id'
            )

        cmd = XmlCommand("modify_alert")
        cmd.set_attribute("alert_id", str(alert_id))

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if filter_id:
            cmd.add_element("filter", attrs={"id": filter_id})

        if condition:
            if not isinstance(condition, AlertCondition):
                raise InvalidArgumentType(
                    function=self.modify_alert.__name__,
                    argument='condition',
                    arg_type=AlertCondition.__name__,
                )

            conditions = cmd.add_element("condition", condition.value)

            if condition_data is not None:
                for key, value in condition_data.items():
                    _data = conditions.add_element("data", value)
                    _data.add_element("name", key)

        if method:
            if not isinstance(method, AlertMethod):
                raise InvalidArgumentType(
                    function=self.modify_alert.__name__,
                    argument='method',
                    arg_type=AlertMethod.__name__,
                )

            methods = cmd.add_element("method", method.value)

            if method_data is not None:
                for key, value in method_data.items():
                    _data = methods.add_element("data", value)
                    _data.add_element("name", key)

        if event:
            if not isinstance(event, AlertEvent):
                raise InvalidArgumentType(
                    function=self.modify_alert.__name__,
                    argument='event',
                    arg_type=AlertEvent.__name__,
                )

            _check_event(event, condition, method)

            events = cmd.add_element("event", event.value)

            if event_data is not None:
                for key, value in event_data.items():
                    _data = events.add_element("data", value)
                    _data.add_element("name", key)

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

    def modify_auth(self, group_name: str, auth_conf_settings: dict) -> Any:
        """Modifies an existing auth.

        Arguments:
            group_name: Name of the group to be modified.
            auth_conf_settings: The new auth config.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_name:
            raise RequiredArgument(
                function=self.modify_auth.__name__, argument='group_name'
            )
        if not auth_conf_settings:
            raise RequiredArgument(
                function=self.modify_auth.__name__,
                argument='auth_conf_settings',
            )
        cmd = XmlCommand("modify_auth")
        _xmlgroup = cmd.add_element("group", attrs={"name": str(group_name)})

        for key, value in auth_conf_settings.items():
            _xmlauthconf = _xmlgroup.add_element("auth_conf_setting")
            _xmlauthconf.add_element("key", key)
            _xmlauthconf.add_element("value", value)

        return self._send_xml_command(cmd)

    def modify_config_set_nvt_preference(
        self,
        config_id: str,
        name: str,
        nvt_oid: str,
        *,
        value: Optional[str] = None
    ) -> Any:
        """Modifies the nvt preferences of an existing scan config.

        Arguments:
            config_id: UUID of scan config to modify.
            name: Name for preference to change.
            nvt_oid: OID of the NVT associated with preference to modify
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_config_set_nvt_preference.__name__,
                argument='config_id',
            )

        if not nvt_oid:
            raise RequiredArgument(
                function=self.modify_config_set_nvt_preference.__name__,
                argument='nvt_oid',
            )

        if not name:
            raise RequiredArgument(
                function=self.modify_config_set_nvt_preference.__name__,
                argument='name',
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        _xmlpref = cmd.add_element("preference")

        _xmlpref.add_element("nvt", attrs={"oid": nvt_oid})
        _xmlpref.add_element("name", name)

        if value:
            _xmlpref.add_element("value", _to_base64(value))

        return self._send_xml_command(cmd)

    def modify_config_set_comment(
        self, config_id: str, comment: Optional[str] = ""
    ) -> Any:
        """Modifies the comment of an existing scan config

        Arguments:
            config_id: UUID of scan config to modify.
            comment: Comment to set on a config. Default: ''
        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_config_set_comment.__name__,
                argument='config_id argument',
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def modify_config_set_scanner_preference(
        self, config_id: str, name: str, *, value: Optional[str] = None
    ) -> Any:
        """Modifies the scanner preferences of an existing scan config

        Arguments:
            config_id: UUID of scan config to modify.
            name: Name of the scanner preference to change
            value: New value for the preference. None to delete the preference
                and to use the default instead.

        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_config_set_scanner_preference.__name__,
                argument='config_id',
            )

        if not name:
            raise RequiredArgument(
                function=self.modify_config_set_scanner_preference.__name__,
                argument='name argument',
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        _xmlpref = cmd.add_element("preference")

        _xmlpref.add_element("name", name)

        if value:
            _xmlpref.add_element("value", _to_base64(value))

        return self._send_xml_command(cmd)

    def modify_config_set_nvt_selection(
        self, config_id: str, family: str, nvt_oids: List[str]
    ) -> Any:
        """Modifies the selected nvts of an existing scan config

        The manager updates the given family in the config to include only the
        given NVTs.

        Arguments:
            config_id: UUID of scan config to modify.
            family: Name of the NVT family to include NVTs from
            nvt_oids: List of NVTs to select for the family.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_config_set_nvt_selection.__name__,
                argument='config_id',
            )

        if not family:
            raise RequiredArgument(
                function=self.modify_config_set_nvt_selection.__name__,
                argument='family argument',
            )

        if not _is_list_like(nvt_oids):
            raise InvalidArgumentType(
                function=self.modify_config_set_nvt_selection.__name__,
                argument='nvt_oids',
                arg_type='list',
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        _xmlnvtsel = cmd.add_element("nvt_selection")
        _xmlnvtsel.add_element("family", family)

        for nvt in nvt_oids:
            _xmlnvtsel.add_element("nvt", attrs={"oid": nvt})

        return self._send_xml_command(cmd)

    def modify_config_set_family_selection(
        self,
        config_id: str,
        families: List[str],
        *,
        auto_add_new_families: Optional[bool] = True,
        auto_add_new_nvts: Optional[bool] = True
    ) -> Any:
        """
        Selected the NVTs of a scan config at a family level.

        Arguments:
            config_id: UUID of scan config to modify.
            families: List of NVT family names to select.
            auto_add_new_families: Whether new families should be added to the
                scan config automatically. Default: True.
            auto_add_new_nvts: Whether new NVTs in the selected families should
                be added to the scan config automatically. Default: True.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_config_set_family_selection.__name__,
                argument='config_id',
            )

        if not _is_list_like(families):
            raise InvalidArgumentType(
                function=self.modify_config_set_family_selection.__name__,
                argument='families',
                arg_type='list',
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        _xmlfamsel = cmd.add_element("family_selection")
        _xmlfamsel.add_element("growing", _to_bool(auto_add_new_families))

        for family in families:
            _xmlfamily = _xmlfamsel.add_element("family")
            _xmlfamily.add_element("name", family)
            _xmlfamily.add_element("all", "1")
            _xmlfamily.add_element("growing", _to_bool(auto_add_new_nvts))

        return self._send_xml_command(cmd)

    def modify_config(
        self, config_id: str, selection: Optional[str] = None, **kwargs
    ) -> Any:
        """Modifies an existing scan config.

        DEPRECATED. Please use *modify_config_set_* methods instead.

        modify_config has four modes to operate depending on the selection.

        Arguments:
            config_id: UUID of scan config to modify.
            selection: one of 'scan_pref', 'nvt_pref', 'nvt_selection' or
                'family_selection'
            name: New name for preference.
            value: New value for preference.
            nvt_oids: List of NVTs associated with preference to modify.
            family: Name of family to modify.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_config.__name__,
                argument='config_id argument',
            )

        if selection is None:
            deprecation(
                "Using modify_config to update the comment of a scan config is"
                "deprecated. Please use modify_config_set_comment instead."
            )
            return self.modify_config_set_comment(
                config_id, kwargs.get("comment")
            )

        if selection not in (
            "nvt_pref",
            "scan_pref",
            "family_selection",
            "nvt_selection",
        ):
            raise InvalidArgument(
                "selection must be one of nvt_pref, "
                "scan_pref, family_selection or "
                "nvt_selection"
            )

        if selection == "nvt_pref":
            deprecation(
                "Using modify_config to update a nvt preference of a scan "
                "config is deprecated. Please use "
                "modify_config_set_nvt_preference instead."
            )
            return self.modify_config_set_nvt_preference(config_id, **kwargs)

        if selection == "scan_pref":
            deprecation(
                "Using modify_config to update a scanner preference of a "
                "scan config is deprecated. Please use "
                "modify_config_set_scanner_preference instead."
            )
            return self.modify_config_set_scanner_preference(
                config_id, **kwargs
            )

        if selection == "nvt_selection":
            deprecation(
                "Using modify_config to update a nvt selection of a "
                "scan config is deprecated. Please use "
                "modify_config_set_nvt_selection instead."
            )
            return self.modify_config_set_nvt_selection(config_id, **kwargs)

        deprecation(
            "Using modify_config to update a family selection of a "
            "scan config is deprecated. Please use "
            "modify_config_set_family_selection instead."
        )
        return self.modify_config_set_family_selection(config_id, **kwargs)

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
        privacy_password: Optional[str] = None
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
            auth_algorithm: The SNMP auth algorithm.
            community: The SNMP community
            privacy_algorithm: The SNMP privacy algorithm.
            privacy_password: The SNMP privacy password

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                function=self.modify_credential.__name__,
                argument='credential_id attribute',
            )

        cmd = XmlCommand("modify_credential")
        cmd.set_attribute("credential_id", credential_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", _to_bool(allow_insecure))

        if certificate:
            cmd.add_element("certificate", certificate)

        if key_phrase is not None and not private_key:
            raise RequiredArgument(
                function=self.modify_credential.__name__, argument='private_key'
            )

        if private_key:
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("private", private_key)

            if key_phrase is not None:
                _xmlkey.add_element("phrase", key_phrase)

        if login:
            cmd.add_element("login", login)

        if password:
            cmd.add_element("password", password)

        if auth_algorithm is not None:
            if not isinstance(auth_algorithm, SnmpAuthAlgorithm):
                raise InvalidArgumentType(
                    function=self.modify_credential.__name__,
                    argument='auth_algorithm',
                    arg_type=SnmpAuthAlgorithm.__name__,
                )
            cmd.add_element("auth_algorithm", auth_algorithm.value)

        if community:
            cmd.add_element("community", community)

        if privacy_algorithm is not None:
            if not isinstance(privacy_algorithm, SnmpPrivacyAlgorithm):
                raise InvalidArgumentType(
                    function=self.modify_credential.__name__,
                    argument='privacy_algorithm',
                    arg_type=SnmpPrivacyAlgorithm.__name__,
                )

            _xmlprivacy = cmd.add_element("privacy")
            _xmlprivacy.add_element("algorithm", privacy_algorithm.value)

            if privacy_password is not None:
                _xmlprivacy.add_element("password", privacy_password)

        return self._send_xml_command(cmd)

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
            filter_type: Filter type the filter applies to.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not filter_id:
            raise RequiredArgument(
                function=self.modify_filter.__name__, argument='filter_id'
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
            if not isinstance(filter_type, self.types.FilterType):
                raise InvalidArgumentType(
                    function=self.modify_filter.__name__,
                    argument='filter_type',
                    arg_type=self.types.FilterType.__name__,
                )
            cmd.add_element("type", filter_type.value)

        return self._send_xml_command(cmd)

    def modify_group(
        self,
        group_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        users: Optional[List[str]] = None
    ) -> Any:
        """Modifies an existing group.

        Arguments:
            group_id: UUID of group to modify.
            comment: Comment on group.
            name: Name of group.
            users: List of user names to be in the group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_id:
            raise RequiredArgument(
                function=self.modify_group.__name__, argument='group_id'
            )

        cmd = XmlCommand("modify_group")
        cmd.set_attribute("group_id", group_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if users:
            cmd.add_element("users", _to_comma_list(users))

        return self._send_xml_command(cmd)

    def modify_note(
        self,
        note_id: str,
        text: str,
        *,
        seconds_active: Optional[int] = None,
        hosts: Optional[List[str]] = None,
        port: Optional[int] = None,
        result_id: Optional[str] = None,
        severity: Optional[Severity] = None,
        task_id: Optional[str] = None,
        threat: Optional[SeverityLevel] = None
    ) -> Any:
        """Modifies an existing note.

        Arguments:
            note_id: UUID of note to modify.
            text: The text of the note.
            seconds_active: Seconds note will be active. -1 on always, 0 off.
            hosts: A list of hosts addresses
            port: Port to which note applies.
            result_id: Result to which note applies.
            severity: Severity to which note applies.
            task_id: Task to which note applies.
            threat: Threat level to which note applies. Will be converted to
                severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not note_id:
            raise RequiredArgument(
                function=self.modify_note.__name__, argument='note_id'
            )

        if not text:
            raise RequiredArgument(
                function=self.modify_note.__name__, argument='text'
            )

        cmd = XmlCommand("modify_note")
        cmd.set_attribute("note_id", note_id)
        cmd.add_element("text", text)

        if seconds_active is not None:
            cmd.add_element("active", str(seconds_active))

        if hosts:
            cmd.add_element("hosts", _to_comma_list(hosts))

        if port:
            cmd.add_element("port", str(port))

        if result_id:
            cmd.add_element("result", attrs={"id": result_id})

        if severity:
            cmd.add_element("severity", str(severity))

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})

        if threat is not None:

            if not isinstance(threat, SeverityLevel):
                raise InvalidArgumentType(
                    function=self.modify_note.__name__,
                    argument='threat',
                    arg_type=SeverityLevel.__name__,
                )

            cmd.add_element("threat", threat.value)

        return self._send_xml_command(cmd)

    def modify_override(
        self,
        override_id: str,
        text: str,
        *,
        seconds_active: Optional[int] = None,
        hosts: Optional[List[str]] = None,
        port: Optional[int] = None,
        result_id: Optional[str] = None,
        severity: Optional[Severity] = None,
        new_severity: Optional[Severity] = None,
        task_id: Optional[str] = None,
        threat: Optional[SeverityLevel] = None,
        new_threat: Optional[SeverityLevel] = None
    ) -> Any:
        """Modifies an existing override.

        Arguments:
            override_id: UUID of override to modify.
            text: The text of the override.
            seconds_active: Seconds override will be active. -1 on always,
                0 off.
            hosts: A list of host addresses
            port: Port to which override applies.
            result_id: Result to which override applies.
            severity: Severity to which override applies.
            new_severity: New severity score for result.
            task_id: Task to which override applies.
            threat: Threat level to which override applies.
                Will be converted to severity.
            new_threat: New threat level for results. Will be converted to
                new_severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not override_id:
            raise RequiredArgument(
                function=self.modify_override.__name__, argument='override_id'
            )
        if not text:
            raise RequiredArgument(
                function=self.modify_override.__name__, argument='text'
            )

        cmd = XmlCommand("modify_override")
        cmd.set_attribute("override_id", override_id)
        cmd.add_element("text", text)

        if seconds_active is not None:
            cmd.add_element("active", str(seconds_active))

        if hosts:
            cmd.add_element("hosts", _to_comma_list(hosts))

        if port:
            cmd.add_element("port", str(port))

        if result_id:
            cmd.add_element("result", attrs={"id": result_id})

        if severity:
            cmd.add_element("severity", str(severity))

        if new_severity:
            cmd.add_element("new_severity", str(new_severity))

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})

        if threat is not None:
            if not isinstance(threat, SeverityLevel):
                raise InvalidArgumentType(
                    function=self.modify_override.__name__,
                    argument='threat',
                    arg_type=SeverityLevel.__name__,
                )
            cmd.add_element("threat", threat.value)

        if new_threat is not None:
            if not isinstance(new_threat, SeverityLevel):
                raise InvalidArgumentType(
                    function=self.modify_override.__name__,
                    argument='new_threat',
                    arg_type=SeverityLevel.__name__,
                )

            cmd.add_element("new_threat", new_threat.value)

        return self._send_xml_command(cmd)

    def modify_permission(
        self,
        permission_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[EntityType] = None,
        subject_id: Optional[str] = None,
        subject_type: Optional[PermissionSubjectType] = None
    ) -> Any:
        """Modifies an existing permission.

        Arguments:
            permission_id: UUID of permission to be modified.
            comment: The comment on the permission.
            name: Permission name, currently the name of a command.
            subject_id: UUID of subject to whom the permission is granted
            subject_type: Type of the subject user, group or role
            resource_id: UUID of entity to which the permission applies
            resource_type: Type of the resource. For Super permissions user,
                group or role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not permission_id:
            raise RequiredArgument(
                function=self.modify_permission.__name__,
                argument='permission_id',
            )

        cmd = XmlCommand("modify_permission")
        cmd.set_attribute("permission_id", permission_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if resource_id or resource_type:
            if not resource_id:
                raise RequiredArgument(
                    function=self.modify_permission.__name__,
                    argument='resource_id',
                )

            if not resource_type:
                raise RequiredArgument(
                    function=self.modify_permission.__name__,
                    argument='resource_type',
                )

            if not isinstance(resource_type, self.types.EntityType):
                raise InvalidArgumentType(
                    function=self.modify_permission.__name__,
                    argument='resource_type',
                    arg_type=self.types.EntityType.__name__,
                )

            _xmlresource = cmd.add_element(
                "resource", attrs={"id": resource_id}
            )
            _xmlresource.add_element("type", resource_type.value)

        if subject_id or subject_type:
            if not subject_id:
                raise RequiredArgument(
                    function=self.modify_permission.__name__,
                    argument='subject_id',
                )

            if not isinstance(subject_type, PermissionSubjectType):
                raise InvalidArgumentType(
                    function=self.modify_permission.__name__,
                    argument='subject_type',
                    arg_type=PermissionSubjectType.__name__,
                )

            _xmlsubject = cmd.add_element("subject", attrs={"id": subject_id})
            _xmlsubject.add_element("type", subject_type.value)

        return self._send_xml_command(cmd)

    def modify_port_list(
        self,
        port_list_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None
    ) -> Any:
        """Modifies an existing port list.

        Arguments:
            port_list_id: UUID of port list to modify.
            name: Name of port list.
            comment: Comment on port list.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument(
                function=self.modify_port_list.__name__, argument='port_list_id'
            )
        cmd = XmlCommand("modify_port_list")
        cmd.set_attribute("port_list_id", port_list_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        return self._send_xml_command(cmd)

    def modify_report_format(
        self,
        report_format_id: str,
        *,
        active: Optional[bool] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        param_name: Optional[str] = None,
        param_value: Optional[str] = None
    ) -> Any:
        """Modifies an existing report format.

        Arguments:
            report_format_id: UUID of report format to modify.
            active: Whether the report format is active.
            name: The name of the report format.
            summary: A summary of the report format.
            param_name: The name of the param.
            param_value: The value of the param.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.modify_report_format.__name__,
                argument='report_format_id',
            )

        cmd = XmlCommand("modify_report_format")
        cmd.set_attribute("report_format_id", report_format_id)

        if active is not None:
            cmd.add_element("active", _to_bool(active))

        if name:
            cmd.add_element("name", name)

        if summary:
            cmd.add_element("summary", summary)

        if param_name:
            _xmlparam = cmd.add_element("param")
            _xmlparam.add_element("name", param_name)

            if param_value is not None:
                _xmlparam.add_element("value", param_value)

        return self._send_xml_command(cmd)

    def modify_role(
        self,
        role_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        users: Optional[List[str]] = None
    ) -> Any:
        """Modifies an existing role.

        Arguments:
            role_id: UUID of role to modify.
            comment: Name of role.
            name: Comment on role.
            users: List of user names.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not role_id:
            raise RequiredArgument(
                function=self.modify_role.__name__, argument='role_id argument'
            )

        cmd = XmlCommand("modify_role")
        cmd.set_attribute("role_id", role_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if users:
            cmd.add_element("users", _to_comma_list(users))

        return self._send_xml_command(cmd)

    def modify_scanner(
        self,
        scanner_id: str,
        *,
        scanner_type: Optional[ScannerType] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        ca_pub: Optional[str] = None,
        credential_id: Optional[str] = None
    ) -> Any:
        """Modifies an existing scanner.

        Arguments:
            scanner_id: UUID of scanner to modify.
            scanner_type: New type of the Scanner.
            host: Host of the scanner.
            port: Port of the scanner.
            comment: Comment on scanner.
            name: Name of scanner.
            ca_pub: Certificate of CA to verify scanner's certificate.
            credential_id: UUID of the client certificate credential for the
                Scanner.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.modify_scanner.__name__,
                argument='scanner_id argument',
            )

        cmd = XmlCommand("modify_scanner")
        cmd.set_attribute("scanner_id", scanner_id)

        if scanner_type is not None:
            if not isinstance(scanner_type, ScannerType):
                raise InvalidArgumentType(
                    function=self.modify_scanner.__name__,
                    argument='scanner_type',
                    arg_type=ScannerType.__name__,
                )

            cmd.add_element("type", scanner_type.value)

        if host:
            cmd.add_element("host", host)

        if port:
            cmd.add_element("port", str(port))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if ca_pub:
            cmd.add_element("ca_pub", ca_pub)

        if credential_id:
            cmd.add_element("credential", attrs={"id": str(credential_id)})

        return self._send_xml_command(cmd)

    def modify_schedule(
        self,
        schedule_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        first_time_minute: Optional[int] = None,
        first_time_hour: Optional[int] = None,
        first_time_day_of_month: Optional[int] = None,
        first_time_month: Optional[int] = None,
        first_time_year: Optional[int] = None,
        duration: Optional[int] = None,
        duration_unit: Optional[TimeUnit] = None,
        period: Optional[int] = None,
        period_unit: Optional[TimeUnit] = None,
        timezone: Optional[str] = None
    ) -> Any:
        """Modifies an existing schedule.

        Arguments:
            schedule_id: UUID of schedule to modify.
            name: Name of the schedule
            comment: Comment for the schedule
            first_time_minute: First time minute the schedule will run. Must be
                an integer >= 0.
            first_time_hour: First time hour the schedule will run. Must be an
                integer >= 0.
            first_time_day_of_month: First time day of month the schedule will
                run. Must be an integer > 0 <= 31.
            first_time_month: First time month the schedule will run. Must be an
                integer >= 1 <= 12.
            first_time_year: First time year the schedule will run
            duration: How long the Manager will run the scheduled task for until
                it gets paused if not finished yet.
            duration_unit: Unit of the duration. One of second, minute, hour,
                day, week, month, year, decade. Required if duration is set.
            period: How often the Manager will repeat the scheduled task. Must
                be an integer > 0.
            period_unit: Unit of the period. One of second, minute, hour, day,
                week, month, year, decade. Required if period is set.
            timezone: The timezone the schedule will follow

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not schedule_id:
            raise RequiredArgument(
                function=self.modify_schedule.__name__, argument='schedule_id'
            )

        cmd = XmlCommand("modify_schedule")
        cmd.set_attribute("schedule_id", schedule_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if (
            first_time_minute is not None
            or first_time_hour is not None
            or first_time_day_of_month is not None
            or first_time_month is not None
            or first_time_year is not None
        ):

            if first_time_minute is None:
                raise RequiredArgument(
                    function=self.modify_schedule.__name__,
                    argument='first_time_minute',
                )
            elif (
                not isinstance(first_time_minute, numbers.Integral)
                or first_time_minute < 0
            ):
                raise InvalidArgument(
                    "first_time_minute argument of modify_schedule needs to be "
                    "an integer greater or equal 0"
                )

            if first_time_hour is None:
                raise RequiredArgument(
                    function=self.modify_schedule.__name__,
                    argument='first_time_hour',
                )
            elif (
                not isinstance(first_time_hour, numbers.Integral)
                or first_time_hour < 0
            ):
                raise InvalidArgument(
                    "first_time_hour argument of modify_schedule needs to be "
                    "an integer greater or equal 0"
                )

            if first_time_day_of_month is None:
                raise RequiredArgument(
                    function=self.modify_schedule.__name__,
                    argument='first_time_day_of_month',
                )
            elif (
                not isinstance(first_time_day_of_month, numbers.Integral)
                or first_time_day_of_month < 1
                or first_time_day_of_month > 31
            ):
                raise InvalidArgument(
                    "first_time_day_of_month argument of modify_schedule needs "
                    "to be an integer between 1 and 31"
                )

            if first_time_month is None:
                raise RequiredArgument(
                    function=self.modify_schedule.__name__,
                    argument='first_time_month',
                )
            elif (
                not isinstance(first_time_month, numbers.Integral)
                or first_time_month < 1
                or first_time_month > 12
            ):
                raise InvalidArgument(
                    "first_time_month argument of modify_schedule needs "
                    "to be an integer between 1 and 12"
                )

            if first_time_year is None:
                raise RequiredArgument(
                    function=self.modify_schedule.__name__,
                    argument='first_time_year',
                )
            elif (
                not isinstance(first_time_year, numbers.Integral)
                or first_time_year < 1970
            ):
                raise InvalidArgument(
                    "first_time_year argument of create_schedule needs "
                    "to be an integer greater or equal 1970"
                )

            _xmlftime = cmd.add_element("first_time")
            _xmlftime.add_element("minute", str(first_time_minute))
            _xmlftime.add_element("hour", str(first_time_hour))
            _xmlftime.add_element("day_of_month", str(first_time_day_of_month))
            _xmlftime.add_element("month", str(first_time_month))
            _xmlftime.add_element("year", str(first_time_year))

        if duration is not None:
            if not duration_unit:
                raise RequiredArgument(
                    function=self.modify_schedule.__name__,
                    argument='duration_unit',
                )

            if not isinstance(duration_unit, TimeUnit):
                raise InvalidArgumentType(
                    function=self.modify_schedule.__name__,
                    argument='duration_unit',
                    arg_type=TimeUnit.__name__,
                )

            if not isinstance(duration, numbers.Integral) or duration < 1:
                raise InvalidArgument(
                    "duration argument must be an integer greater than 0"
                )

            _xmlduration = cmd.add_element("duration", str(duration))
            _xmlduration.add_element("unit", duration_unit.value)

        if period is not None:
            if not period_unit:
                raise RequiredArgument(
                    function=self.modify_schedule.__name__,
                    argument='period_unit',
                )

            if not isinstance(period_unit, TimeUnit):
                raise InvalidArgumentType(
                    function=self.modify_schedule.__name__,
                    argument='period_unit',
                    arg_type=TimeUnit.__name__,
                )

            if not isinstance(period, numbers.Integral) or period < 1:
                raise InvalidArgument(
                    "period argument must be an integer greater than 0"
                )

            _xmlperiod = cmd.add_element("period", str(period))
            _xmlperiod.add_element("unit", period_unit.value)

        if timezone:
            cmd.add_element("timezone", timezone)

        return self._send_xml_command(cmd)

    def modify_setting(
        self,
        setting_id: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ) -> Any:
        """Modifies an existing setting.

        Arguments:
            setting_id: UUID of the setting to be changed.
            name: The name of the setting. Either setting_id or name must be
                passed.
            value: The value of the setting.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not setting_id and not name:
            raise RequiredArgument(
                function=self.modify_setting.__name__,
                argument='setting_id or name argument',
            )

        if value is None:
            raise RequiredArgument(
                function=self.modify_setting.__name__, argument='value argument'
            )

        cmd = XmlCommand("modify_setting")

        if setting_id:
            cmd.set_attribute("setting_id", setting_id)
        else:
            cmd.add_element("name", name)

        cmd.add_element("value", _to_base64(value))

        return self._send_xml_command(cmd)

    def modify_tag(
        self,
        tag_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
        active: Optional[bool] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[EntityType] = None
    ) -> Any:
        """Modifies an existing tag.

        Arguments:
            tag_id: UUID of the tag.
            comment: Comment to add to the tag.
            name: Name of the tag.
            value: Value of the tag.
            active: Whether the tag is active.
            resource_id: ID of the resource to which to attach the tag.
                Required if resource_type is set.
            resource_type: Type of the resource to which to attach the tag.
                Required if resource_id is set.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tag_id:
            raise RequiredArgument(
                function=self.modify_tag.__name__, argument='tag_id'
            )

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

        if resource_id or resource_type:
            if not resource_id:
                raise RequiredArgument(
                    function=self.modify_tag.__name__, argument='resource_id'
                )

            if not resource_type:
                raise RequiredArgument(
                    function=self.modify_tag.__name__, argument='resource_type'
                )

            if not isinstance(resource_type, self.types.EntityType):
                raise InvalidArgumentType(
                    function=self.modify_tag.__name__,
                    argument='resource_type',
                    arg_type=self.types.EntityType.__name__,
                )

            _xmlresource = cmd.add_element(
                "resource", attrs={"id": resource_id}
            )
            _xmlresource.add_element("type", resource_type.value)

        return self._send_xml_command(cmd)

    def modify_target(
        self,
        target_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        hosts: Optional[List[str]] = None,
        exclude_hosts: Optional[List[str]] = None,
        ssh_credential_id: Optional[str] = None,
        ssh_credential_port: Optional[bool] = None,
        smb_credential_id: Optional[str] = None,
        esxi_credential_id: Optional[str] = None,
        snmp_credential_id: Optional[str] = None,
        alive_test: Optional[AliveTest] = None,
        reverse_lookup_only: Optional[bool] = None,
        reverse_lookup_unify: Optional[bool] = None,
        port_list_id: Optional[str] = None
    ) -> Any:
        """Modifies an existing target.

        Arguments:
            target_id: ID of target to modify.
            comment: Comment on target.
            name: Name of target.
            hosts: List of target hosts.
            exclude_hosts: A list of hosts to exclude.
            ssh_credential_id: UUID of SSH credential to use on target.
            ssh_credential_port: The port to use for ssh credential
            smb_credential_id: UUID of SMB credential to use on target.
            esxi_credential_id: UUID of ESXi credential to use on target.
            snmp_credential_id: UUID of SNMP credential to use on target.
            port_list_id: UUID of port list describing ports to scan.
            alive_test: Which alive tests to use.
            reverse_lookup_only: Whether to scan only hosts that have names.
            reverse_lookup_unify: Whether to scan only one IP when multiple IPs
                have the same name.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not target_id:
            raise RequiredArgument(
                function=self.modify_target.__name__, argument='target_id'
            )

        cmd = XmlCommand("modify_target")
        cmd.set_attribute("target_id", target_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if hosts:
            cmd.add_element("hosts", _to_comma_list(hosts))
            if exclude_hosts is None:
                exclude_hosts = ['']

        if exclude_hosts:
            cmd.add_element("exclude_hosts", _to_comma_list(exclude_hosts))

        if alive_test:
            if not isinstance(alive_test, AliveTest):
                raise InvalidArgumentType(
                    function=self.modify_target.__name__,
                    argument='alive_test',
                    arg_type=AliveTest.__name__,
                )
            cmd.add_element("alive_tests", alive_test.value)

        if ssh_credential_id:
            _xmlssh = cmd.add_element(
                "ssh_credential", attrs={"id": ssh_credential_id}
            )

            if ssh_credential_port:
                _xmlssh.add_element("port", str(ssh_credential_port))

        if smb_credential_id:
            cmd.add_element("smb_credential", attrs={"id": smb_credential_id})

        if esxi_credential_id:
            cmd.add_element("esxi_credential", attrs={"id": esxi_credential_id})

        if snmp_credential_id:
            cmd.add_element("snmp_credential", attrs={"id": snmp_credential_id})

        if reverse_lookup_only is not None:
            cmd.add_element(
                "reverse_lookup_only", _to_bool(reverse_lookup_only)
            )

        if reverse_lookup_unify is not None:
            cmd.add_element(
                "reverse_lookup_unify", _to_bool(reverse_lookup_unify)
            )

        if port_list_id:
            cmd.add_element("port_list", attrs={"id": port_list_id})

        return self._send_xml_command(cmd)

    def modify_task(
        self,
        task_id: str,
        *,
        name: Optional[str] = None,
        config_id: Optional[str] = None,
        target_id: Optional[str] = None,
        scanner_id: Optional[str] = None,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        comment: Optional[str] = None,
        alert_ids: Optional[List[str]] = None,
        observers: Optional[List[str]] = None,
        preferences: Optional[dict] = None
    ) -> Any:
        """Modifies an existing task.

        Arguments:
            task_id: UUID of task to modify.
            name: The name of the task.
            config_id: UUID of scan config to use by the task
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: The comment on the task.
            alert_ids: List of UUIDs for alerts to be applied to the task
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the task should be run.
            schedule_periods: A limit to the number of times the task will be
                scheduled, or 0 for no limit.
            observers: List of names or ids of users which should be allowed to
                observe this task
            preferences: Name/Value pairs of scanner preferences.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.modify_task.__name__, argument='task_id argument'
            )

        cmd = XmlCommand("modify_task")
        cmd.set_attribute("task_id", task_id)

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if config_id:
            cmd.add_element("config", attrs={"id": config_id})

        if target_id:
            cmd.add_element("target", attrs={"id": target_id})

        if alterable is not None:
            cmd.add_element("alterable", _to_bool(alterable))

        if hosts_ordering:
            if not isinstance(hosts_ordering, HostsOrdering):
                raise InvalidArgumentType(
                    function=self.modify_task.__name__,
                    argument='hosts_ordering',
                    arg_type=HostsOrdering.__name__,
                )
            cmd.add_element("hosts_ordering", hosts_ordering.value)

        if scanner_id:
            cmd.add_element("scanner", attrs={"id": scanner_id})

        if schedule_id:
            cmd.add_element("schedule", attrs={"id": schedule_id})

        if schedule_periods is not None:
            if (
                not isinstance(schedule_periods, numbers.Integral)
                or schedule_periods < 0
            ):
                raise InvalidArgument(
                    "schedule_periods must be an integer greater or equal "
                    "than 0"
                )
            cmd.add_element("schedule_periods", str(schedule_periods))

        if alert_ids is not None:
            if not _is_list_like(alert_ids):
                raise InvalidArgumentType(
                    function=self.modify_task.__name__,
                    argument='alert_ids',
                    arg_type='list',
                )

            for alert in alert_ids:
                cmd.add_element("alert", attrs={"id": str(alert)})

        if observers is not None:
            if not _is_list_like(observers):
                raise InvalidArgumentType(
                    function=self.modify_task.__name__,
                    argument='observers',
                    arg_type='list',
                )

            cmd.add_element("observers", _to_comma_list(observers))

        if preferences is not None:
            if not isinstance(preferences, collections.abc.Mapping):
                raise InvalidArgumentType(
                    function=self.modify_task.__name__,
                    argument='preferences',
                    arg_type=collections.abc.Mapping.__name__,
                )

            _xmlprefs = cmd.add_element("preferences")
            for pref_name, pref_value in preferences.items():
                _xmlpref = _xmlprefs.add_element("preference")
                _xmlpref.add_element("scanner_name", pref_name)
                _xmlpref.add_element("value", str(pref_value))

        return self._send_xml_command(cmd)

    def modify_user(
        self,
        user_id: str = None,
        name: str = None,
        *,
        new_name: Optional[str] = None,
        password: Optional[str] = None,
        role_ids: Optional[List[str]] = None,
        hosts: Optional[List[str]] = None,
        hosts_allow: Optional[bool] = False,
        ifaces: Optional[List[str]] = None,
        ifaces_allow: Optional[bool] = False
    ) -> Any:
        """Modifies an existing user.

        Arguments:
            user_id: UUID of the user to be modified. Overrides name element
                argument.
            name: The name of the user to be modified. Either user_id or name
                must be passed.
            new_name: The new name for the user.
            password: The password for the user.
            roles_id: List of roles UUIDs for the user.
            hosts: User access rules: List of hosts.
            hosts_allow: If True, allow only listed, otherwise forbid listed.
            ifaces: User access rules: List of ifaces.
            ifaces_allow: If True, allow only listed, otherwise forbid listed.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not user_id and not name:
            raise RequiredArgument(
                function=self.modify_user.__name__, argument='user_id or name'
            )

        cmd = XmlCommand("modify_user")

        if user_id:
            cmd.set_attribute("user_id", user_id)
        else:
            cmd.add_element("name", name)

        if new_name:
            cmd.add_element("new_name", new_name)

        if password:
            cmd.add_element("password", password)

        if role_ids:
            for role in role_ids:
                cmd.add_element("role", attrs={"id": role})

        if hosts:
            cmd.add_element(
                "hosts",
                _to_comma_list(hosts),
                attrs={"allow": _to_bool(hosts_allow)},
            )

        if ifaces:
            cmd.add_element(
                "ifaces",
                _to_comma_list(ifaces),
                attrs={"allow": _to_bool(ifaces_allow)},
            )

        return self._send_xml_command(cmd)

    def move_task(self, task_id: str, *, slave_id: Optional[str] = None) -> Any:
        """Move an existing task to another GMP slave scanner or the master

        Arguments:
            task_id: UUID of the task to be moved
            slave_id: UUID of slave to reassign the task to, empty for master.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.move_task.__name__, argument='task_id'
            )

        cmd = XmlCommand("move_task")
        cmd.set_attribute("task_id", task_id)

        if slave_id is not None:
            cmd.set_attribute("slave_id", slave_id)

        return self._send_xml_command(cmd)

    def restore(self, entity_id: str) -> Any:
        """Restore an entity from the trashcan

        Arguments:
            entity_id: ID of the entity to be restored from the trashcan

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not entity_id:
            raise RequiredArgument(
                function=self.restore.__name__, argument='entity_id'
            )

        cmd = XmlCommand("restore")
        cmd.set_attribute("id", entity_id)

        return self._send_xml_command(cmd)

    def resume_task(self, task_id: str) -> Any:
        """Resume an existing stopped task

        Arguments:
            task_id: UUID of the task to be resumed

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.resume_task.__name__, argument='task_id'
            )

        cmd = XmlCommand("resume_task")
        cmd.set_attribute("task_id", task_id)

        return self._send_xml_command(cmd)

    def start_task(self, task_id: str) -> Any:
        """Start an existing task

        Arguments:
            task_id: UUID of the task to be started

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.start_task.__name__, argument='task_id'
            )

        cmd = XmlCommand("start_task")
        cmd.set_attribute("task_id", task_id)

        return self._send_xml_command(cmd)

    def stop_task(self, task_id: str) -> Any:
        """Stop an existing running task

        Arguments:
            task_id: UUID of the task to be stopped

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.stop_task.__name__, argument='task_id'
            )

        cmd = XmlCommand("stop_task")
        cmd.set_attribute("task_id", task_id)

        return self._send_xml_command(cmd)

    def sync_cert(self) -> Any:
        """Request a synchronization with the CERT feed service

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_cert"))

    def sync_config(self) -> Any:
        """Request an OSP config synchronization with scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_config"))

    def sync_feed(self) -> Any:
        """Request a synchronization with the NVT feed service

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_feed"))

    def sync_scap(self) -> Any:
        """Request a synchronization with the SCAP feed service

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_scap"))

    def test_alert(self, alert_id: str) -> Any:
        """Run an alert

        Invoke a test run of an alert

        Arguments:
            alert_id: UUID of the alert to be tested

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not alert_id:
            raise InvalidArgument("test_alert requires an alert_id argument")

        cmd = XmlCommand("test_alert")
        cmd.set_attribute("alert_id", alert_id)

        return self._send_xml_command(cmd)

    def trigger_alert(
        self,
        alert_id: str,
        report_id: str,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        report_format_id: Optional[str] = None,
        delta_report_id: Optional[str] = None
    ) -> Any:
        """Run an alert by ignoring its event and conditions

        The alert is triggered to run immediately with the provided filtered
        report by ignoring the even and condition settings.

        Arguments:
            alert_id: UUID of the alert to be run
            report_id: UUID of the report to be provided to the alert
            filter: Filter term to use to filter results in the report
            filter_id: UUID of filter to use to filter results in the report
            report_format_id: UUID of report format to use
            delta_report_id: UUID of an existing report to compare report to.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not alert_id:
            raise RequiredArgument(
                function=self.trigger_alert.__name__,
                argument='alert_id argument',
            )

        if not report_id:
            raise RequiredArgument(
                function=self.trigger_alert.__name__,
                argument='report_id argument',
            )

        cmd = XmlCommand("get_reports")
        cmd.set_attribute("report_id", report_id)
        cmd.set_attribute("alert_id", alert_id)

        if filter:
            cmd.set_attribute("filter", filter)

        if filter_id:
            cmd.set_attribute("filt_id", filter_id)

        if report_format_id:
            cmd.set_attribute("format_id", report_format_id)

        if delta_report_id:
            cmd.set_attribute("delta_report_id", delta_report_id)

        return self._send_xml_command(cmd)

    def verify_agent(self, agent_id: str) -> Any:
        """Verify an existing agent

        Verifies the trust level of an existing agent. It will be checked
        whether signature of the agent currently matches the agent. This
        includes the agent installer file. It is *not* verified if the agent
        works as expected by the user.

        Arguments:
            agent_id: UUID of the agent to be verified

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not agent_id:
            raise InvalidArgument("verify_agent requires an agent_id argument")

        cmd = XmlCommand("verify_agent")
        cmd.set_attribute("agent_id", agent_id)

        return self._send_xml_command(cmd)

    def verify_report_format(self, report_format_id: str) -> Any:
        """Verify an existing report format

        Verifies the trust level of an existing report format. It will be
        checked whether the signature of the report format currently matches the
        report format. This includes the script and files used to generate
        reports of this format. It is *not* verified if the report format works
        as expected by the user.

        Arguments:
            report_format_id: UUID of the report format to be verified

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.verify_report_format.__name__,
                argument='report_format_id',
            )

        cmd = XmlCommand("verify_report_format")
        cmd.set_attribute("report_format_id", report_format_id)

        return self._send_xml_command(cmd)

    def verify_scanner(self, scanner_id: str) -> Any:
        """Verify an existing scanner

        Verifies if it is possible to connect to an existing scanner. It is
        *not* verified if the scanner works as expected by the user.

        Arguments:
            scanner_id: UUID of the scanner to be verified

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.verify_scanner.__name__, argument='scanner_id'
            )

        cmd = XmlCommand("verify_scanner")
        cmd.set_attribute("scanner_id", scanner_id)

        return self._send_xml_command(cmd)
