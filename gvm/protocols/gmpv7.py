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

from lxml import etree

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.utils import get_version_string, deprecation
from gvm.xml import XmlCommand, create_parser

from .base import GvmProtocol

logger = logging.getLogger(__name__)

PROTOCOL_VERSION = (7,)

FILTER_TYPES = (
    "agent",
    "alert",
    "asset",
    "config",
    "credential",
    "filter",
    "group",
    "note",
    "override",
    "permission",
    "port_list",
    "report",
    "report_format",
    "result",
    "role",
    "schedule",
    "secinfo",
    "tag",
    "target",
    "task",
    "user",
)

TIME_UNITS = (
    "second",
    "minute",
    "hour",
    "day",
    "week",
    "month",
    "year",
    "decade",
)

ALIVE_TESTS = (
    "Consider Alive",
    "ICMP, TCP-ACK Service & ARP Ping",
    "TCP-ACK Service & ARP Ping",
    "ICMP & ARP Ping",
    "ICMP & TCP-ACK Service Ping",
    "ARP Ping",
    "TCP-ACK Service Ping",
    "TCP-SYN Service Ping",
    "ICMP Ping",
    "Scan Config Default",
)

CREDENTIAL_TYPES = ("cc", "snmp", "up", "usk")

OSP_SCANNER_TYPE = "1"
OPENVAS_SCANNER_TYPE = "2"
CVE_SCANNER_TYPE = "3"
GMP_SCANNER_TYPE = "4"  # formerly slave scanner

SCANNER_TYPES = (
    OSP_SCANNER_TYPE,
    OPENVAS_SCANNER_TYPE,
    CVE_SCANNER_TYPE,
    GMP_SCANNER_TYPE,
)

ALERT_EVENTS = ("Task run status changed",)

ALERT_EVENTS_SECINFO = ("Updated SecInfo arrived", "New SecInfo arrived")

ALERT_CONDITIONS = (
    "Always",
    "Severity at least",
    "Filter count changed",
    "Filter count at least",
)

ALERT_CONDITIONS_SECINFO = ("Always",)

ALERT_METHODS = (
    "SCP",
    "Send",
    "SMB",
    "SNMP",
    "Syslog",
    "Email",
    "Start Task",
    "HTTP Get",
    "Sourcefire Connector",
    "verinice Connector",
)

ALERT_METHODS_SECINFO = ("SCP", "Send", "SMB", "SNMP", "Syslog", "Email")

ASSET_TYPES = ("host", "os")

INFO_TYPES = (
    "CERT_BUND_ADV",
    "CPE",
    "CVE",
    "DFN_CERT_ADV",
    "OVALDEF",
    "NVT",
    "ALLINFO",
)

THREAD_TYPES = ("High", "Medium", "Low", "Alarm", "Log", "Debug")

SUBJECT_TYPES = ("user", "group", "role")

AGGREGATE_RESOURCE_TYPES = (
    "alert",
    "allinfo",
    "cert_bund_adv",
    "cpe",
    "cve",
    "dfn_cert_adv",
    "host",
    "note",
    "nvt",
    "os",
    "ovaldef",
    "override",
    "report",
    "result",
    "task",
    "vuln",
)


def _check_command_status(xml):
    """Check gmp response

    Look into the gmp response and check for the status in the root element

    Arguments:
        xml {string} -- XML-Source

    Returns:
        bool -- True if valid, otherwise False
    """

    if xml is 0 or xml is None:
        logger.error("XML Command is empty")
        return False

    try:
        root = etree.XML(xml, parser=create_parser())
        status = root.attrib["status"]
        return status is not None and status[0] == "2"

    except etree.Error as e:
        logger.error("etree.XML(xml): %s", e)
        return False


def _to_bool(value):
    return "1" if value else "0"


def _to_base64(value):
    return base64.b64encode(value.encode("utf-8"))


def _to_comma_list(value):
    return ",".join(value)


def _add_filter(cmd, filter, filter_id):
    if filter:
        cmd.set_attribute("filter", filter)

    if filter_id:
        cmd.set_attribute("filt_id", filter_id)


def _check_event(event, condition, method):
    if event in ALERT_EVENTS:
        if condition not in ALERT_CONDITIONS:
            raise InvalidArgument("Invalid condition for event")
        if method not in ALERT_METHODS:
            raise InvalidArgument("Invalid method for event")
    elif event in ALERT_EVENTS_SECINFO:
        if condition not in ALERT_CONDITIONS_SECINFO:
            raise InvalidArgument("Invalid condition for event")
        if method not in ALERT_METHODS_SECINFO:
            raise InvalidArgument("Invalid method for event")
    elif event is not None:
        raise InvalidArgument('Invalid event "{0}"'.format(event))


def _is_list_like(value):
    return isinstance(value, (list, tuple))


class Gmp(GvmProtocol):
    """Python interface for Greenbone Management Protocol

    This class implements the `Greenbone Management Protocol version 7`_

    Attributes:
        connection (:class:`gvm.connections.GvmConnection`): Connection to use
            to talk with the gvmd daemon. See :mod:`gvm.connections` for
            possible connection types.
        transform (`callable`_, optional): Optional transform callable to
            convert response data. After each request the callable gets passed
            the plain response data which can be used to check the data and/or
            conversion into different representations like a xml dom.

            See :mod:`gvm.transforms` for existing transforms.

    .. _Greenbone Management Protocol version 7:
        https://docs.greenbone.net/API/GMP/gmp-7.0.html
    .. _callable:
        https://docs.python.org/3/library/functions.html#callable
    """

    def __init__(self, connection, *, transform=None):
        super().__init__(connection, transform=transform)

        # Is authenticated on gvmd
        self._authenticated = False

    @staticmethod
    def get_protocol_version():
        """Determine the Greenbone Management Protocol version.

        Returns:
            str: Implemented version of the Greenbone Management Protocol
        """
        return get_version_string(PROTOCOL_VERSION)

    def is_authenticated(self):
        """Checks if the user is authenticated

        If the user is authenticated privileged GMP commands like get_tasks
        may be send to gvmd.

        Returns:
            bool: True if an authenticated connection to gvmd has been
            established.
        """
        return self._authenticated

    def authenticate(self, username, password):
        """Authenticate to gvmd.

        The generated authenticate command will be send to server.
        Afterwards the response is read, transformed and returned.

        Arguments:
            username (str): Username
            password (str): Password

        Returns:
            any, str by default: Transformed response from server.
        """
        cmd = XmlCommand("authenticate")

        if not username:
            raise RequiredArgument("authenticate requires username")

        if not password:
            raise RequiredArgument("authenticate requires password")

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
        installer,
        signature,
        name,
        *,
        comment=None,
        howto_install=None,
        howto_use=None
    ):
        """Create a new agent

        Arguments:
            installer (str): A base64 encoded file that installs the agent on a
                target machine
            signature: (str): A detached OpenPGP signature of the installer
            name (str): A name for the agent
            comment (str, optional): A comment for the agent
            howto_install (str, optional): A file that describes how to install
                the agent
            howto_use (str, optional): A file that describes how to use the
                agent

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_agent requires name argument")

        if not installer:
            raise RequiredArgument("create_agent requires installer argument")

        if not signature:
            raise RequiredArgument("create_agent requires signature argument")

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

    def clone_agent(self, agent_id):
        """Clone an existing agent

        Arguments:
            agent_id (str): UUID of an existing agent to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not agent_id:
            raise RequiredArgument("clone_agent requires a agent_id argument")

        cmd = XmlCommand("create_agent")
        cmd.add_element("copy", agent_id)
        return self._send_xml_command(cmd)

    def create_alert(
        self,
        name,
        condition,
        event,
        method,
        *,
        method_data=None,
        event_data=None,
        condition_data=None,
        filter_id=None,
        comment=None
    ):
        """Create a new alert

        Arguments:
            name (str): Name of the new Alert
            condition (str): The condition that must be satisfied for the alert
                to occur; if the event is either 'Updated SecInfo arrived' or
                'New SecInfo arrived', condition must be 'Always'. Otherwise,
                condition can also be on of 'Severity at least', 'Filter count
                changed' or 'Filter count at least'.
            event (str): The event that must happen for the alert to occur, one
                of 'Task run status changed', 'Updated SecInfo arrived' or 'New
                SecInfo arrived'
            method (str): The method by which the user is alerted, one of 'SCP',
                'Send', 'SMB', 'SNMP', 'Syslog' or 'Email'; if the event is
                neither 'Updated SecInfo arrived' nor 'New SecInfo arrived',
                method can also be one of 'Start Task', 'HTTP Get', 'Sourcefire
                Connector' or 'verinice Connector'.
            condition_data (dict, optional): Data that defines the condition
            event_data (dict, optional): Data that defines the event
            method_data (dict, optional): Data that defines the method
            filter_id (str, optional): Filter to apply when executing alert
            comment (str, optional): Comment for the alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_alert requires name argument")

        if not condition:
            raise RequiredArgument("create_alert requires condition argument")

        if not event:
            raise RequiredArgument("create_alert requires event argument")

        if not method:
            raise RequiredArgument("create_alert requires method argument")

        _check_event(event, condition, method)

        cmd = XmlCommand("create_alert")
        cmd.add_element("name", name)

        conditions = cmd.add_element("condition", condition)

        if not condition_data is None:
            for key, value in condition_data.items():
                _data = conditions.add_element("data", value)
                _data.add_element("name", key)

        events = cmd.add_element("event", event)

        if not event_data is None:
            for key, value in event_data.items():
                _data = events.add_element("data", value)
                _data.add_element("name", key)

        methods = cmd.add_element("method", method)

        if not method_data is None:
            for key, value in method_data.items():
                _data = methods.add_element("data", value)
                _data.add_element("name", key)

        if filter_id:
            cmd.add_element("filter", attrs={"id": filter_id})

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def clone_alert(self, alert_id):
        """Clone an existing alert

        Arguments:
            alert_id (str): UUID of an existing alert to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not alert_id:
            raise RequiredArgument("clone_alert requires a alert_id argument")

        cmd = XmlCommand("create_alert")
        cmd.add_element("copy", alert_id)
        return self._send_xml_command(cmd)

    def create_config(self, config_id, name):
        """Create a new scan config from an existing one

        Arguments:
            config_id (str): UUID of the existing scan config
            name (str): Name of the new scan config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_config requires name argument")

        if not config_id:
            raise RequiredArgument("create_config requires config_id argument")

        cmd = XmlCommand("create_config")
        cmd.add_element("copy", config_id)
        cmd.add_element("name", name)
        return self._send_xml_command(cmd)

    def clone_config(self, config_id):
        """Clone a scan config from an existing one

        Arguments:
            config_id (str): UUID of the existing scan config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config_id:
            raise RequiredArgument("clone_config requires config_id argument")

        cmd = XmlCommand("create_config")
        cmd.add_element("copy", config_id)
        return self._send_xml_command(cmd)

    def import_config(self, config):
        """Import a scan config from XML

        Arguments:
            config (str): Scan Config XML as string to import. This XML must
                contain a :code:`<get_configs_response>` root element.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config:
            raise RequiredArgument("import_config requires config argument")

        cmd = XmlCommand("create_config")

        try:
            cmd.append_xml_str(config)
        except etree.XMLSyntaxError as e:
            raise InvalidArgument(
                "Invalid xml passed as config to import_config", e
            )

        return self._send_xml_command(cmd)

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
        privacy_password=None
    ):
        """Create a new credential

        Create a new credential e.g. to be used in the method of an alert.

        Currently the following credential types are supported:

            - 'up'   - Username + Password
            - 'usk'  - Username + private SSH-Key
            - 'cc'   - Client Certificates
            - 'snmp' - SNMPv1 or SNMPv2c protocol

        Arguments:
            name (str): Name of the new credential
            credential_type (str): The credential type. One of 'cc', 'snmp',
                'up', 'usk'
            comment (str, optional): Comment for the credential
            allow_insecure (boolean, optional): Whether to allow insecure use of
                the credential
            certificate (str, optional): Certificate for the credential.
                Required for cc credential type.
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
            community (str, optional): The SNMP community.
            auth_algorithm (str, optional): The SNMP authentication algorithm.
                Either 'md5' or 'sha1'. Required for snmp credential type.
            privacy_algorithm (str, optional): The SNMP privacy algorithm,
                either aes or des.
            privacy_password (str, optional): The SNMP privacy password

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

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_credential requires name argument")

        if credential_type not in CREDENTIAL_TYPES:
            raise InvalidArgument(
                "create_credential requires type to be either cc, snmp, up "
                " or usk"
            )

        cmd = XmlCommand("create_credential")
        cmd.add_element("name", name)

        cmd.add_element("type", credential_type)

        if comment:
            cmd.add_element("comment", comment)

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", _to_bool(allow_insecure))

        if credential_type == "cc":
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

        return self._send_xml_command(cmd)

    def clone_credential(self, credential_id):
        """Clone an existing credential

        Arguments:
            credential_id (str): UUID of an existing credential to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                "clone_credential requires a credential_id argument"
            )

        cmd = XmlCommand("create_credential")
        cmd.add_element("copy", credential_id)
        return self._send_xml_command(cmd)

    def create_filter(
        self,
        name,
        *,
        make_unique=False,
        filter_type=None,
        comment=None,
        term=None
    ):
        """Create a new filter

        Arguments:
            name (str): Name of the new filter
            make_unique (boolean, optional):
            filter_type (str, optional): Filter for entity type
            comment (str, optional): Comment for the filter
            term (str, optional): Filter term e.g. 'name=foo'

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_filter requires a name argument")

        cmd = XmlCommand("create_filter")
        _xmlname = cmd.add_element("name", name)
        if make_unique:
            _xmlname.add_element("make_unique", "1")

        if comment:
            cmd.add_element("comment", comment)

        if term:
            cmd.add_element("term", term)

        if filter_type:
            filter_type = filter_type.lower()
            if filter_type not in FILTER_TYPES:
                raise InvalidArgument(
                    "create_filter requires type to be one of {0} but "
                    "was {1}".format(", ".join(FILTER_TYPES), filter_type)
                )
            cmd.add_element("type", filter_type)

        return self._send_xml_command(cmd)

    def clone_filter(self, filter_id):
        """Clone an existing filter

        Arguments:
            filter_id (str): UUID of an existing filter to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not filter_id:
            raise RequiredArgument("clone_filter requires a filter_id argument")

        cmd = XmlCommand("create_filter")
        cmd.add_element("copy", filter_id)
        return self._send_xml_command(cmd)

    def create_group(self, name, *, comment=None, special=False, users=None):
        """Create a new group

        Arguments:
            name (str): Name of the new group
            comment (str, optional): Comment for the group
            special (boolean, optional): Create permission giving members full
                access to each other's entities
            users (list, optional): List of user names to be in the group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_group requires a name argument")

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

    def clone_group(self, group_id):
        """Clone an existing group

        Arguments:
            group_id (str): UUID of an existing group to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_id:
            raise RequiredArgument("clone_group requires a group_id argument")

        cmd = XmlCommand("create_group")
        cmd.add_element("copy", group_id)
        return self._send_xml_command(cmd)

    def create_host(self, name, *, comment=None):
        """Create a new host asset

        Arguments:
            name (str): Name for the new host asset
            comment (str, optional): Comment for the new host asset

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_host requires name argument")

        cmd = XmlCommand("create_asset")
        asset = cmd.add_element("asset")
        asset.add_element("type", "host")  # ignored for gmp7, required for gmp8
        asset.add_element("name", name)

        if comment:
            asset.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def create_note(
        self,
        text,
        nvt_oid,
        *,
        seconds_active=None,
        hosts=None,
        result_id=None,
        severity=None,
        task_id=None,
        threat=None,
        port=None
    ):
        """Create a new note

        Arguments:
            text (str): Text of the new note
            nvt_id (str): OID of the nvt to which note applies
            seconds_active (int, optional): Seconds note will be active. -1 on
                always, 0 off
            hosts (list, optional): A list of hosts addresses
            port (int, optional): Port to which the note applies
            result_id (str, optional): UUID of a result to which note applies
            severity (decimal, optional): Severity to which note applies
            task_id (str, optional): UUID of task to which note applies
            threat (str, optional): Threat level to which note applies. One of
                High, Medium, Low, Alarm, Log or Debug. Will be converted to
                severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not text:
            raise RequiredArgument("create_note requires a text argument")

        if not nvt_oid:
            raise RequiredArgument("create_note requires a nvt_oid argument")

        cmd = XmlCommand("create_note")
        cmd.add_element("text", text)
        cmd.add_element("nvt", attrs={"oid": nvt_oid})

        if not seconds_active is None:
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
            if threat not in THREAD_TYPES:
                raise InvalidArgument(
                    "create_note threat argument {0} is invalid. threat must "
                    "be one of {1}".format(threat, ", ".join(THREAD_TYPES))
                )

            cmd.add_element("threat", threat)

        return self._send_xml_command(cmd)

    def clone_note(self, note_id):
        """Clone an existing note

        Arguments:
            note_id (str): UUID of an existing note to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not note_id:
            raise RequiredArgument("clone_note requires a note_id argument")

        cmd = XmlCommand("create_note")
        cmd.add_element("copy", note_id)
        return self._send_xml_command(cmd)

    def create_override(
        self,
        text,
        nvt_oid,
        *,
        seconds_active=None,
        hosts=None,
        port=None,
        result_id=None,
        severity=None,
        new_severity=None,
        task_id=None,
        threat=None,
        new_threat=None
    ):
        """Create a new override

        Arguments:
            text (str): Text of the new override
            nvt_id (str): OID of the nvt to which override applies
            seconds_active (int, optional): Seconds override will be active.
                -1 on always, 0 off
            hosts (list, optional): A list of host addresses
            port (int, optional): Port to which the override applies
            result_id (str, optional): UUID of a result to which override
                applies
            severity (decimal, optional): Severity to which override applies
            new_severity (decimal, optional): New severity for result
            task_id (str, optional): UUID of task to which override applies
            threat (str, optional): Threat level to which override applies. One
                of High, Medium, Low, Alarm, Log or Debug. Will be converted to
                severity.
            new_threat (str, optional): New threat level for results. One
                of High, Medium, Low, Alarm, Log or Debug. Will be converted to
                new_severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not text:
            raise RequiredArgument("create_override requires a text argument")

        if not nvt_oid:
            raise RequiredArgument(
                "create_override requires a nvt_oid " "argument"
            )

        cmd = XmlCommand("create_override")
        cmd.add_element("text", text)
        cmd.add_element("nvt", attrs={"oid": nvt_oid})

        if not seconds_active is None:
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
            if threat not in THREAD_TYPES:
                raise InvalidArgument(
                    "create_override threat argument {0} is invalid. threat"
                    "must be one of {1}".format(threat, ", ".join(THREAD_TYPES))
                )

            cmd.add_element("threat", threat)

        if new_threat is not None:
            if new_threat not in THREAD_TYPES:
                raise InvalidArgument(
                    "create_override new_threat argument {0} is invalid. "
                    "new_threat must be one of {1}".format(
                        new_threat, ", ".join(THREAD_TYPES)
                    )
                )

            cmd.add_element("new_threat", new_threat)

        return self._send_xml_command(cmd)

    def clone_override(self, override_id):
        """Clone an existing override

        Arguments:
            override_id (str): UUID of an existing override to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not override_id:
            raise RequiredArgument(
                "clone_override requires a override_id argument"
            )

        cmd = XmlCommand("create_override")
        cmd.add_element("copy", override_id)
        return self._send_xml_command(cmd)

    def create_permission(
        self,
        name,
        subject_id,
        subject_type,
        *,
        resource_id=None,
        resource_type=None,
        comment=None
    ):
        """Create a new permission

        Arguments:
            name (str): Name of the new permission
            subject_id (str): UUID of subject to whom the permission is granted
            subject_type (str): Type of the subject user, group or role
            comment (str, optional): Comment for the permission
            resource_id (str, optional): UUID of entity to which the permission
                applies
            resource_type (str, optional): Type of the resource. For Super
                permissions user, group or role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_permission requires a name argument")

        if not subject_id:
            raise RequiredArgument(
                "create_permission requires a subject_id argument"
            )

        if subject_type not in SUBJECT_TYPES:
            raise InvalidArgument(
                "create_permission requires subject_type to be either user, "
                "group or role"
            )

        cmd = XmlCommand("create_permission")
        cmd.add_element("name", name)

        _xmlsubject = cmd.add_element("subject", attrs={"id": subject_id})
        _xmlsubject.add_element("type", subject_type)

        if comment:
            cmd.add_element("comment", comment)

        if resource_id or resource_type:
            if not resource_id:
                raise RequiredArgument(
                    "create_permission requires resource_id for resource_type"
                )

            if not resource_type:
                raise RequiredArgument(
                    "create_permission requires resource_type for resource_id"
                )

            _xmlresource = cmd.add_element(
                "resource", attrs={"id": resource_id}
            )
            _xmlresource.add_element("type", resource_type)

        return self._send_xml_command(cmd)

    def clone_permission(self, permission_id):
        """Clone an existing permission

        Arguments:
            permission_id (str): UUID of an existing permission to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not permission_id:
            raise RequiredArgument(
                "clone_permission requires a permission_id argument"
            )

        cmd = XmlCommand("create_permission")
        cmd.add_element("copy", permission_id)
        return self._send_xml_command(cmd)

    def create_port_list(self, name, port_range, *, comment=None):
        """Create a new port list

        Arguments:
            name (str): Name of the new port list
            port_range (str): Port list ranges e.g. `"T: 1-1234"` for tcp port
                1 - 1234
            comment (str, optional): Comment for the port list

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_port_list requires a name argument")

        if not port_range:
            raise RequiredArgument(
                "create_port_list requires a port_range argument"
            )

        cmd = XmlCommand("create_port_list")
        cmd.add_element("name", name)
        cmd.add_element("port_range", port_range)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def clone_port_list(self, port_list_id):
        """Clone an existing port list

        Arguments:
            port_list_id (str): UUID of an existing port list to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument(
                "clone_port_list requires a port_list_id argument"
            )

        cmd = XmlCommand("create_port_list")
        cmd.add_element("copy", port_list_id)
        return self._send_xml_command(cmd)

    def create_port_range(
        self, port_list_id, start, end, port_range_type, *, comment=None
    ):
        """Create new port range

        Arguments:
            port_list_id (str): UUID of the port list to which to add the range
            start (int): The first port in the range
            end (int): The last port in the range
            port_range_type (str): The type of the ports: TCP, UDP, ...
            comment (str, optional): Comment for the port range

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument(
                "create_port_range requires " "a port_list_id argument"
            )

        if not port_range_type:
            raise RequiredArgument(
                "create_port_range requires a port_range_type argument"
            )

        if not start:
            raise RequiredArgument(
                "create_port_range requires a start argument"
            )

        if not end:
            raise RequiredArgument("create_port_range requires a end argument")

        cmd = XmlCommand("create_port_range")
        cmd.add_element("port_list", attrs={"id": port_list_id})
        cmd.add_element("start", str(start))
        cmd.add_element("end", str(end))
        cmd.add_element("type", port_range_type)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def import_report(
        self,
        report,
        *,
        task_id=None,
        task_name=None,
        task_comment=None,
        in_assets=None
    ):
        """Import a Report from XML

        Arguments:
            report (str): Report XML as string to import. This XML must contain
                a :code:`<report>` root element.
            task_id (str, optional): UUID of task to import report to
            task_name (str, optional): Name of task to be created if task_id is
                not present. Either task_id or task_name must be passed
            task_comment (str, optional): Comment for task to be created if
                task_id is not present
            in_asset (boolean, optional): Whether to create or update assets
                using the report

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report:
            raise RequiredArgument("import_report requires a report argument")

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
                "import_report requires a task_id or task_name argument"
            )

        if not in_assets is None:
            cmd.add_element("in_assets", _to_bool(in_assets))

        try:
            cmd.append_xml_str(report)
        except etree.XMLSyntaxError as e:
            raise InvalidArgument(
                "Invalid xml passed as report to import_report", e
            )

        return self._send_xml_command(cmd)

    def create_role(self, name, *, comment=None, users=None):
        """Create a new role

        Arguments:
            name (str): Name of the role
            comment (str, optional): Comment for the role
            users (list, optional): List of user names to add to the role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        if not name:
            raise RequiredArgument("create_role requires a name argument")

        cmd = XmlCommand("create_role")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if users:
            cmd.add_element("users", _to_comma_list(users))

        return self._send_xml_command(cmd)

    def clone_role(self, role_id):
        """Clone an existing role

        Arguments:
            role_id (str): UUID of an existing role to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not role_id:
            raise RequiredArgument("clone_role requires a role_id argument")

        cmd = XmlCommand("create_role")
        cmd.add_element("copy", role_id)
        return self._send_xml_command(cmd)

    def create_scanner(
        self,
        name,
        host,
        port,
        scanner_type,
        credential_id,
        *,
        ca_pub=None,
        comment=None
    ):
        """Create a new scanner

        Arguments:
            name (str): Name of the scanner
            host (str): The host of the scanner
            port (int): The port of the scanner
            scanner_type (str): Type of the scanner.
                '1' for OSP, '2' for OpenVAS (classic) Scanner.
            credential_id (str): UUID of client certificate credential for the
                scanner
            ca_pub (str, optional): Certificate of CA to verify scanner
                certificate
            comment (str, optional): Comment for the scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_scanner requires a name argument")

        if not host:
            raise RequiredArgument("create_scanner requires a host argument")

        if not port:
            raise RequiredArgument("create_scanner requires a port argument")

        if not scanner_type:
            raise RequiredArgument(
                "create_scanner requires a scanner_type " "argument"
            )

        if not credential_id:
            raise RequiredArgument(
                "create_scanner requires a credential_id " "argument"
            )

        if scanner_type not in SCANNER_TYPES:
            raise InvalidArgument(
                "create_scanner requires a scanner_type "
                'argument which must be either "1" for OSP, '
                '"2" for OpenVAS (Classic), "3" for CVE or '
                '"4" for GMP Scanner.'
            )

        cmd = XmlCommand("create_scanner")
        cmd.add_element("name", name)
        cmd.add_element("host", host)
        cmd.add_element("port", str(port))
        cmd.add_element("type", scanner_type)

        if ca_pub:
            cmd.add_element("ca_pub", ca_pub)

        cmd.add_element("credential", attrs={"id": str(credential_id)})

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def clone_scanner(self, scanner_id):
        """Clone an existing scanner

        Arguments:
            scanner_id (str): UUID of an existing scanner to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                "clone_scanner requires a scanner_id argument"
            )

        cmd = XmlCommand("create_scanner")
        cmd.add_element("copy", scanner_id)
        return self._send_xml_command(cmd)

    def create_schedule(
        self,
        name,
        *,
        comment=None,
        first_time_minute=None,
        first_time_hour=None,
        first_time_day_of_month=None,
        first_time_month=None,
        first_time_year=None,
        duration=None,
        duration_unit=None,
        period=None,
        period_unit=None,
        timezone=None
    ):
        """Create a new schedule

        Arguments:
            name (str): Name of the schedule
            comment (str, optional): Comment for the schedule
            first_time_minute (int, optional): First time minute the schedule
                will run. Must be an integer >= 0.
            first_time_hour (int, optional): First time hour the schedule
                will run. Must be an integer >= 0.
            first_time_day_of_month (int, optional): First time day of month the
                schedule will run. Must be an integer > 0 <= 31.
            first_time_month (int, optional): First time month the schedule
                will run. Must be an integer >= 1 <= 12.
            first_time_year (int, optional): First time year the schedule
                will run. Must be an integer >= 1970.
            duration (int, optional): How long the Manager will run the
                scheduled task for until it gets paused if not finished yet.
                Must be an integer > 0.
            duration_unit (str, optional): Unit of the duration. One of second,
                minute, hour, day, week, month, year, decade. Required if
                duration is set.
            period (int, optional): How often the Manager will repeat the
                scheduled task. Must be an integer > 0.
            period_unit (str, optional): Unit of the period. One of second,
                minute, hour, day, week, month, year, decade. Required if
                period is set.
            timezone (str, optional): The timezone the schedule will follow

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_schedule requires a name argument")

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
                    "Setting first_time requires first_time_minute argument"
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
                    "Setting first_time requires first_time_hour argument"
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
                    "Setting first_time requires first_time_day_of_month "
                    "argument"
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
                    "Setting first_time requires first_time_month argument"
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
                    "Setting first_time requires first_time_year argument"
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
                    "Setting duration requires duration_unit argument"
                )

            if not duration_unit in TIME_UNITS:
                raise InvalidArgument(
                    "duration_unit must be one of {units}. But {actual} has "
                    "been passed".format(
                        units=", ".join(TIME_UNITS), actual=duration_unit
                    )
                )

            if not isinstance(duration, numbers.Integral) or duration < 1:
                raise InvalidArgument(
                    "duration argument must be an integer greater than 0"
                )

            _xmlduration = cmd.add_element("duration", str(duration))
            _xmlduration.add_element("unit", duration_unit)

        if period is not None:
            if not period_unit:
                raise RequiredArgument(
                    "Setting period requires period_unit argument"
                )

            if not period_unit in TIME_UNITS:
                raise InvalidArgument(
                    "period_unit must be one of {units} but {actual} has "
                    "been passed".format(
                        units=", ".join(TIME_UNITS), actual=period_unit
                    )
                )

            if not isinstance(period, numbers.Integral) or period < 0:
                raise InvalidArgument(
                    "period argument must be a positive integer"
                )

            _xmlperiod = cmd.add_element("period", str(period))
            _xmlperiod.add_element("unit", period_unit)

        if timezone:
            cmd.add_element("timezone", timezone)

        return self._send_xml_command(cmd)

    def clone_schedule(self, schedule_id):
        """Clone an existing schedule

        Arguments:
            schedule_id (str): UUID of an existing schedule to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not schedule_id:
            raise RequiredArgument(
                "clone_schedule requires a schedule_id argument"
            )

        cmd = XmlCommand("create_schedule")
        cmd.add_element("copy", schedule_id)
        return self._send_xml_command(cmd)

    def create_tag(
        self,
        name,
        resource_type,
        *,
        resource_id=None,
        value=None,
        comment=None,
        active=None
    ):
        """Create a new tag

        Arguments:
            name (str): Name of the tag. A full tag name consisting of namespace
                and predicate e.g. `foo:bar`.
            resource_id (str, optional): ID of the resource the tag is to be
                attached to.
            resource_type (str): Entity type the tag is to be attached to
            value (str, optional): Value associated with the tag
            comment (str, optional): Comment for the tag
            active (boolean, optional): Whether the tag should be active

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_tag requires name argument")

        if not resource_type:
            raise RequiredArgument("create_tag requires resource_type argument")

        cmd = XmlCommand("create_tag")
        cmd.add_element("name", name)

        if not resource_id:
            resource_id = ''

        _xmlresource = cmd.add_element(
            "resource", attrs={"id": str(resource_id)}
        )
        _xmlresource.add_element("type", resource_type)

        if comment:
            cmd.add_element("comment", comment)

        if value:
            cmd.add_element("value", value)

        if not active is None:
            if active:
                cmd.add_element("active", "1")
            else:
                cmd.add_element("active", "0")

        return self._send_xml_command(cmd)

    def clone_tag(self, tag_id):
        """Clone an existing tag

        Arguments:
            tag_id (str): UUID of an existing tag to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tag_id:
            raise RequiredArgument("clone_tag requires a tag_id argument")

        cmd = XmlCommand("create_tag")
        cmd.add_element("copy", tag_id)
        return self._send_xml_command(cmd)

    def create_target(
        self,
        name,
        *,
        make_unique=None,
        asset_hosts_filter=None,
        hosts=None,
        comment=None,
        exclude_hosts=None,
        ssh_credential_id=None,
        ssh_credential_port=None,
        smb_credential_id=None,
        esxi_credential_id=None,
        snmp_credential_id=None,
        alive_tests=None,
        reverse_lookup_only=None,
        reverse_lookup_unify=None,
        port_range=None,
        port_list_id=None
    ):
        """Create a new target

        Arguments:
            name (str): Name of the target
            make_unique (boolean, optional): Append a unique suffix if the name
                already exists
            asset_hosts_filter (str, optional): Filter to select target host
                from assets hosts
            hosts (list, optional): List of hosts addresses to scan
            exclude_hosts (list, optional): List of hosts addresses to exclude
                from scan
            comment (str, optional): Comment for the target
            ssh_credential_id (str, optional): UUID of a ssh credential to use
                on target
            ssh_credential_port (int, optional): The port to use for ssh
                credential
            smb_credential_id (str, optional): UUID of a smb credential to use
                on target
            snmp_credential_id (str, optional): UUID of a snmp credential to use
                on target
            esxi_credential_id (str, optional): UUID of a esxi credential to use
                on target
            alive_tests (str, optional): Which alive tests to use
            reverse_lookup_only (boolean, optional): Whether to scan only hosts
                that have names
            reverse_lookup_unify (boolean, optional): Whether to scan only one
                IP when multiple IPs have the same name.
            port_range (str, optional): Port range for the target
            port_list_id (str, optional): UUID of the port list to use on target

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_target requires a name argument")

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
                "create_target requires either a hosts or "
                "an asset_hosts_filter argument"
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

        if alive_tests:
            if not alive_tests in ALIVE_TESTS:
                raise InvalidArgument(
                    "alive_tests must be one of {tests} but "
                    "{actual} has been passed".format(
                        tests="|".join(ALIVE_TESTS), actual=alive_tests
                    )
                )

            cmd.add_element("alive_tests", alive_tests)

        if not reverse_lookup_only is None:
            cmd.add_element(
                "reverse_lookup_only", _to_bool(reverse_lookup_only)
            )

        if not reverse_lookup_unify is None:
            cmd.add_element(
                "reverse_lookup_unify", _to_bool(reverse_lookup_unify)
            )

        if port_range:
            cmd.add_element("port_range", port_range)

        if port_list_id:
            cmd.add_element("port_list", attrs={"id": port_list_id})

        return self._send_xml_command(cmd)

    def clone_target(self, target_id):
        """Clone an existing target

        Arguments:
            target_id (str): UUID of an existing target to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not target_id:
            raise RequiredArgument("clone_target requires a target_id argument")

        cmd = XmlCommand("create_target")
        cmd.add_element("copy", target_id)
        return self._send_xml_command(cmd)

    def create_task(
        self,
        name,
        config_id,
        target_id,
        scanner_id,
        *,
        alterable=None,
        hosts_ordering=None,
        schedule_id=None,
        alert_ids=None,
        comment=None,
        schedule_periods=None,
        observers=None,
        preferences=None
    ):
        """Create a new task

        Arguments:
            name (str): Name of the task
            config_id (str): UUID of scan config to use by the task
            target_id (str): UUID of target to be scanned
            scanner_id (str): UUID of scanner to use for scanning the target
            comment (str, optional): Comment for the task
            alterable (boolean, optional): Whether the task should be alterable
            alert_ids (list, optional): List of UUIDs for alerts to be applied
                to the task
            hosts_ordering (str, optional): The order hosts are scanned in
            schedule_id (str, optional): UUID of a schedule when the task should
                be run.
            schedule_periods (int, optional): A limit to the number of times the
                task will be scheduled, or 0 for no limit
            observers (list, optional): List of names or ids of users which
                should be allowed to observe this task
            preferences (dict, optional): Name/Value pairs of scanner
                preferences.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_task requires a name argument")

        if not config_id:
            raise RequiredArgument("create_task requires a config_id argument")

        if not target_id:
            raise RequiredArgument("create_task requires a target_id argument")

        if not scanner_id:
            raise RequiredArgument("create_task requires a scanner_id argument")

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

        if not alterable is None:
            cmd.add_element("alterable", _to_bool(alterable))

        if hosts_ordering:
            # not sure about the possible values for hosts_orderning
            # it seems gvmd does not check the param
            # gsa allows to select 'sequential', 'random' or 'reverse'
            cmd.add_element("hosts_ordering", hosts_ordering)

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
                raise InvalidArgument("obeservers argument must be a list")

            # gvmd splits by comma and space
            # gvmd tries to lookup each value as user name and afterwards as
            # user id. So both user name and user id are possible
            cmd.add_element("observers", _to_comma_list(observers))

        if preferences is not None:
            if not isinstance(preferences, collections.abc.Mapping):
                raise InvalidArgument('preferences argument must be a dict')

            _xmlprefs = cmd.add_element("preferences")
            for pref_name, pref_value in preferences.items():
                _xmlpref = _xmlprefs.add_element("preference")
                _xmlpref.add_element("scanner_name", pref_name)
                _xmlpref.add_element("value", str(pref_value))

        return self._send_xml_command(cmd)

    def create_container_task(self, name, *, comment=None):
        """Create a new container task

        A container task is a "meta" task to import and view reports from other
        systems.

        Arguments:
            name (str): Name of the task
            comment (str, optional): Comment for the task

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_task requires a name argument")

        cmd = XmlCommand("create_task")
        cmd.add_element("name", name)
        cmd.add_element("target", attrs={"id": "0"})

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def clone_task(self, task_id):
        """Clone an existing task

        Arguments:
            task_id (str): UUID of existing task to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument("clone_task requires a task_id argument")

        cmd = XmlCommand("create_task")
        cmd.add_element("copy", task_id)
        return self._send_xml_command(cmd)

    def create_user(
        self,
        name,
        *,
        password=None,
        hosts=None,
        hosts_allow=False,
        ifaces=None,
        ifaces_allow=False,
        role_ids=None
    ):
        """Create a new user

        Arguments:
            name (str): Name of the user
            password (str, optional): Password of the user
            hosts (list, optional): A list of host addresses (IPs, DNS names)
            hosts_allow (boolean, optional): If True allow only access to passed
                hosts otherwise deny access. Default is False for deny hosts.
            ifaces (list, optional): A list of interface names
            ifaces_allow (boolean, optional): If True allow only access to
                passed interfaces otherwise deny access. Default is False for
                deny interfaces.
            role_ids (list, optional): A list of role UUIDs for the user

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("create_user requires a name argument")

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

    def clone_user(self, user_id):
        """Clone an existing user

        Arguments:
            user_id (str): UUID of existing user to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not user_id:
            raise RequiredArgument("clone_user requires a user_id argument")

        cmd = XmlCommand("create_user")
        cmd.add_element("copy", user_id)
        return self._send_xml_command(cmd)

    def delete_agent(self, agent_id, *, ultimate=False):
        """Deletes an existing agent

        Arguments:
            agent_id (str) UUID of the agent to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not agent_id:
            raise RequiredArgument("delete_agent requires an agent_id argument")

        cmd = XmlCommand("delete_agent")
        cmd.set_attribute("agent_id", agent_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_alert(self, alert_id, *, ultimate=False):
        """Deletes an existing alert

        Arguments:
            alert_id (str) UUID of the alert to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not alert_id:
            raise RequiredArgument("delete_alert requires an alert_id argument")

        cmd = XmlCommand("delete_alert")
        cmd.set_attribute("alert_id", alert_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_asset(self, *, asset_id=None, report_id=None):
        """Deletes an existing asset

        Arguments:
            asset_id (str, optional): UUID of the single asset to delete.
            report_id (str,optional): UUID of report from which to get all
                assets to delete.
        """
        if not asset_id and not report_id:
            raise RequiredArgument(
                "delete_asset requires an asset_id or " "a report_id argument"
            )

        cmd = XmlCommand("delete_asset")
        if asset_id:
            cmd.set_attribute("asset_id", asset_id)
        else:
            cmd.set_attribute("report_id", report_id)

        return self._send_xml_command(cmd)

    def delete_config(self, config_id, *, ultimate=False):
        """Deletes an existing config

        Arguments:
            config_id (str) UUID of the config to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not config_id:
            raise RequiredArgument(
                "delete_config requires a " "config_id argument"
            )

        cmd = XmlCommand("delete_config")
        cmd.set_attribute("config_id", config_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_credential(self, credential_id, *, ultimate=False):
        """Deletes an existing credential

        Arguments:
            credential_id (str) UUID of the credential to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not credential_id:
            raise RequiredArgument(
                "delete_credential requires a " "credential_id argument"
            )

        cmd = XmlCommand("delete_credential")
        cmd.set_attribute("credential_id", credential_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_filter(self, filter_id, *, ultimate=False):
        """Deletes an existing filter

        Arguments:
            filter_id (str) UUID of the filter to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not filter_id:
            raise RequiredArgument(
                "delete_filter requires a " "filter_id argument"
            )

        cmd = XmlCommand("delete_filter")
        cmd.set_attribute("filter_id", filter_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_group(self, group_id, *, ultimate=False):
        """Deletes an existing group

        Arguments:
            group_id (str) UUID of the group to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not group_id:
            raise RequiredArgument(
                "delete_group requires a " "group_id argument"
            )

        cmd = XmlCommand("delete_group")
        cmd.set_attribute("group_id", group_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_note(self, note_id, *, ultimate=False):
        """Deletes an existing note

        Arguments:
            note_id (str) UUID of the note to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not note_id:
            raise RequiredArgument("delete_note requires a " "note_id argument")

        cmd = XmlCommand("delete_note")
        cmd.set_attribute("note_id", note_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_override(self, override_id, *, ultimate=False):
        """Deletes an existing override

        Arguments:
            override_id (str) UUID of the override to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not override_id:
            raise RequiredArgument(
                "delete_override requires a " "override_id argument"
            )

        cmd = XmlCommand("delete_override")
        cmd.set_attribute("override_id", override_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_permission(self, permission_id, *, ultimate=False):
        """Deletes an existing permission

        Arguments:
            permission_id (str) UUID of the permission to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not permission_id:
            raise RequiredArgument(
                "delete_permission requires a " "permission_id argument"
            )

        cmd = XmlCommand("delete_permission")
        cmd.set_attribute("permission_id", permission_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_port_list(self, port_list_id, *, ultimate=False):
        """Deletes an existing port list

        Arguments:
            port_list_id (str) UUID of the port list to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not port_list_id:
            raise RequiredArgument(
                "delete_port_list requires a " "port_list_id argument"
            )

        cmd = XmlCommand("delete_port_list")
        cmd.set_attribute("port_list_id", port_list_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_port_range(self, port_range_id):
        """Deletes an existing port range

        Arguments:
            port_range_id (str) UUID of the port range to be deleted.
        """
        if not port_range_id:
            raise RequiredArgument(
                "delete_port_range requires a " "port_range_id argument"
            )

        cmd = XmlCommand("delete_port_range")
        cmd.set_attribute("port_range_id", port_range_id)

        return self._send_xml_command(cmd)

    def delete_report(self, report_id):
        """Deletes an existing report

        Arguments:
            report_id (str) UUID of the report to be deleted.
        """
        if not report_id:
            raise RequiredArgument(
                "delete_report requires a " "report_id argument"
            )

        cmd = XmlCommand("delete_report")
        cmd.set_attribute("report_id", report_id)

        return self._send_xml_command(cmd)

    def delete_report_format(self, report_format_id, *, ultimate=False):
        """Deletes an existing report format

        Arguments:
            report_format_id (str) UUID of the report format to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not report_format_id:
            raise RequiredArgument(
                "delete_report_format requires a " "report_format_id argument"
            )

        cmd = XmlCommand("delete_report_format")
        cmd.set_attribute("report_format_id", report_format_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_role(self, role_id, *, ultimate=False):
        """Deletes an existing role

        Arguments:
            role_id (str) UUID of the role to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not role_id:
            raise RequiredArgument("delete_role requires a " "role_id argument")

        cmd = XmlCommand("delete_role")
        cmd.set_attribute("role_id", role_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_scanner(self, scanner_id, *, ultimate=False):
        """Deletes an existing scanner

        Arguments:
            scanner_id (str) UUID of the scanner to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not scanner_id:
            raise RequiredArgument(
                "delete_scanner requires a " "scanner_id argument"
            )

        cmd = XmlCommand("delete_scanner")
        cmd.set_attribute("scanner_id", scanner_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_schedule(self, schedule_id, *, ultimate=False):
        """Deletes an existing schedule

        Arguments:
            schedule_id (str) UUID of the schedule to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not schedule_id:
            raise RequiredArgument(
                "delete_schedule requires a " "schedule_id argument"
            )

        cmd = XmlCommand("delete_schedule")
        cmd.set_attribute("schedule_id", schedule_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_tag(self, tag_id, *, ultimate=False):
        """Deletes an existing tag

        Arguments:
            tag_id (str) UUID of the tag to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not tag_id:
            raise RequiredArgument("delete_tag requires a " "tag_id argument")

        cmd = XmlCommand("delete_tag")
        cmd.set_attribute("tag_id", tag_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_target(self, target_id, *, ultimate=False):
        """Deletes an existing target

        Arguments:
            target_id (str) UUID of the target to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not target_id:
            raise RequiredArgument(
                "delete_target requires a " "target_id argument"
            )

        cmd = XmlCommand("delete_target")
        cmd.set_attribute("target_id", target_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_task(self, task_id, *, ultimate=False):
        """Deletes an existing task

        Arguments:
            task_id (str) UUID of the task to be deleted.
            ultimate (boolean, optional): Whether to remove entirely,
                or to the trashcan.
        """
        if not task_id:
            raise RequiredArgument("delete_task requires a " "task_id argument")

        cmd = XmlCommand("delete_task")
        cmd.set_attribute("task_id", task_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_user(
        self, user_id=None, *, name=None, inheritor_id=None, inheritor_name=None
    ):
        """Deletes an existing user

        Either user_id or name must be passed.

        Arguments:
            user_id (str, optional): UUID of the task to be deleted.
            name (str, optional): The name of the user to be deleted.
            inheritor_id (str, optional): The ID of the inheriting user
                or "self". Overrides inheritor_name.
            inheritor_name (str, optional): The name of the inheriting user.

        """
        if not user_id and not name:
            raise RequiredArgument(
                "delete_user requires a user_id or name argument"
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

    def describe_auth(self):
        """Describe authentication methods

        Returns a list of all used authentication methods if such a list is
        available.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("describe_auth"))

    def empty_trashcan(self):
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
        filter=None,
        filter_id=None,
        trash=None,
        details=None,
        format=None
    ):
        """Request a list of agents

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): True to request the agents in the
                trashcan
            details (boolean, optional): Whether to include agents package
                information when no format was provided
            format (str, optional): One of "installer", "howto_install" or
                "howto_use"

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_agents")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        if not details is None:
            cmd.set_attribute("details", _to_bool(details))

        if format:
            if not format in ("installer", "howto_install", "howto_use"):
                raise InvalidArgument(
                    "installer argument needs to be one of installer, "
                    "howto_install or howto_use"
                )

            cmd.set_attribute("format", format)

        return self._send_xml_command(cmd)

    def get_agent(self, agent_id):
        """Request a single agent

        Arguments:
            agent_id (str): UUID of an existing agent

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not agent_id:
            raise RequiredArgument("get_agent requires an agent_id argument")

        cmd = XmlCommand("get_agents")
        cmd.set_attribute("agent_id", agent_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_aggregates(self, resource_type, **kwargs):
        """Request aggregated information on a resource type

        Additional arguments can be set via the kwargs parameter, but are not
        yet validated.

        Arguments:
           resource_type (str): The GMP resource type to gather data from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not resource_type:
            raise RequiredArgument(
                "get_aggregates requires resource_type argument"
            )

        if resource_type not in AGGREGATE_RESOURCE_TYPES:
            raise InvalidArgument(
                "get_aggregates requires a valid resource_type argument"
            )

        cmd = XmlCommand("get_aggregates")

        cmd.set_attribute("type", resource_type)

        cmd.set_attributes(kwargs)
        return self._send_xml_command(cmd)

    def get_alerts(
        self, *, filter=None, filter_id=None, trash=None, tasks=None
    ):
        """Request a list of alerts

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): True to request the alerts in the
                trashcan
            tasks (boolean, optional): Whether to include the tasks using the
                alerts
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_alerts")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        if not tasks is None:
            cmd.set_attribute("tasks", _to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_alert(self, alert_id):
        """Request a single alert

        Arguments:
            alert_id (str): UUID of an existing alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not alert_id:
            raise RequiredArgument("get_alert requires an alert_id argument")

        cmd = XmlCommand("get_alerts")
        cmd.set_attribute("alert_id", alert_id)
        return self._send_xml_command(cmd)

    def get_assets(self, asset_type, *, filter=None, filter_id=None):
        """Request a list of assets

        Arguments:
            asset_type (str): Either 'os' or 'host'
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not asset_type in ASSET_TYPES:
            raise InvalidArgument("asset_type must be either os or host")

        cmd = XmlCommand("get_assets")

        cmd.set_attribute("type", asset_type)

        _add_filter(cmd, filter, filter_id)

        return self._send_xml_command(cmd)

    def get_asset(self, asset_id, asset_type):
        """Request a single asset

        Arguments:
            asset_type (str): Either 'os' or 'host'
            asset_id (str): UUID of an existing asset

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not asset_type in ASSET_TYPES:
            raise InvalidArgument("asset_type must be either os or host")

        if not asset_id:
            raise RequiredArgument("get_asset requires an asset_type argument")

        cmd = XmlCommand("get_assets")
        cmd.set_attribute("asset_id", asset_id)
        cmd.set_attribute("type", asset_type)

        return self._send_xml_command(cmd)

    def get_credentials(
        self,
        *,
        filter=None,
        filter_id=None,
        scanners=None,
        trash=None,
        targets=None
    ):
        """Request a list of credentials

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            scanners (boolean, optional): Whether to include a list of scanners
                using the credentials
            trash (boolean, optional): Whether to get the trashcan credentials
                instead
            targets (boolean, optional): Whether to include a list of targets
                using the credentials

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_credentials")

        _add_filter(cmd, filter, filter_id)

        if not scanners is None:
            cmd.set_attribute("scanners", _to_bool(scanners))

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        if not targets is None:
            cmd.set_attribute("targets", _to_bool(targets))

        return self._send_xml_command(cmd)

    def get_credential(self, credential_id, *, credential_format=None):
        """Request a single credential

        Arguments:
            credential_id (str): UUID of an existing credential
            credential_format (str, optional): One of "key", "rpm", "deb",
                "exe" or "pem"

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                "get_credential requires credential_id argument"
            )

        cmd = XmlCommand("get_credentials")
        cmd.set_attribute("credential_id", credential_id)
        if credential_format:
            if not credential_format in ("key", "rpm", "deb", "exe", "pem"):
                raise InvalidArgument(
                    "credential_format argument needs to be one of "
                    "key, rpm, deb, exe or pem"
                )

            cmd.set_attribute("format", credential_format)
        return self._send_xml_command(cmd)

    def get_configs(
        self,
        *,
        filter=None,
        filter_id=None,
        trash=None,
        details=None,
        families=None,
        preferences=None,
        tasks=None
    ):
        """Request a list of scan configs

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): Whether to get the trashcan scan configs
                instead
            details (boolean, optional): Whether to get config families,
                preferences, nvt selectors and tasks.
            families (boolean, optional): Whether to include the families if no
                details are requested
            preferences (boolean, optional): Whether to include the preferences
                if no details are requested
            tasks (boolean, optional): Whether to get tasks using this config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_configs")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        if not details is None:
            cmd.set_attribute("details", _to_bool(details))

        if not families is None:
            cmd.set_attribute("families", _to_bool(families))

        if not preferences is None:
            cmd.set_attribute("preferences", _to_bool(preferences))

        if not tasks is None:
            cmd.set_attribute("tasks", _to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_config(self, config_id):
        """Request a single scan config

        Arguments:
            config_id (str): UUID of an existing scan config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config_id:
            raise RequiredArgument("get_config requires config_id argument")

        cmd = XmlCommand("get_configs")
        cmd.set_attribute("config_id", config_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_feeds(self):
        """Request the list of feeds

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("get_feeds"))

    def get_feed(self, feed_type):
        """Request a single feed

        Arguments:
            feed_type (str): Type of single feed to get: NVT, CERT or SCAP

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not feed_type:
            raise RequiredArgument("get_feed requires a feed_type argument")

        feed_type = feed_type.upper()

        if not feed_type in ("NVT", "CERT", "SCAP"):
            raise InvalidArgument(
                "get_feed type arguments must be one of NVT, CERT or SCAP"
            )

        cmd = XmlCommand("get_feeds")
        cmd.set_attribute("type", feed_type)

        return self._send_xml_command(cmd)

    def get_filters(
        self, *, filter=None, filter_id=None, trash=None, alerts=None
    ):
        """Request a list of filters

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): Whether to get the trashcan filters
                instead
            alerts (boolean, optional): Whether to include list of alerts that
                use the filter.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_filters")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        if not alerts is None:
            cmd.set_attribute("alerts", _to_bool(alerts))

        return self._send_xml_command(cmd)

    def get_filter(self, filter_id):
        """Request a single filter

        Arguments:
            filter_id (str): UUID of an existing filter

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not filter_id:
            raise RequiredArgument("get_filter requires a filter_id argument")

        cmd = XmlCommand("get_filters")
        cmd.set_attribute("filter_id", filter_id)
        return self._send_xml_command(cmd)

    def get_groups(self, *, filter=None, filter_id=None, trash=None):
        """Request a list of groups

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): Whether to get the trashcan groups
                instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_groups")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        return self._send_xml_command(cmd)

    def get_group(self, group_id):
        """Request a single group

        Arguments:
            group_id (str): UUID of an existing group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_id:
            raise RequiredArgument("get_group requires a group_id argument")

        cmd = XmlCommand("get_groups")
        cmd.set_attribute("group_id", group_id)
        return self._send_xml_command(cmd)

    def get_info_list(
        self, info_type, *, filter=None, filter_id=None, name=None, details=None
    ):
        """Request a list of security information

        Arguments:
            info_type (str): Type must be either CERT_BUND_ADV, CPE, CVE,
                DFN_CERT_ADV, OVALDEF, NVT or ALLINFO
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            name (str, optional): Name or identifier of the requested
                information
            details (boolean, optional): Whether to include information about
                references to this information

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not info_type:
            raise RequiredArgument(
                "get_info_list requires an info_type argument"
            )

        info_type = info_type.upper()

        if not info_type in INFO_TYPES:
            raise InvalidArgument(
                "get_info_list info_type argument must be one of CERT_BUND_ADV"
                ", CPE, CVE, DFN_CERT_ADV, OVALDEF, NVT or ALLINFO"
            )

        cmd = XmlCommand("get_info")

        cmd.set_attribute("type", info_type)

        _add_filter(cmd, filter, filter_id)

        if name:
            cmd.set_attribute("name", name)

        if not details is None:
            cmd.set_attribute("details", _to_bool(details))

        return self._send_xml_command(cmd)

    def get_info(self, info_id, info_type):
        """Request a single secinfo

        Arguments:
            info_id (str): UUID of an existing secinfo
            info_type (str): Type must be either CERT_BUND_ADV, CPE, CVE,
                DFN_CERT_ADV, OVALDEF, NVT or ALLINFO

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not info_type:
            raise RequiredArgument("get_info requires an info_type argument")

        info_type = info_type.upper()

        if not info_type in INFO_TYPES:
            raise InvalidArgument(
                "get_info info_type argument must be one of CERT_BUND_ADV"
                ", CPE, CVE, DFN_CERT_ADV, OVALDEF, NVT or ALLINFO"
            )

        if not info_id:
            raise RequiredArgument("get_info requires an info_id argument")

        cmd = XmlCommand("get_info")
        cmd.set_attribute("info_id", info_id)

        cmd.set_attribute("type", info_type)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_notes(
        self, *, filter=None, filter_id=None, details=None, result=None
    ):
        """Request a list of notes

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            details (boolean, optional): Add info about connected results and
                tasks
            result (boolean, optional): Return the details of possible connected
                results.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_notes")

        _add_filter(cmd, filter, filter_id)

        if not details is None:
            cmd.set_attribute("details", _to_bool(details))

        if not result is None:
            cmd.set_attribute("result", _to_bool(result))

        return self._send_xml_command(cmd)

    def get_note(self, note_id):
        """Request a single note

        Arguments:
            note_id (str): UUID of an existing note

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not note_id:
            raise RequiredArgument("get_note requires a note_id argument")

        cmd = XmlCommand("get_notes")
        cmd.set_attribute("note_id", note_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_nvts(
        self,
        *,
        details=None,
        preferences=None,
        preference_count=None,
        timeout=None,
        config_id=None,
        preferences_config_id=None,
        family=None,
        sort_order=None,
        sort_field=None
    ):
        """Request a list of nvts

        Arguments:
            details (boolean, optional): Whether to include full details
            preferences (boolean, optional): Whether to include nvt preferences
            preference_count (boolean, optional): Whether to include preference
                count
            timeout (boolean, optional):  Whether to include the special timeout
                preference
            config_id (str, optional): UUID of scan config to which to limit the
                NVT listing
            preferences_config_id (str, optional): UUID of scan config to use
                for preference values
            family (str, optional): Family to which to limit NVT listing
            sort_order (str, optional): Sort order
            sort_field (str, optional): Sort field

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_nvts")

        if not details is None:
            cmd.set_attribute("details", _to_bool(details))

        if not preferences is None:
            cmd.set_attribute("preferences", _to_bool(preferences))

        if not preference_count is None:
            cmd.set_attribute("preference_count", _to_bool(preference_count))

        if not timeout is None:
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

    def get_nvt(self, nvt_oid):
        """Request a single nvt

        Arguments:
            nvt_oid (str): OID of an existing nvt

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not nvt_oid:
            raise RequiredArgument("get_nvt requires nvt_oid argument")

        cmd = XmlCommand("get_nvts")
        cmd.set_attribute("nvt_oid", nvt_oid)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_nvt_families(self, *, sort_order=None):
        """Request a list of nvt families

        Arguments:
            sort_order (str, optional): Sort order

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_nvt_families")

        if sort_order:
            cmd.set_attribute("sort_order", sort_order)

        return self._send_xml_command(cmd)

    def get_overrides(
        self, *, filter=None, filter_id=None, details=None, result=None
    ):
        """Request a list of overrides

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            details (boolean, optional):
            result (boolean, optional):

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_overrides")

        _add_filter(cmd, filter, filter_id)

        if not details is None:
            cmd.set_attribute("details", _to_bool(details))

        if not result is None:
            cmd.set_attribute("result", _to_bool(result))

        return self._send_xml_command(cmd)

    def get_override(self, override_id):
        """Request a single override

        Arguments:
            override_id (str): UUID of an existing override

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not override_id:
            raise RequiredArgument(
                "get_override requires an override_id argument"
            )

        cmd = XmlCommand("get_overrides")
        cmd.set_attribute("override_id", override_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_permissions(self, *, filter=None, filter_id=None, trash=None):
        """Request a list of permissions

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): Whether to get permissions in the
                trashcan instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_permissions")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        return self._send_xml_command(cmd)

    def get_permission(self, permission_id):
        """Request a single permission

        Arguments:
            permission_id (str): UUID of an existing permission

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not permission_id:
            raise RequiredArgument(
                "get_permission requires a permission_id argument"
            )

        cmd = XmlCommand("get_permissions")
        cmd.set_attribute("permission_id", permission_id)
        return self._send_xml_command(cmd)

    def get_port_lists(
        self,
        *,
        filter=None,
        filter_id=None,
        details=None,
        targets=None,
        trash=None
    ):
        """Request a list of port lists

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            details (boolean, optional): Whether to include full port list
                details
            targets (boolean, optional): Whether to include targets using this
                port list
            trash (boolean, optional): Whether to get port lists in the
                trashcan instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_port_lists")

        _add_filter(cmd, filter, filter_id)

        if not details is None:
            cmd.set_attribute("details", _to_bool(details))

        if not targets is None:
            cmd.set_attribute("targets", _to_bool(targets))

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        return self._send_xml_command(cmd)

    def get_port_list(self, port_list_id):
        """Request a single port list

        Arguments:
            port_list_id (str): UUID of an existing port list

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument(
                "get_port_list requires a port_list_id argument"
            )

        cmd = XmlCommand("get_port_lists")
        cmd.set_attribute("port_list_id", port_list_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_preferences(self, *, nvt_oid=None, config_id=None):
        """Request a list of preferences

        When the command includes a config_id attribute, the preference element
        includes the preference name, type and value, and the NVT to which the
        preference applies. Otherwise, the preference element includes just the
        name and value, with the NVT and type built into the name.

        Arguments:
            nvt_oid (str, optional): OID of nvt
            config_id (str, optional): UUID of scan config of which to show
                preference values
            preference (str, optional): name of a particular preference to get

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_preferences")

        if nvt_oid:
            cmd.set_attribute("nvt_oid", nvt_oid)

        if config_id:
            cmd.set_attribute("config_id", config_id)

        return self._send_xml_command(cmd)

    def get_preference(self, name):
        """Request a nvt preference


        Arguments:
            preference (str): name of a particular preference

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument("get_preference requires a name argument")

        cmd = XmlCommand("get_preferences")

        cmd.set_attribute("preference", name)

        return self._send_xml_command(cmd)

    def get_reports(
        self,
        *,
        filter=None,
        filter_id=None,
        note_details=None,
        override_details=None,
        no_details=None
    ):
        """Request a list of reports

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            note_details (boolean, optional): If notes are included, whether to
                include note details
            override_details (boolean, optional): If overrides are included,
                whether to include override details
            no_details (boolean, optional): Whether to exclude results

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_reports")

        if filter:
            cmd.set_attribute("report_filter", filter)

        if filter_id:
            cmd.set_attribute("report_filt_id", filter_id)

        if not note_details is None:
            cmd.set_attribute("note_details", _to_bool(note_details))

        if not override_details is None:
            cmd.set_attribute("override_details", _to_bool(override_details))

        if not no_details is None:
            cmd.set_attribute("details", _to_bool(not no_details))

        cmd.set_attribute("ignore_pagination", "1")

        return self._send_xml_command(cmd)

    def get_report(
        self,
        report_id,
        *,
        filter=None,
        filter_id=None,
        delta_report_id=None,
        report_format_id=None
    ):
        """Request a single report

        Arguments:
            report_id (str): UUID of an existing report
            filter (str, optional): Filter term to use to filter results in the
                report
            filter_id (str, optional): UUID of filter to use to filter results
                in the report
            delta_report_id (str, optional): UUID of an existing report to
                compare report to.
            report_format_id (str, optional): UUID of report format to use

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_id:
            raise RequiredArgument("get_report requires a report_id argument")

        cmd = XmlCommand("get_reports")
        cmd.set_attribute("report_id", report_id)

        _add_filter(cmd, filter, filter_id)

        if delta_report_id:
            cmd.set_attribute("delta_report_id", delta_report_id)

        if report_format_id:
            cmd.set_attribute("format_id", report_format_id)

        return self._send_xml_command(cmd)

    def get_report_formats(
        self,
        *,
        filter=None,
        filter_id=None,
        trash=None,
        alerts=None,
        params=None,
        details=None
    ):
        """Request a list of report formats

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): Whether to get the trashcan report
                formats instead
            alerts (boolean, optional): Whether to include alerts that use the
                report format
            params (boolean, optional): Whether to include report format
                parameters
            details (boolean, optional): Include report format file, signature
                and parameters

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_report_formats")

        _add_filter(cmd, filter, filter_id)

        if not details is None:
            cmd.set_attribute("details", _to_bool(details))

        if not alerts is None:
            cmd.set_attribute("alerts", _to_bool(alerts))

        if not params is None:
            cmd.set_attribute("params", _to_bool(params))

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        return self._send_xml_command(cmd)

    def get_report_format(self, report_format_id):
        """Request a single report format

        Arguments:
            report_format_id (str): UUID of an existing report format

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                "get_report_format requires report_format_id argument"
            )

        cmd = XmlCommand("get_report_formats")
        cmd.set_attribute("report_format_id", report_format_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_results(
        self,
        *,
        filter=None,
        filter_id=None,
        task_id=None,
        note_details=None,
        override_details=None,
        details=None
    ):
        """Request a list of results

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            task_id (str, optional): UUID of task for note and override handling
            note_details (boolean, optional): If notes are included, whether to
                include note details
            override_details (boolean, optional): If overrides are included,
                whether to include override details
            details (boolean, optional): Whether to include additional details
                of the results

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_results")

        _add_filter(cmd, filter, filter_id)

        if task_id:
            cmd.set_attribute("task_id", task_id)

        if not details is None:
            cmd.set_attribute("details", _to_bool(details))

        if not note_details is None:
            cmd.set_attribute("note_details", _to_bool(note_details))

        if not override_details is None:
            cmd.set_attribute("override_details", _to_bool(override_details))

        return self._send_xml_command(cmd)

    def get_result(self, result_id):
        """Request a single result

        Arguments:
            result_id (str): UUID of an existing result

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not result_id:
            raise RequiredArgument("get_result requires a result_id argument")

        cmd = XmlCommand("get_results")
        cmd.set_attribute("result_id", result_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_roles(self, *, filter=None, filter_id=None, trash=None):
        """Request a list of roles

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): Whether to get the trashcan roles instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_roles")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        return self._send_xml_command(cmd)

    def get_role(self, role_id):
        """Request a single role

        Arguments:
            role_id (str): UUID of an existing role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not role_id:
            raise RequiredArgument("get_role requires a role_id argument")

        cmd = XmlCommand("get_roles")
        cmd.set_attribute("role_id", role_id)
        return self._send_xml_command(cmd)

    def get_scanners(
        self, *, filter=None, filter_id=None, trash=None, details=None
    ):
        """Request a list of scanners

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): Whether to get the trashcan scanners
                instead
            details (boolean, optional):  Whether to include extra details like
                tasks using this scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_scanners")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        if not details is None:
            cmd.set_attribute("details", _to_bool(details))

        return self._send_xml_command(cmd)

    def get_scanner(self, scanner_id):
        """Request a single scanner

        Arguments:
            scanner_id (str): UUID of an existing scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument("get_scanner requires a scanner_id argument")

        cmd = XmlCommand("get_scanners")
        cmd.set_attribute("scanner_id", scanner_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_schedules(
        self, *, filter=None, filter_id=None, trash=None, tasks=None
    ):
        """Request a list of schedules

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): Whether to get the trashcan schedules
                instead
            tasks (boolean, optional): Whether to include tasks using the
                schedules

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_schedules")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        if not tasks is None:
            cmd.set_attribute("tasks", _to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_schedule(self, schedule_id):
        """Request a single schedule

        Arguments:
            schedule_id (str): UUID of an existing schedule

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not schedule_id:
            raise RequiredArgument(
                "get_schedule requires a schedule_id argument"
            )

        cmd = XmlCommand("get_schedules")
        cmd.set_attribute("schedule_id", schedule_id)
        return self._send_xml_command(cmd)

    def get_settings(self, *, filter=None):
        """Request a list of user settings

        Arguments:
            filter (str, optional): Filter term to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_settings")

        if filter:
            cmd.set_attribute("filter", filter)

        return self._send_xml_command(cmd)

    def get_setting(self, setting_id):
        """Request a single setting

        Arguments:
            setting_id (str): UUID of an existing setting

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not setting_id:
            raise RequiredArgument("get_setting requires a setting_id argument")

        cmd = XmlCommand("get_settings")
        cmd.set_attribute("setting_id", setting_id)
        return self._send_xml_command(cmd)

    def get_system_reports(
        self,
        *,
        name=None,
        duration=None,
        start_time=None,
        end_time=None,
        brief=None,
        slave_id=None
    ):
        """Request a list of system reports

        Arguments:
            name (str, optional): A string describing the required system report
            duration (int, optional): The number of seconds into the past that
                the system report should include
            start_time (str, optional): The start of the time interval the
                system report should include in ISO time format
            end_time (str, optional): The end of the time interval the system
                report should include in ISO time format
            brief (boolean, optional): Whether to include the actual system
                reports
            slave_id (str, optional): UUID of GMP scanner from which to get the
                system reports

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_system_reports")

        if name:
            cmd.set_attribute("name", name)

        if not duration is None:
            if not isinstance(duration, numbers.Integral):
                raise InvalidArgument("duration needs to be an integer number")

            cmd.set_attribute("duration", str(duration))

        if start_time:
            cmd.set_attribute("start_time", str(start_time))

        if end_time:
            cmd.set_attribute("end_time", str(end_time))

        if not brief is None:
            cmd.set_attribute("brief", _to_bool(brief))

        if slave_id:
            cmd.set_attribute("slave_id", slave_id)

        return self._send_xml_command(cmd)

    def get_tags(
        self, *, filter=None, filter_id=None, trash=None, names_only=None
    ):
        """Request a list of tags

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): Whether to get tags from the trashcan
                instead
            names_only (boolean, optional): Whether to get only distinct tag
                names

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tags")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        if not names_only is None:
            cmd.set_attribute("names_only", _to_bool(names_only))

        return self._send_xml_command(cmd)

    def get_tag(self, tag_id):
        """Request a single tag

        Arguments:
            tag_id (str): UUID of an existing tag

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tag_id:
            raise RequiredArgument("get_tag requires a tag_id argument")

        cmd = XmlCommand("get_tags")
        cmd.set_attribute("tag_id", tag_id)
        return self._send_xml_command(cmd)

    def get_targets(
        self, *, filter=None, filter_id=None, trash=None, tasks=None
    ):
        """Request a list of targets

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): Whether to get the trashcan targets
                instead
            tasks (boolean, optional): Whether to include list of tasks that
                use the target

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_targets")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        if not tasks is None:
            cmd.set_attribute("tasks", _to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_target(self, target_id):
        """Request a single target

        Arguments:
            target_id (str): UUID of an existing target

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not target_id:
            raise RequiredArgument("get_target requires a target_id argument")

        cmd = XmlCommand("get_targets")
        cmd.set_attribute("target_id", target_id)
        return self._send_xml_command(cmd)

    def get_tasks(
        self,
        *,
        filter=None,
        filter_id=None,
        trash=None,
        details=None,
        schedules_only=None
    ):
        """Request a list of tasks

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): Whether to get the trashcan tasks instead
            details (boolean, optional): Whether to include full task details
            schedules_only (boolean, optional): Whether to only include id, name
                and schedule details

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tasks")

        _add_filter(cmd, filter, filter_id)

        if not trash is None:
            cmd.set_attribute("trash", _to_bool(trash))

        if not details is None:
            cmd.set_attribute("details", _to_bool(details))

        if not schedules_only is None:
            cmd.set_attribute("schedules_only", _to_bool(schedules_only))

        return self._send_xml_command(cmd)

    def get_task(self, task_id):
        """Request a single task

        Arguments:
            task_id (str): UUID of an existing task

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument("get_task requires task_id argument")

        cmd = XmlCommand("get_tasks")
        cmd.set_attribute("task_id", task_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_users(self, *, filter=None, filter_id=None):
        """Request a list of users

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_users")

        _add_filter(cmd, filter, filter_id)

        return self._send_xml_command(cmd)

    def get_user(self, user_id):
        """Request a single user

        Arguments:
            user_id (str): UUID of an existing user

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not user_id:
            raise RequiredArgument("get_user requires a user_id argument")

        cmd = XmlCommand("get_users")
        cmd.set_attribute("user_id", user_id)
        return self._send_xml_command(cmd)

    def get_version(self):
        """Get the Greenbone Manager Protocol version used by the remote gvmd

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("get_version"))

    def help(self, *, format=None, help_type=""):
        """Get the help text

        Arguments:
            format (str, optional): One of "html", "rnc", "text" or "xml
            type (str, optional): One of "brief" or "". Default ""

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

    def modify_agent(self, agent_id, *, name=None, comment=None):
        """Modifies an existing agent

        Arguments:
            agent_id (str) UUID of the agent to be modified.
            name (str, optional): Name of the new credential
            comment (str, optional): Comment for the credential

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not agent_id:
            raise RequiredArgument("modify_agent requires agent_id argument")

        cmd = XmlCommand("modify_agent")
        cmd.set_attribute("agent_id", str(agent_id))

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def modify_alert(
        self,
        alert_id,
        *,
        name=None,
        comment=None,
        filter_id=None,
        event=None,
        event_data=None,
        condition=None,
        condition_data=None,
        method=None,
        method_data=None
    ):
        """Modifies an existing alert.

        Arguments:
            alert_id (str) UUID of the alert to be modified.
            name (str, optional): Name of the Alert.
            condition (str, optional): The condition that must be satisfied
                for the alert to occur.
            condition (str, optional): The condition that must be satisfied for
                the alert to occur; if the event is either 'Updated SecInfo
                arrived' or 'New SecInfo arrived', condition must be 'Always'.
                Otherwise, condition can also be on of 'Severity at least',
                'Filter count changed' or 'Filter count at least'.
            condition_data (dict, optional): Data that defines the condition
            event (str, optional): The event that must happen for the alert to
                occur, one of 'Task run status changed',
                'Updated SecInfo arrived' or 'New SecInfo arrived'
            event_data (dict, optional): Data that defines the event
            method (str, optional): The method by which the user is alerted,
                one of 'SCP', 'Send', 'SMB', 'SNMP', 'Syslog' or 'Email';
                if the event is neither 'Updated SecInfo arrived' nor
                'New SecInfo arrived', method can also be one of 'Start Task',
                'HTTP Get', 'Sourcefire Connector' or 'verinice Connector'.
            method_data (dict, optional): Data that defines the method
            filter_id (str, optional): Filter to apply when executing alert
            comment (str, optional): Comment for the alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        if not alert_id:
            raise RequiredArgument("modify_alert requires an alert_id argument")

        _check_event(event, condition, method)

        cmd = XmlCommand("modify_alert")
        cmd.set_attribute("alert_id", str(alert_id))

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if filter_id:
            cmd.add_element("filter", attrs={"id": filter_id})

        if condition:
            conditions = cmd.add_element("condition", condition)

            if not condition_data is None:
                for key, value in condition_data.items():
                    _data = conditions.add_element("data", value)
                    _data.add_element("name", key)

        if event:
            events = cmd.add_element("event", event)

            if not event_data is None:
                for key, value in event_data.items():
                    _data = events.add_element("data", value)
                    _data.add_element("name", key)

        if method:
            methods = cmd.add_element("method", method)

            if not method_data is None:
                for key, value in method_data.items():
                    _data = methods.add_element("data", value)
                    _data.add_element("name", key)

        return self._send_xml_command(cmd)

    def modify_asset(self, asset_id, comment=""):
        """Modifies an existing asset.

        Arguments:
            asset_id (str) UUID of the asset to be modified.
            comment (str, optional): Comment for the asset.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not asset_id:
            raise RequiredArgument("modify_asset requires an asset_id argument")

        cmd = XmlCommand("modify_asset")
        cmd.set_attribute("asset_id", asset_id)
        cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def modify_auth(self, group_name, auth_conf_settings):
        """Modifies an existing auth.

        Arguments:
            group_name (str) Name of the group to be modified.
            auth_conf_settings (dict): The new auth config.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_name:
            raise RequiredArgument("modify_auth requires a group_name argument")
        if not auth_conf_settings:
            raise RequiredArgument(
                "modify_auth requires an " "auth_conf_settings argument"
            )
        cmd = XmlCommand("modify_auth")
        _xmlgroup = cmd.add_element("group", attrs={"name": str(group_name)})

        for key, value in auth_conf_settings.items():
            _xmlauthconf = _xmlgroup.add_element("auth_conf_setting")
            _xmlauthconf.add_element("key", key)
            _xmlauthconf.add_element("value", value)

        return self._send_xml_command(cmd)

    def modify_config_set_nvt_preference(
        self, config_id, name, nvt_oid, *, value=None
    ):
        """Modifies the nvt preferences of an existing scan config.

        Arguments:
            config_id (str): UUID of scan config to modify.
            name (str): Name for preference to change.
            nvt_oid (str): OID of the NVT associated with preference to modify
            value (str, optional): New value for the preference. None to delete
                the preference and to use the default instead.
        """
        if not config_id:
            raise RequiredArgument(
                "modify_config_set_nvt_preference requires config_id argument"
            )

        if not nvt_oid:
            raise RequiredArgument(
                "modify_config_set_nvt_preference requires a nvt_oid argument"
            )

        if not name:
            raise RequiredArgument(
                "modify_config_set_nvt_preference requires a name argument"
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        _xmlpref = cmd.add_element("preference")

        _xmlpref.add_element("nvt", attrs={"oid": nvt_oid})
        _xmlpref.add_element("name", name)

        if value:
            _xmlpref.add_element("value", _to_base64(value))

        return self._send_xml_command(cmd)

    def modify_config_set_comment(self, config_id, comment=""):
        """Modifies the comment of an existing scan config

        Arguments:
            config_id (str): UUID of scan config to modify.
            comment (str, optional): Comment to set on a config. Default: ''
        """
        if not config_id:
            raise RequiredArgument(
                "modify_config_set_comment requires a config_id argument"
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def modify_config_set_scanner_preference(
        self, config_id, name, *, value=None
    ):
        """Modifies the scanner preferences of an existing scan config

        Arguments:
            config_id (str): UUID of scan config to modify.
            name (str): Name of the scanner preference to change
            value (str, optional): New value for the preference. None to delete
                the preference and to use the default instead.

        """
        if not config_id:
            raise RequiredArgument(
                "modify_config_set_scanner_preference requires a config_id "
                "argument"
            )

        if not name:
            raise RequiredArgument(
                "modify_config_set_scanner_preference requires a name argument"
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        _xmlpref = cmd.add_element("preference")

        _xmlpref.add_element("name", name)

        if value:
            _xmlpref.add_element("value", _to_base64(value))

        return self._send_xml_command(cmd)

    def modify_config_set_nvt_selection(self, config_id, family, nvt_oids):
        """Modifies the selected nvts of an existing scan config

        The manager updates the given family in the config to include only the
        given NVTs.

        Arguments:
            config_id (str): UUID of scan config to modify.
            family (str): Name of the NVT family to include NVTs from
            nvt_oids (list): List of NVTs to select for the family.
        """
        if not config_id:
            raise RequiredArgument(
                "modify_config_set_nvt_selection requires a config_id "
                "argument"
            )

        if not family:
            raise RequiredArgument(
                "modify_config_set_nvt_selection requires a family argument"
            )

        if not _is_list_like(nvt_oids):
            raise InvalidArgument(
                "modify_config_set_nvt_selection requires an iterable as "
                "nvt_oids argument"
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
        config_id,
        families,
        *,
        auto_add_new_families=True,
        auto_add_new_nvts=True
    ):
        """
        Selected the NVTs of a scan config at a family level.

        Arguments:
            config_id (str): UUID of scan config to modify.
            families (list): List of NVT family names to select.
            auto_add_new_families (boolean, optional): Whether new families
                should be added to the scan config automatically. Default: True.
            auto_add_new_nvts (boolean, optional): Whether new NVTs in the
                selected families should be added to the scan config
                automatically. Default: True.
        """
        if not config_id:
            raise RequiredArgument(
                "modify_config_set_family_selection requires a config_id "
                "argument"
            )

        if not _is_list_like(families):
            raise InvalidArgument(
                "modify_config_set_family_selection requires a list as "
                "families argument"
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

    def modify_config(self, config_id, selection=None, **kwargs):
        """Modifies an existing scan config.

        DEPRECATED. Please use *modify_config_set_* methods instead.

        modify_config has four modes to operate depending on the selection.

        Arguments:
            config_id (str): UUID of scan config to modify.
            selection (str): one of 'scan_pref', 'nvt_pref', 'nvt_selection' or
                'family_selection'
            name (str, optional): New name for preference.
            value(str, optional): New value for preference.
            nvt_oids (list, optional): List of NVTs associated with preference
                to modify.
            family (str,optional): Name of family to modify.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config_id:
            raise RequiredArgument("modify_config required config_id argument")

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
        credential_id,
        credential_type=None,
        *,
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
        privacy_password=None
    ):
        """Modifies an existing credential.

        Arguments:
            credential_id (str): UUID of the credential
            credential_type (str, optional): The credential type. One of 'cc',
                'snmp', 'up', 'usk'
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
                    "modify_credential requires type "
                    "to be either cc, snmp, up or usk"
                )

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", _to_bool(allow_insecure))

        if certificate:
            cmd.add_element("certificate", certificate)

        if key_phrase is not None or private_key:
            if key_phrase is not None and not private_key:
                raise RequiredArgument(
                    "modify_credential requires "
                    "key_phrase and private_key arguments"
                )

            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("private", private_key)

            if key_phrase is not None:
                _xmlkey.add_element("phrase", key_phrase)

        if login:
            cmd.add_element("login", login)

        if password:
            cmd.add_element("password", password)

        if auth_algorithm is not None:
            if auth_algorithm not in ("md5", "sha1"):
                raise InvalidArgument(
                    "modify_credential requires "
                    "auth_algorithm to be either "
                    "md5 or sha1"
                )
            cmd.add_element("auth_algorithm", auth_algorithm)

        if community:
            cmd.add_element("community", community)

        if privacy_algorithm is not None:
            if privacy_algorithm not in ("aes", "des"):
                raise InvalidArgument(
                    "modify_credential requires "
                    "privacy_algorithm to be either"
                    "aes or des"
                )

            _xmlprivacy = cmd.add_element("privacy")
            _xmlprivacy.add_element("algorithm", privacy_algorithm)

            if privacy_password is not None:
                _xmlprivacy.add_element("password", privacy_password)

        return self._send_xml_command(cmd)

    def modify_filter(
        self, filter_id, *, comment=None, name=None, term=None, filter_type=None
    ):
        """Modifies an existing filter.

        Arguments:
            filter_id (str): UUID of the filter to be modified
            comment (str, optional): Comment on filter.
            name (str, optional): Name of filter.
            term (str, optional): Filter term.
            filter_type (str, optional): Resource type filter applies to.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not filter_id:
            raise RequiredArgument(
                "modify_filter requires a filter_id " "attribute"
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
            filter_type = filter_type.lower()
            if filter_type not in FILTER_TYPES:
                raise InvalidArgument(
                    "modify_filter requires type to be one of {0} but "
                    "was {1}".format(", ".join(FILTER_TYPES), filter_type)
                )
            cmd.add_element("type", filter_type)

        return self._send_xml_command(cmd)

    def modify_group(self, group_id, *, comment=None, name=None, users=None):
        """Modifies an existing group.

        Arguments:
            group_id (str): UUID of group to modify.
            comment (str, optional): Comment on group.
            name (str, optional): Name of group.
            users (list, optional): List of user names to be in the group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_id:
            raise RequiredArgument("modify_group requires a group_id argument")

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
        note_id,
        text,
        *,
        seconds_active=None,
        hosts=None,
        port=None,
        result_id=None,
        severity=None,
        task_id=None,
        threat=None
    ):
        """Modifies an existing note.

        Arguments:
            note_id (str): UUID of note to modify.
            text (str): The text of the note.
            seconds_active (int, optional): Seconds note will be active.
                -1 on always, 0 off.
            hosts (list, optional): A list of hosts addresses
            port (int, optional): Port to which note applies.
            result_id (str, optional): Result to which note applies.
            severity (descimal, optional): Severity to which note applies.
            task_id (str, optional): Task to which note applies.
            threat (str, optional): Threat level to which note applies. One of
                High, Medium, Low, Alarm, Log or Debug. Will be converted to
                severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not note_id:
            raise RequiredArgument("modify_note requires a note_id attribute")

        if not text:
            raise RequiredArgument("modify_note requires a text element")

        cmd = XmlCommand("modify_note")
        cmd.set_attribute("note_id", note_id)
        cmd.add_element("text", text)

        if not seconds_active is None:
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
            cmd.add_element("threat", threat)

            if threat not in THREAD_TYPES:
                raise InvalidArgument(
                    "modify_note threat argument {0} is invalid. threat must "
                    "be one of {1}".format(threat, ", ".join(THREAD_TYPES))
                )

        return self._send_xml_command(cmd)

    def modify_override(
        self,
        override_id,
        text,
        *,
        seconds_active=None,
        hosts=None,
        port=None,
        result_id=None,
        severity=None,
        new_severity=None,
        task_id=None,
        threat=None,
        new_threat=None
    ):
        """Modifies an existing override.

        Arguments:
            override_id (str): UUID of override to modify.
            text (str): The text of the override.
            seconds_active (int, optional): Seconds override will be active.
                -1 on always, 0 off.
            hosts (list, optional): A list of host addresses
            port (int, optional): Port to which override applies.
            result_id (str, optional): Result to which override applies.
            severity (decimal, optional): Severity to which override applies.
            new_severity (decimal, optional): New severity score for result.
            task_id (str, optional): Task to which override applies.
            threat (str, optional): Threat level to which override applies. One
                of High, Medium, Low, Alarm, Log or Debug. Will be converted to
                severity.
            new_threat (str, optional): New threat level for results. One
                of High, Medium, Low, Alarm, Log or Debug. Will be converted to
                new_severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not override_id:
            raise RequiredArgument(
                "modify_override requires a override_id " "argument"
            )
        if not text:
            raise RequiredArgument("modify_override requires a text argument")

        cmd = XmlCommand("modify_override")
        cmd.set_attribute("override_id", override_id)
        cmd.add_element("text", text)

        if not seconds_active is None:
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
            if threat not in THREAD_TYPES:
                raise InvalidArgument(
                    "modify_override threat argument {0} is invalid. threat"
                    "must be one of {1}".format(threat, ", ".join(THREAD_TYPES))
                )
            cmd.add_element("threat", threat)

        if new_threat is not None:
            if new_threat not in THREAD_TYPES:
                raise InvalidArgument(
                    "modify_override new_threat argument {0} is invalid. "
                    "new_threat must be one of {1}".format(
                        new_threat, ", ".join(THREAD_TYPES)
                    )
                )

            cmd.add_element("new_threat", new_threat)

        return self._send_xml_command(cmd)

    def modify_permission(
        self,
        permission_id,
        *,
        comment=None,
        name=None,
        resource_id=None,
        resource_type=None,
        subject_id=None,
        subject_type=None
    ):
        """Modifies an existing permission.

        Arguments:
            permission_id (str): UUID of permission to be modified.
            comment (str, optional): The comment on the permission.
            name (str, optional): Permission name, currently the name of
                a command.
            subject_id (str, optional): UUID of subject to whom the permission
                is granted
            subject_type (str, optional): Type of the subject user, group or
                role
            resource_id (str, optional): UUID of entity to which the permission
                applies
            resource_type (str, optional): Type of the resource. For Super
                permissions user, group or role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not permission_id:
            raise RequiredArgument(
                "modify_permission requires " "a permission_id element"
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
                    "modify_permission requires resource_id for resource_type"
                )

            if not resource_type:
                raise RequiredArgument(
                    "modify_permission requires resource_type for resource_id"
                )

            _xmlresource = cmd.add_element(
                "resource", attrs={"id": resource_id}
            )
            _xmlresource.add_element("type", resource_type)

        if subject_id or subject_type:
            if not subject_id:
                raise RequiredArgument(
                    "modify_permission requires a subject_id for subject_type"
                )

            if subject_type not in SUBJECT_TYPES:
                raise InvalidArgument(
                    "modify_permission requires subject_type to be either "
                    "user, group or role"
                )

            _xmlsubject = cmd.add_element("subject", attrs={"id": subject_id})
            _xmlsubject.add_element("type", subject_type)

        return self._send_xml_command(cmd)

    def modify_port_list(self, port_list_id, *, comment=None, name=None):
        """Modifies an existing port list.

        Arguments:
            port_list_id (str): UUID of port list to modify.
            name (str, optional): Name of port list.
            comment (str, optional): Comment on port list.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument(
                "modify_port_list requires " "a port_list_id attribute"
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
        report_format_id,
        *,
        active=None,
        name=None,
        summary=None,
        param_name=None,
        param_value=None
    ):
        """Modifies an existing report format.

        Arguments:
            report_format_id (str) UUID of report format to modify.
            active (boolean, optional): Whether the report format is active.
            name (str, optional): The name of the report format.
            summary (str, optional): A summary of the report format.
            param_name (str, optional): The name of the param.
            param_value (str, optional): The value of the param.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                "modify_report requires " "a report_format_id attribute"
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

    def modify_role(self, role_id, *, comment=None, name=None, users=None):
        """Modifies an existing role.

        Arguments:
            role_id (str): UUID of role to modify.
            comment (str, optional): Name of role.
            name (str, optional): Comment on role.
            users  (list, optional): List of user names.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not role_id:
            raise RequiredArgument("modify_role requires a role_id argument")

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
        scanner_id,
        *,
        scanner_type=None,
        host=None,
        port=None,
        comment=None,
        name=None,
        ca_pub=None,
        credential_id=None
    ):
        """Modifies an existing scanner.

        Arguments:
            scanner_id (str): UUID of scanner to modify.
            scanner_type (str, optional): New type of the Scanner. Must be one
                of '1' (OSP Scanner), '2' (OpenVAS Scanner), '3' CVE Scanner or
                '4' (GMP Scanner).
            host (str, optional): Host of the scanner.
            port (int, optional): Port of the scanner.
            comment (str, optional): Comment on scanner.
            name (str, optional): Name of scanner.
            ca_pub (str, optional): Certificate of CA to verify scanner's
                certificate.
            credential_id (str, optional): UUID of the client certificate
                credential for the Scanner.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                "modify_scanner requires a scanner_id argument"
            )

        if scanner_type is not None and scanner_type not in SCANNER_TYPES:
            raise InvalidArgument(
                "modify_scanner requires a scanner_type "
                'argument which must be either "1" for OSP, '
                '"2" for OpenVAS (Classic), "3" for CVE or '
                '"4" for GMP Scanner.'
            )

        cmd = XmlCommand("modify_scanner")
        cmd.set_attribute("scanner_id", scanner_id)

        if scanner_type:
            cmd.add_element("type", scanner_type)

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
        schedule_id,
        *,
        comment=None,
        name=None,
        first_time_minute=None,
        first_time_hour=None,
        first_time_day_of_month=None,
        first_time_month=None,
        first_time_year=None,
        duration=None,
        duration_unit=None,
        period=None,
        period_unit=None,
        timezone=None
    ):
        """Modifies an existing schedule.

        Arguments:
            schedule_id (str): UUID of schedule to modify.
            name (str, optional): Name of the schedule
            comment (str, optional): Comment for the schedule
            first_time_minute (int, optional): First time minute the schedule
                will run. Must be an integer >= 0.
            first_time_hour (int, optional): First time hour the schedule
                will run. Must be an integer >= 0.
            first_time_day_of_month (int, optional): First time day of month the
                schedule will run. Must be an integer > 0 <= 31.
            first_time_month (int, optional): First time month the schedule
                will run. Must be an integer >= 1 <= 12.
            first_time_year (int, optional): First time year the schedule
                will run
            duration (int, optional): How long the Manager will run the
                scheduled task for until it gets paused if not finished yet.
            duration_unit (str, optional): Unit of the duration. One of second,
                minute, hour, day, week, month, year, decade. Required if
                duration is set.
            period (int, optional): How often the Manager will repeat the
                scheduled task. Must be an integer > 0.
            period_unit (str, optional): Unit of the period. One of second,
                minute, hour, day, week, month, year, decade. Required if
                period is set.
            timezone (str, optional): The timezone the schedule will follow

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not schedule_id:
            raise RequiredArgument(
                "modify_schedule requires a schedule_id" "argument"
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
                    "Setting first_time requires first_time_minute argument"
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
                    "Setting first_time requires first_time_hour argument"
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
                    "Setting first_time requires first_time_day_of_month "
                    "argument"
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
                    "Setting first_time requires first_time_month argument"
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
                    "Setting first_time requires first_time_year argument"
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
                    "Setting duration requires duration_unit argument"
                )

            if not duration_unit in TIME_UNITS:
                raise InvalidArgument(
                    "duration_unit must be one of {units} but {actual} has "
                    "been passed".format(
                        units=", ".join(TIME_UNITS), actual=duration_unit
                    )
                )

            if not isinstance(duration, numbers.Integral) or duration < 1:
                raise InvalidArgument(
                    "duration argument must be an integer greater than 0"
                )

            _xmlduration = cmd.add_element("duration", str(duration))
            _xmlduration.add_element("unit", duration_unit)

        if period is not None:
            if not period_unit:
                raise RequiredArgument(
                    "Setting period requires period_unit argument"
                )

            if not period_unit in TIME_UNITS:
                raise InvalidArgument(
                    "period_unit must be one of {units} but {actual} has "
                    "been passed".format(
                        units=", ".join(TIME_UNITS), actual=period_unit
                    )
                )

            if not isinstance(period, numbers.Integral) or period < 1:
                raise InvalidArgument(
                    "period argument must be an integer greater than 0"
                )

            _xmlperiod = cmd.add_element("period", str(period))
            _xmlperiod.add_element("unit", period_unit)

        if timezone:
            cmd.add_element("timezone", timezone)

        return self._send_xml_command(cmd)

    def modify_setting(self, setting_id=None, name=None, value=None):
        """Modifies an existing setting.

        Arguments:
            setting_id (str, optional): UUID of the setting to be changed.
            name (str, optional): The name of the setting. Either setting_id or
                name must be passed.
            value (str): The value of the setting.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not setting_id and not name:
            raise RequiredArgument(
                "modify_setting requires a setting_id or name argument"
            )

        if value is None:
            raise RequiredArgument("modify_setting requires a value argument")

        cmd = XmlCommand("modify_setting")

        if setting_id:
            cmd.set_attribute("setting_id", setting_id)
        else:
            cmd.add_element("name", name)

        cmd.add_element("value", _to_base64(value))

        return self._send_xml_command(cmd)

    def modify_tag(
        self,
        tag_id,
        *,
        comment=None,
        name=None,
        value=None,
        active=None,
        resource_id=None,
        resource_type=None
    ):
        """Modifies an existing tag.

        Arguments:
            tag_id (str): UUID of the tag.
            comment (str, optional): Comment to add to the tag.
            name (str, optional): Name of the tag.
            value (str, optional): Value of the tag.
            active (boolean, optional): Whether the tag is active.
            resource_id (str, optional): ID of the resource to which to
                attach the tag. Required if resource_type is set.
            resource_type (str, optional): Type of the resource to which to
                attach the tag. Required if resource_id is set.

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

        if resource_id or resource_type:
            if not resource_id:
                raise RequiredArgument(
                    "modify_tag requires resource_id argument when "
                    "resource_type is set"
                )

            if not resource_type:
                raise RequiredArgument(
                    "modify_tag requires resource_type argument when "
                    "resource_id is set"
                )

            _xmlresource = cmd.add_element(
                "resource", attrs={"id": resource_id}
            )
            _xmlresource.add_element("type", resource_type)

        return self._send_xml_command(cmd)

    def modify_target(
        self,
        target_id,
        *,
        name=None,
        comment=None,
        hosts=None,
        exclude_hosts=None,
        ssh_credential_id=None,
        ssh_credential_port=None,
        smb_credential_id=None,
        esxi_credential_id=None,
        snmp_credential_id=None,
        alive_tests=None,
        reverse_lookup_only=None,
        reverse_lookup_unify=None,
        port_list_id=None
    ):
        """Modifies an existing target.

        Arguments:
            target_id (uuid) ID of target to modify.
            comment (str, optional): Comment on target.
            name (str, optional): Name of target.
            hosts (list, optional): List of target hosts.
            exclude_hosts (list, optional): A list of hosts to exclude.
            ssh_credential (str, optional): UUID of SSH credential to
                use on target.
            ssh_credential_port (int, optional): The port to use for ssh
                credential
            smb_credential (str, optional): UUID of SMB credential to use
                on target.
            esxi_credential (str, optional): UUID of ESXi credential to use
                on target.
            snmp_credential (str, optional): UUID of SNMP credential to use
                on target.
            port_list (str, optional): UUID of port list describing ports to
                scan.
            alive_tests (str, optional): Which alive tests to use.
            reverse_lookup_only (boolean, optional): Whether to scan only hosts
                that have names.
            reverse_lookup_unify (boolean, optional): Whether to scan only one
                IP when multiple IPs have the same name.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not target_id:
            raise RequiredArgument(
                "modify_target requires a " "target_id argument"
            )

        cmd = XmlCommand("modify_target")
        cmd.set_attribute("target_id", target_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if hosts:
            cmd.add_element("hosts", _to_comma_list(hosts))

        if exclude_hosts:
            cmd.add_element("exclude_hosts", _to_comma_list(exclude_hosts))

        if alive_tests:
            if not alive_tests in ALIVE_TESTS:
                raise InvalidArgument(
                    "alive_tests must be one of {tests} but "
                    "{actual} has been passed".format(
                        tests="|".join(ALIVE_TESTS), actual=alive_tests
                    )
                )
            cmd.add_element("alive_tests", alive_tests)

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

        if not reverse_lookup_only is None:
            cmd.add_element(
                "reverse_lookup_only", _to_bool(reverse_lookup_only)
            )

        if not reverse_lookup_unify is None:
            cmd.add_element(
                "reverse_lookup_unify", _to_bool(reverse_lookup_unify)
            )

        if port_list_id:
            cmd.add_element("port_list", attrs={"id": port_list_id})

        return self._send_xml_command(cmd)

    def modify_task(
        self,
        task_id,
        *,
        name=None,
        config_id=None,
        target_id=None,
        scanner_id=None,
        alterable=None,
        hosts_ordering=None,
        schedule_id=None,
        schedule_periods=None,
        comment=None,
        alert_ids=None,
        observers=None,
        preferences=None
    ):
        """Modifies an existing task.

        Arguments:
            task_id (str) UUID of task to modify.
            name  (str, optional): The name of the task.
            config_id (str, optional): UUID of scan config to use by the task
            target_id (str, optional): UUID of target to be scanned
            scanner_id (str, optional): UUID of scanner to use for scanning the
                target
            comment  (str, optional):The comment on the task.
            alert_ids (list, optional): List of UUIDs for alerts to be applied
                to the task
            hosts_ordering (str, optional): The order hosts are scanned in
            schedule_id (str, optional): UUID of a schedule when the task should
                be run.
            schedule_periods (int, optional): A limit to the number of times
                the task will be scheduled, or 0 for no limit.
            observers (list, optional): List of names or ids of users which
                should be allowed to observe this task
            preferences (dict, optional): Name/Value pairs of scanner
                preferences.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument("modify_task requires a task_id argument")

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

        if not alterable is None:
            cmd.add_element("alterable", _to_bool(alterable))

        if hosts_ordering:
            # not sure about the possible values for hosts_orderning
            # it seems gvmd does not check the param
            # gsa allows to select 'sequential', 'random' or 'reverse'
            cmd.add_element("hosts_ordering", hosts_ordering)

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
                raise InvalidArgument("alert_ids argument must be a list")

            for alert in alert_ids:
                cmd.add_element("alert", attrs={"id": str(alert)})

        if observers is not None:
            if not _is_list_like(observers):
                raise InvalidArgument("obeservers argument must be a list")

            cmd.add_element("observers", _to_comma_list(observers))

        if preferences is not None:
            if not isinstance(preferences, collections.abc.Mapping):
                raise InvalidArgument('preferences argument must be a dict')

            _xmlprefs = cmd.add_element("preferences")
            for pref_name, pref_value in preferences.items():
                _xmlpref = _xmlprefs.add_element("preference")
                _xmlpref.add_element("scanner_name", pref_name)
                _xmlpref.add_element("value", str(pref_value))

        return self._send_xml_command(cmd)

    def modify_user(
        self,
        user_id=None,
        name=None,
        *,
        new_name=None,
        password=None,
        role_ids=None,
        hosts=None,
        hosts_allow=False,
        ifaces=None,
        ifaces_allow=False
    ):
        """Modifies an existing user.

        Arguments:
            user_id (str, optional): UUID of the user to be modified. Overrides
                name element argument.
            name (str, optional): The name of the user to be modified. Either
                user_id or name must be passed.
            new_name (str, optional): The new name for the user.
            password (str, optional): The password for the user.
            roles_id (list, optional): List of roles UUIDs for the user.
            hosts (list, optional): User access rules: List of hosts.
            hosts_allow (boolean,optional): If True, allow only listed,
                otherwise forbid listed.
            ifaces (list, optional): User access rules: List
                of ifaces.
            ifaces_allow (boolean, optional): If True, allow only listed,
                otherwise forbid listed.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not user_id and not name:
            raise RequiredArgument(
                "modify_user requires an user_id or name argument"
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

    def move_task(self, task_id, *, slave_id=None):
        """Move an existing task to another GMP slave scanner or the master

        Arguments:
            task_id (str): UUID of the task to be moved
            slave_id (str, optional): UUID of slave to reassign the task to,
                empty for master.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise InvalidArgument("move_task requires an task_id argument")

        cmd = XmlCommand("move_task")
        cmd.set_attribute("task_id", task_id)

        if not slave_id is None:
            cmd.set_attribute("slave_id", slave_id)

        return self._send_xml_command(cmd)

    def restore(self, entity_id):
        """Restore an entity from the trashcan

        Arguments:
            entity_id (str): ID of the entity to be restored from the trashcan

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not entity_id:
            raise InvalidArgument("restore requires an entity_id argument")

        cmd = XmlCommand("restore")
        cmd.set_attribute("id", entity_id)

        return self._send_xml_command(cmd)

    def resume_task(self, task_id):
        """Resume an existing stopped task

        Arguments:
            task_id (str): UUID of the task to be resumed

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise InvalidArgument("resume_task requires an task_id argument")

        cmd = XmlCommand("resume_task")
        cmd.set_attribute("task_id", task_id)

        return self._send_xml_command(cmd)

    def start_task(self, task_id):
        """Start an existing task

        Arguments:
            task_id (str): UUID of the task to be started

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise InvalidArgument("start_task requires an task_id argument")

        cmd = XmlCommand("start_task")
        cmd.set_attribute("task_id", task_id)

        return self._send_xml_command(cmd)

    def stop_task(self, task_id):
        """Stop an existing running task

        Arguments:
            task_id (str): UUID of the task to be stopped

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise InvalidArgument("stop_task requires an task_id argument")

        cmd = XmlCommand("stop_task")
        cmd.set_attribute("task_id", task_id)

        return self._send_xml_command(cmd)

    def sync_cert(self):
        """Request a synchronization with the CERT feed service

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_cert"))

    def sync_config(self):
        """Request an OSP config synchronization with scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_config"))

    def sync_feed(self):
        """Request a synchronization with the NVT feed service

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_feed"))

    def sync_scap(self):
        """Request a synchronization with the SCAP feed service

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_scap"))

    def test_alert(self, alert_id):
        """Run an alert

        Invoke a test run of an alert

        Arguments:
            alert_id (str): UUID of the alert to be tested

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
        alert_id,
        report_id,
        *,
        filter=None,
        filter_id=None,
        report_format_id=None,
        delta_report_id=None
    ):
        """Run an alert by ignoring its event and conditions

        The alert is triggered to run immediately with the provided filtered
        report by ignoring the even and condition settings.

        Arguments:
            alert_id (str): UUID of the alert to be run
            report_id (str): UUID of the report to be provided to the alert
            filter (str, optional): Filter term to use to filter results in the
                report
            filter_id (str, optional): UUID of filter to use to filter results
                in the report
            report_format_id (str, optional): UUID of report format to use
            delta_report_id (str, optional): UUID of an existing report to
                compare report to.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not alert_id:
            raise RequiredArgument("run_alert requires a alert_id argument")

        if not report_id:
            raise RequiredArgument("run_alert requires a report_id argument")

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

    def verify_agent(self, agent_id):
        """Verify an existing agent

        Verifies the trust level of an existing agent. It will be checked
        whether signature of the agent currently matches the agent. This
        includes the agent installer file. It is *not* verified if the agent
        works as expected by the user.

        Arguments:
            agent_id (str): UUID of the agent to be verified

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not agent_id:
            raise InvalidArgument("verify_agent requires an agent_id argument")

        cmd = XmlCommand("verify_agent")
        cmd.set_attribute("agent_id", agent_id)

        return self._send_xml_command(cmd)

    def verify_report_format(self, report_format_id):
        """Verify an existing report format

        Verifies the trust level of an existing report format. It will be
        checked whether the signature of the report format currently matches the
        report format. This includes the script and files used to generate
        reports of this format. It is *not* verified if the report format works
        as expected by the user.

        Arguments:
            report_format_id (str): UUID of the report format to be verified

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise InvalidArgument(
                "verify_report_format requires a report_format_id argument"
            )

        cmd = XmlCommand("verify_report_format")
        cmd.set_attribute("report_format_id", report_format_id)

        return self._send_xml_command(cmd)

    def verify_scanner(self, scanner_id):
        """Verify an existing scanner

        Verifies if it is possible to connect to an existing scanner. It is
        *not* verified if the scanner works as expected by the user.

        Arguments:
            scanner_id (str): UUID of the scanner to be verified

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise InvalidArgument(
                "verify_scanner requires a scanner_id argument"
            )

        cmd = XmlCommand("verify_scanner")
        cmd.set_attribute("scanner_id", scanner_id)

        return self._send_xml_command(cmd)
