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
Module for communication with gvmd in Greenbone Management Protocol version 7
"""
import logging

from lxml import etree

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.utils import get_version_string
from gvm.xml import _GmpCommandFactory as GmpCommandFactory, XmlCommand

from .base import GvmProtocol

logger = logging.getLogger(__name__)

PROTOCOL_VERSION = (7,)

FILTER_TYPES = [
    'agent',
    'alert',
    'asset',
    'config',
    'credential',
    'filter',
    'group',
    'note',
    'override',
    'permission',
    'port_list',
    'report',
    'report_format',
    'result',
    'role',
    'schedule',
    'secinfo',
    'tag',
    'target',
    'task',
    'user',
]

TIME_UNITS = [
    'second',
    'minute',
    'hour',
    'day',
    'week',
    'month',
    'year',
    'decade',
]


def _check_command_status(xml):
    """Check gmp response

    Look into the gmp response and check for the status in the root element

    Arguments:
        xml {string} -- XML-Source

    Returns:
        bool -- True if valid, otherwise False
    """

    if xml is 0 or xml is None:
        logger.error('XML Command is empty')
        return False

    try:
        parser = etree.XMLParser(encoding='utf-8', recover=True)

        root = etree.XML(xml, parser=parser)
        status = root.attrib['status']
        return status is not None and status[0] == '2'

    except etree.Error as e:
        logger.error('etree.XML(xml): %s', e)
        return False


def _to_bool(value):
    return '1' if value else '0'


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
            conversion into different representaitions like a xml dom.

            See :mod:`gvm.transforms` for existing transforms.

    .. _Greenbone Management Protocol version 7:
        https://docs.greenbone.net/API/GMP/gmp-7.0.html
    .. _callable:
        https://docs.python.org/3.6/library/functions.html#callable
    """

    def __init__(self, connection, transform=None):
        super().__init__(connection, transform)

        # Is authenticated on gvmd
        self._authenticated = False

        # GMP Message Creator
        self._generator = GmpCommandFactory()

    @staticmethod
    def get_protocol_version():
        """Allow to determine the Greenbone Management Protocol version.

            Returns:
                str: Implemented version of the Greenbone Management Protocol
        """
        return get_version_string(PROTOCOL_VERSION)

    def is_authenticated(self):
        """Checks if the user is authenticated

        If the user is authenticated privilged GMP commands like get_tasks
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
        cmd = XmlCommand('authenticate')

        if not username:
            raise RequiredArgument('authenticate requires username')

        if not password:
            raise RequiredArgument('authenticate requires password')

        credentials = cmd.add_element('credentials')
        credentials.add_element('username', username)
        credentials.add_element('password', password)

        self._send(cmd.to_string())
        response = self._read()

        if _check_command_status(response):
            self._authenticated = True

        return self._transform(response)

    def create_agent(self, installer, signature, name, comment=None,
                     howto_install=None, howto_use=None):
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
            raise RequiredArgument('create_agent requires name argument')

        if not installer:
            raise RequiredArgument('create_agent requires installer argument')

        if not signature:
            raise RequiredArgument('create_agent requires signature argument')

        cmd = XmlCommand('create_agent')
        cmd.add_element('installer', installer)
        cmd.add_element('signature', signature)
        cmd.add_element('name', name)

        if comment:
            cmd.add_element('comment', comment)

        if howto_install:
            cmd.add_element('howto_install', howto_install)

        if howto_use:
            cmd.add_element('howto_use', howto_use)

        return self._send_xml_command(cmd)

    def clone_agent(self, agent_id):
        """Clone an existing agent

        Arguments:
            copy (str): UUID of an existing agent to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_agent')
        cmd.add_element('copy', agent_id)
        return self._send_xml_command(cmd)

    def create_alert(self, name, condition, event, method, method_data=None,
                     event_data=None, condition_data=None, filter_id=None,
                     comment=None):
        """Create a new alert

        Arguments:
            name (str): Name of the new Alert
            condition (str): The condition that must be satisfied for the alert
                to occur.
            event (str): The event that must happen for the alert to occur
            method (str): The method by which the user is alerted
            condition_data (dict, optional): Data that defines the condition
            event_data (dict, optional): Data that defines the event
            method_data (dict, optional): Data that defines the method
            filter_id (str, optional): Filter to apply when executing alert
            comment (str, optional): Comment for the alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument('create_alert requires name argument')

        if condition is None or len(condition) == 0:
            raise RequiredArgument('create_alert requires condition argument')

        if event is None or len(event) == 0:
            raise RequiredArgument('create_alert requires event argument')

        cmd = XmlCommand('create_alert')
        cmd.add_element('name', name)

        conditions = cmd.add_element('condition', condition)

        if not condition_data is None:
            for value, key in condition_data.items():
                _data = conditions.add_element('data', value)
                _data.add_element('name', key)

        events = cmd.add_element('event', event)

        if not event_data is None:
            for value, key in event_data.items():
                _data = events.add_element('data', value)
                _data.add_element('name', key)

        methods = cmd.add_element('method', method)

        if not method_data is None:
            for value, key in method_data.items():
                _data = methods.add_element('data', value)
                _data.add_element('name', key)

        if filter_id:
            cmd.add_element('filter', attrs={'id': filter_id})

        if comment:
            cmd.add_element('comment', comment)

        return self._send_xml_command(cmd)

    def clone_alert(self, alert_id):
        """Clone an existing alert

        Arguments:
            copy (str): UUID of an existing alert to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_alert')
        cmd.add_element('copy', alert_id)
        return self._send_xml_command(cmd)

    def create_asset(self, name, asset_type, comment=None):
        """Create a new asset

        Arguments:
            name (str): Name for the new asset
            asset_type (str): Either 'os' or 'host'
            comment (str, optional): Comment for the new asset

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if asset_type not in ('host', 'os'):
            raise InvalidArgument(
                'create_asset requires asset_type to be either host or os')

        if not name:
            raise RequiredArgument('create_asset requires name argument')

        cmd = XmlCommand('create_asset')
        asset = cmd.add_element('asset')
        asset.add_element('type', asset_type)
        asset.add_element('name', name)

        if comment:
            asset.add_element('comment', comment)

        return self._send_xml_command(cmd)

    def create_config(self, name, copy):
        """Create a new scan config from an existing one

        Arguments:
            name (str): Name of the new scan config
            copy (str): UUID of the existing scan config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument('create_config requires name argument')

        if not copy:
            raise RequiredArgument('create_config requires copy argument')

        cmd = XmlCommand('create_config')
        cmd.add_element('copy', copy)
        cmd.add_element('name', name)
        return self._send_xml_command(cmd)

    def create_credential(self, name, comment=None, allow_insecure=False,
                          certificate=None, key_phrase=None, private_key=None,
                          login=None, password=None, auth_algorithm=None,
                          community=None, privacy_algorithm=None,
                          privacy_password=None, credential_type=None):
        """Create a new credential

        Arguments:
            name (str): Name of the new credential
            comment (str, optional): Comment for the credential
            allow_insecure (boolean, optional): Whether to allow insecure use of
                the credential
            certificate (str, optional): Certificate for the credential
            key_phrase (str, optional): Key passphrase for the private key
            private_key (str, optional): Private key to use for login
            login (str, optional): Username for the credential
            password (str, optional): Password for the credential
            community (str, optional): The SNMP community
            privacy_alogorithm (str, optional): The SNMP privacy algorithm,
                either aes or des.
            privacy_password (str, optional): The SNMP privacy password
            credential_type (str, optional): The credential type. One of 'cc',
                'snmp', 'up', 'usk'

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument('create_credential requires name argument')

        cmd = XmlCommand('create_credential')
        cmd.add_element('name', name)

        if comment:
            cmd.add_element('comment', comment)

        if allow_insecure:
            cmd.add_element('allow_insecure', '1')

        if certificate:
            cmd.add_element('certificate', certificate)

        if not key_phrase is None and private_key:
            _xmlkey = cmd.add_element('key')
            _xmlkey.add_element('phrase', key_phrase)
            _xmlkey.add_element('private', private_key)

        if login:
            cmd.add_element('login', login)

        if password:
            cmd.add_element('password', password)

        if auth_algorithm:
            if auth_algorithm not in ('md5', 'sha1'):
                raise InvalidArgument(
                    'create_credential requires auth_algorithm to be either '
                    'md5 or sha1')
            cmd.add_element('auth_algorithm', auth_algorithm)

        if community:
            cmd.add_element('community', community)

        if privacy_algorithm and privacy_password:
            if privacy_algorithm not in ('aes', 'des'):
                raise InvalidArgument(
                    'create_credential requires algorithm to be either aes or '
                    'des')
            _xmlprivacy = cmd.add_element('privacy')
            _xmlprivacy.add_element('algorithm', privacy_algorithm)
            _xmlprivacy.add_element('password', privacy_password)

        if credential_type:
            if credential_type not in ('cc', 'snmp', 'up', 'usk'):
                raise InvalidArgument(
                    'create_credential requires type to be either cc, snmp, up '
                    ' or usk')
            cmd.add_element('type', credential_type)

        return self._send_xml_command(cmd)

    def clone_credential(self, credential_id):
        """Clone an existing credential

        Arguments:
            copy (str): UUID of an existing credential to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_credential')
        cmd.add_element('copy', credential_id)
        return self._send_xml_command(cmd)

    def create_filter(self, name, make_unique=False, filter_type=None,
                      comment=None, term=None):
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
            raise RequiredArgument('create_filter requires a name argument')

        cmd = XmlCommand('create_filter')
        _xmlname = cmd.add_element('name', name)
        if make_unique:
            _xmlname.add_element('make_unique', '1')

        if comment:
            cmd.add_element('comment', comment)

        if term:
            cmd.add_element('term', term)

        if filter_type:
            filter_type = filter_type.lower()
            if filter_type not in FILTER_TYPES:
                raise InvalidArgument(
                    'create_filter requires type to be one of {0} but '
                    'was {1}'.format(', '.join(FILTER_TYPES), filter_type))
            cmd.add_element('type', filter_type)

        return self._send_xml_command(cmd)

    def clone_filter(self, filter_id):
        """Clone an existing filter

        Arguments:
            copy (str): UUID of an existing filter to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_filter')
        cmd.add_element('copy', filter_id)
        return self._send_xml_command(cmd)

    def create_group(self, name, comment=None, special=False, users=None):
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
            raise RequiredArgument('create_group requires a name argument')

        cmd = XmlCommand('create_group')
        cmd.add_element('name', name)

        if comment:
            cmd.add_element('comment', comment)

        if special:
            _xmlspecial = cmd.add_element('specials')
            _xmlspecial.add_element('full')

        if users:
            cmd.add_element('users', ','.join(users))

        return self._send_xml_command(cmd)

    def clone_group(self, group_id):
        """Clone an existing group

        Arguments:
            copy (str): UUID of an existing group to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_group')
        cmd.add_element('copy', group_id)
        return self._send_xml_command(cmd)

    def create_note(self, text, nvt_oid, active=None, comment=None, hosts=None,
                    result_id=None, severity=None, task_id=None, threat=None,
                    port=None):
        """Create a new note

        Arguments:
            text (str): Text of the new note
            nvt_id (str): OID of the nvt to which note applies
            active (int, optional): Seconds note will be active. -1 on
                always, 0 off
            comment (str, optional): Comment for the note
            hosts (list, optional): A list of hosts addresses
            port (str, optional): Port to which the note applies
            result_id (str, optional): UUID of a result to which note applies
            severity (decimal, optional): Severity to which note applies
            task_id (str, optional): UUID of task to which note applies
            threat (str, optional): Threat level to which note applies. Will be
                converted to severity

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not text:
            raise RequiredArgument('create_note requires a text argument')

        if not nvt_oid:
            raise RequiredArgument('create_note requires a nvt_oid argument')

        cmd = XmlCommand('create_note')
        cmd.add_element('text', text)
        cmd.add_element('nvt', attrs={"oid": nvt_oid})

        if not active is None:
            cmd.add_element('active', str(active))

        if comment:
            cmd.add_element('comment', comment)

        if hosts:
            cmd.add_element('hosts', ', '.join(hosts))

        if port:
            cmd.add_element('port', port)

        if result_id:
            cmd.add_element('result', attrs={'id': result_id})

        if severity:
            cmd.add_element('severity', severity)

        if task_id:
            cmd.add_element('task', attrs={'id': task_id})

        if threat:
            cmd.add_element('threat', threat)

        return self._send_xml_command(cmd)

    def clone_note(self, note_id):
        """Clone an existing note

        Arguments:
            copy (str): UUID of an existing note to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_note')
        cmd.add_element('copy', note_id)
        return self._send_xml_command(cmd)

    def create_override(self, text, nvt_oid, active=None, hosts=None,
                        port=None, result_id=None, severity=None, comment=None,
                        new_severity=None, task_id=None, threat=None,
                        new_threat=None):
        """Create a new override

        Arguments:
            text (str): Text of the new override
            nvt_id (str): OID of the nvt to which override applies
            active (int, optional): Seconds override will be active. -1 on
                always, 0 off
            comment (str, optional): Comment for the override
            hosts (list, optional): A list of host addresses
            port (str, optional): Port ot which the override applies
            result_id (str, optional): UUID of a result to which override
                applies
            severity (decimal, optional): Severity to which override applies
            new_severity (decimal, optional): New severity for result
            task_id (str, optional): UUID of task to which override applies
            threat (str, optional): Threat level to which override applies. Will
                be converted to severity
            new_threat (str, optional): New threat level for result, will be
                converted to a new_severity

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not text:
            raise RequiredArgument('create_override requires a text argument')

        if not nvt_oid:
            raise RequiredArgument('create_override requires a nvt_oid '
                                   'argument')

        cmd = XmlCommand('create_override')
        cmd.add_element('text', text)
        cmd.add_element('nvt', attrs={'oid': nvt_oid})

        if active:
            cmd.add_element('active', active)

        if comment:
            cmd.add_element('comment', comment)

        if hosts:
            cmd.add_element('hosts', ', '.join(hosts))

        if port:
            cmd.add_element('port', port)

        if result_id:
            cmd.add_element('result', attrs={'id': result_id})

        if severity:
            cmd.add_element('severity', severity)

        if new_severity:
            cmd.add_element('new_severity', new_severity)

        if task_id:
            cmd.add_element('task', attrs={'id': task_id})

        if threat:
            cmd.add_element('threat', threat)

        if new_threat:
            cmd.add_element('new_threat', new_threat)

        return self._send_xml_command(cmd)

    def clone_override(self, override_id):
        """Clone an existing override

        Arguments:
            copy (str): UUID of an existing override to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_override')
        cmd.add_element('copy', override_id)
        return self._send_xml_command(cmd)

    def create_permission(self, name, subject_id, subject_type,
                          resource_id=None, resource_type=None,
                          comment=None):
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
            raise RequiredArgument('create_permission requires a name argument')

        if not subject_id:
            raise RequiredArgument(
                'create_permission requires a subject_id argument')

        if subject_type not in ('user', 'group', 'role'):
            raise InvalidArgument(
                'create_permission requires subject_type to be either user, '
                'group or role')

        cmd = XmlCommand('create_permission')
        cmd.add_element('name', name)

        _xmlsubject = cmd.add_element('subject', attrs={'id': subject_id})
        _xmlsubject.add_element('type', type)

        if comment:
            cmd.add_element('comment', comment)

        if resource_id and resource_type:
            _xmlresource = cmd.add_element('resource',
                                           attrs={'id': resource_id})
            _xmlresource.add_element('type', resource_type)


        return self._send_xml_command(cmd)

    def clone_permission(self, permission_id):
        """Clone an existing permission

        Arguments:
            copy (str): UUID of an existing permission to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_permission')
        cmd.add_element('copy', permission_id)
        return self._send_xml_command(cmd)

    def create_port_list(self, name, port_range, comment=None):
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
            raise RequiredArgument('create_port_list requires a name argument')

        if not port_range:
            raise RequiredArgument(
                'create_port_list requires a port_range argument')

        cmd = XmlCommand('create_port_list')
        cmd.add_element('name', name)
        cmd.add_element('port_range', port_range)

        if comment:
            cmd.add_element('comment', comment)

        return self._send_xml_command(cmd)

    def clone_port_list(self, port_list_id):
        """Clone an existing port list

        Arguments:
            copy (str): UUID of an existing port list to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_port_list')
        cmd.add_element('copy', port_list_id)
        return self._send_xml_command(cmd)

    def create_port_range(self, port_list_id, start, end, port_range_type,
                          comment=None):
        """Create new port range

        Arguments:
            port_list_id (str): UUID of the port list to which to add the range
            start (int): The first port in the range
            end (int): The last port in the range
            type (str): The type of the ports: TCP, UDP, ...
            comment (str, optional): Comment for the port range

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not port_list_id:
            raise RequiredArgument('create_port_range requires '
                                   'a port_list_id argument')

        if not port_range_type:
            raise RequiredArgument(
                'create_port_range requires a port_range_type argument')

        if not start:
            raise RequiredArgument(
                'create_port_range requires a start argument')

        if not end:
            raise RequiredArgument(
                'create_port_range requires a end argument')

        cmd = XmlCommand('create_port_range')
        cmd.add_element('port_list', attrs={'id': port_list_id})
        cmd.add_element('start', start)
        cmd.add_element('end', end)
        cmd.add_element('type', port_range_type)

        if comment:
            cmd.add_element('comment', comment)

        return self._send_xml_command(cmd)

    def import_report(self, report, task_id=None, task_name=None,
                      task_comment=None, in_assets=None):
        """Import a Report

        Arguments:
            report (str): Report XML as string to import
            task_id (str, optional): UUID of task to import report to
            task_name (str, optional): Name of task to be createed if task_id is
                not present. Either task_id or task_name must be passed
            task_comment (str, optional): Comment for task to be created if
                task_id is not present
            in_asset (boolean, optional): Whether to create or update assets
                using the report

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report:
            raise RequiredArgument('create_report requires a report argument')

        cmd = XmlCommand('create_report')

        if task_id:
            cmd.add_element('task', attrs={'id': task_id})
        elif task_name:
            _xmltask = cmd.add_element('task')
            _xmltask.add_element('name', task_name)

            if task_comment:
                _xmltask.add_element('comment', task_comment)
        else:
            raise RequiredArgument(
                'import_report requires a task_id or task_name argument')

        if not in_assets is None:
            if in_assets:
                cmd.add_element('in_assets', '1')
            else:
                cmd.add_element('in_assets', '0')
        try:
            cmd.append_xml_str(report)
        except etree.XMLSyntaxError as e:
            raise InvalidArgument(
                'Invalid xml passed as report to import_report', e)

        return self._send_xml_command(cmd)

    def create_role(self, name, comment=None, users=None):
        """Create a new role

        Arguments:
            name (str): Name of the role
            comment (str, optional): Comment for the role
            users (list, optional): List of user names to add to the role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        if not name:
            raise RequiredArgument('create_role requires a name argument')

        cmd = XmlCommand('create_role')
        cmd.add_element('name', name)

        if comment:
            cmd.add_element('comment', comment)

        if users:
            cmd.add_element('users', ",".join(users))

        return self._send_xml_command(cmd)

    def clone_role(self, role_id):
        """Clone an existing role

        Arguments:
            copy (str): UUID of an existing role to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_role')
        cmd.add_element('copy', role_id)
        return self._send_xml_command(cmd)

    def create_scanner(self, name, host, port, scanner_type, ca_pub,
                       credential_id, comment=None):
        """Create a new scanner

        Arguments:
            name (str): Name of the scanner
            host (str): The host of the scanner
            port (str): The port of the scanner
            scanner_type (str): The type of the scanner
            ca_pub (str): Certificate of CA to verify scanner certificate
            credential_id (str): UUID of client certificate credential for the
                scanner
            comment (str, optional): Comment for the scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument('create_scanner requires a name argument')

        if not host:
            raise RequiredArgument('create_scanner requires a host argument')

        if not port:
            raise RequiredArgument('create_scanner requires a port argument')

        if not type:
            raise RequiredArgument('create_scanner requires a scanner_type '
                                   'argument')
        if not ca_pub:
            raise RequiredArgument('create_scanner requires a ca_pub argument')

        if not credential_id:
            raise RequiredArgument('create_scanner requires a credential_id '
                                   'argument')

        cmd = XmlCommand('create_scanner')
        cmd.add_element('name', name)
        cmd.add_element('host', host)
        cmd.add_element('port', port)
        cmd.add_element('type', scanner_type)
        cmd.add_element('ca_pub', ca_pub)
        cmd.add_element('credential', attrs={'id': str(credential_id)})

        if comment:
            cmd.add_element('comment', comment)

        return self._send_xml_command(cmd)

    def clone_scanner(self, scanner_id):
        """Clone an existing scanner

        Arguments:
            copy (str): UUID of an existing scanner to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_scanner')
        cmd.add_element('copy', scanner_id)
        return self._send_xml_command(cmd)

    def create_schedule(self, name, comment=None, first_time_minute=None,
                        first_time_hour=None, first_time_day_of_month=None,
                        first_time_month=None, first_time_year=None,
                        duration=None, duration_unit=None, period=None,
                        period_unit=None, timezone=None):
        """Create a new schedule

        Arguments:
            name (str): Name of the schedule
            comment (str, optional): Comment for the schedule
            first_time_minute (int, optional): First time minute the schedule
                will run
            first_time_hour (int, optional): First time hour the schedule
                will run
            first_time_day_of_month (int, optional): First time day of month the
                schedule will run
            first_time_month (int, optional): First time month the schedule
                will run
            first_time_year (int, optional): First time year the schedule
                will run
            duration (int, optional): How long the Manager will run the
                scheduled task for until it gets paused if not finished yet.
            duration_unit (str, optional): Unit of the duration. One of second,
                minute, hour, day, week, month, year, decade. Required if
                duration is set.
            period (int, optional): How often the Manager will repeat the
                scheduled task
            period_unit (str, optional): Unit of the period. One of second,
                minute, hour, day, week, month, year, decade. Required if
                period is set.
            timezone (str, optional): The timezone the schedule will follow

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument('create_schedule requires a name argument')

        cmd = XmlCommand('create_schedule')
        cmd.add_element('name', name)

        if comment:
            cmd.add_element('comment', comment)

        if first_time_minute or first_time_hour or first_time_day_of_month or \
            first_time_month or first_time_year:

            if not first_time_minute:
                raise RequiredArgument(
                    'Setting first_time requires first_time_minute argument')
            if not first_time_hour:
                raise RequiredArgument(
                    'Setting first_time requires first_time_hour argument')
            if not first_time_day_of_month:
                raise RequiredArgument(
                    'Setting first_time requires first_time_day_of_month '
                    'argument')
            if not first_time_month:
                raise RequiredArgument(
                    'Setting first_time requires first_time_month argument')
            if not first_time_year:
                raise RequiredArgument(
                    'Setting first_time requires first_time_year argument')

            _xmlftime = cmd.add_element('first_time')
            _xmlftime.add_element('minute', str(first_time_minute))
            _xmlftime.add_element('hour', str(first_time_hour))
            _xmlftime.add_element('day_of_month', str(first_time_day_of_month))
            _xmlftime.add_element('month', str(first_time_month))
            _xmlftime.add_element('year', str(first_time_year))

        if duration:
            if not duration_unit:
                raise RequiredArgument(
                    'Setting duration requires duration_unit argument')

            if not duration_unit in TIME_UNITS:
                raise InvalidArgument(
                    'duration_unit must be one of {units} but {actual} has '
                    'been passed'.format(
                        units=', '.join(TIME_UNITS), actual=duration_unit))

            _xmlduration = cmd.add_element('duration', str(duration))
            _xmlduration.add_element('unit', duration_unit)

        if period:
            if not period_unit:
                raise RequiredArgument(
                    'Setting period requires period_unit argument')

            if not period_unit in TIME_UNITS:
                raise InvalidArgument(
                    'period_unit must be one of {units} but {actual} has '
                    'been passed'.format(
                        units=', '.join(TIME_UNITS), actual=period_unit))

            _xmlperiod = cmd.add_element('period', str(period))
            _xmlperiod.add_element('unit', period_unit)

        if timezone:
            cmd.add_element('timezone', timezone)

        return self._send_xml_command(cmd)

    def clone_schedule(self, schedule_id):
        """Clone an existing schedule

        Arguments:
            copy (str): UUID of an existing schedule to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_schedule')
        cmd.add_element('copy', schedule_id)
        return self._send_xml_command(cmd)

    def create_tag(self, name, resource_id, resource_type, value=None,
                   comment=None, active=None):
        """Create a new tag

        Arguments:
            name (str): Name of the tag. A full tag name consisting of namespace
                and predicate e.g. `foo:bar`.
            resource_id (str): ID of the resource  the tag is to be attached to.
            resource_type (str): Entity type the tag is to be attached to
            value (str, optional): Value associated with the tag
            comment (str, optional): Comment for the tag
            active (boolean, optional): Whether the tag should be active

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_tag')
        cmd.add_element('name', name)
        _xmlresource = cmd.add_element('resource',
                                       attrs={'id': str(resource_id)})
        _xmlresource.add_element('type', resource_type)

        if comment:
            cmd.add_element('comment', comment)

        if value:
            cmd.add_element('value', value)

        if not active is None:
            if active:
                cmd.add_element('active', '1')
            else:
                cmd.add_element('active', '0')

        return self._send_xml_command(cmd)

    def clone_tag(self, tag_id):
        """Clone an existing tag

        Arguments:
            copy (str): UUID of an existing tag to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_tag')
        cmd.add_element('copy', tag_id)
        return self._send_xml_command(cmd)

    def create_target(self, name, make_unique=False, asset_hosts_filter=None,
                      hosts=None, comment=None, exclude_hosts=None,
                      ssh_credential_id=None, ssh_credential_port=None,
                      smb_credential_id=None, esxi_credential_id=None,
                      snmp_credential_id=None, alive_tests=None,
                      reverse_lookup_only=None, reverse_lookup_unify=None,
                      port_range=None, port_list_id=None):
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
            ssh_credential_port (str, optional): The port to use for ssh
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
            raise RequiredArgument('create_target requires a name argument')

        cmd = XmlCommand('create_target')
        _xmlname = cmd.add_element('name', name)
        if make_unique:
            _xmlname.add_element('make_unique', '1')

        if asset_hosts_filter:
            cmd.add_element('asset_hosts',
                            attrs={'filter': str(asset_hosts_filter)})
        elif hosts:
            cmd.add_element('hosts', ', '.join(hosts))
        else:
            raise RequiredArgument('create_target requires either a hosts or '
                                   'an asset_hosts_filter argument')

        if comment:
            cmd.add_element('comment', comment)

        if exclude_hosts:
            cmd.add_element('exclude_hosts', ', '.join(exclude_hosts))

        if ssh_credential_id:
            _xmlssh = cmd.add_element('ssh_credential',
                                      attrs={'id': ssh_credential_id})
            if ssh_credential_port:
                _xmlssh.add_element('port', ssh_credential_port)

        if smb_credential_id:
            cmd.add_element('smb_credential', attrs={'id': smb_credential_id})

        if esxi_credential_id:
            cmd.add_element('esxi_credential', attrs={'id': esxi_credential_id})

        if snmp_credential_id:
            cmd.add_element('snmp_credential', attrs={'id': snmp_credential_id})

        if alive_tests:
            cmd.add_element('alive_tests', alive_tests)

        if not reverse_lookup_only is None:
            if reverse_lookup_only:
                cmd.add_element('reverse_lookup_only', '1')
            else:
                cmd.add_element('reverse_lookup_only', '0')

        if not reverse_lookup_unify is None:
            if reverse_lookup_unify:
                cmd.add_element('reverse_lookup_unify', '1')
            else:
                cmd.add_element('reverse_lookup_unify', '0')

        if port_range:
            cmd.add_element('port_range', port_range)

        if port_list_id:
            cmd.add_element('port_list', attrs={'id': port_list_id})

        return self._send_xml_command(cmd)

    def clone_target(self, target_id):
        """Clone an existing target

        Arguments:
            copy (str): UUID of an existing target to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_target')
        cmd.add_element('copy', target_id)
        return self._send_xml_command(cmd)

    def create_task(self, name, config_id, target_id, scanner_id,
                    alterable=None, hosts_ordering=None, schedule_id=None,
                    alert_ids=None, comment=None, schedule_periods=None,
                    observers=None):
        """Create a new task

        Arguments:
            name (str): Name of the task
            config_id (str): UUID of scan config to use by the task
            target_id (str): UUID of target to be scanned
            scanner_id (str): UUID of scanner to use for scanning the target
            comment (str, optional): Comment for the task
            alterable (boolean, optional): Wether the task should be alterable
            alert_ids (list, optional): List of UUIDs for alerts to be applied
                to the task
            hosts_ordering (str, optional): The order hosts are scanned in
            schedule_id (str, optional): UUID of a schedule when the task should
                be run.
            schedule_periods (int, optional): A limit to the number of times the
                task will be scheduled, or 0 for no limit
            observers (list, optional): List of user names which should be
                allowed to observe this task

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument('create_task requires a name argument')

        if not config_id:
            raise RequiredArgument('create_task requires a config_id argument')

        if not target_id:
            raise RequiredArgument('create_task requires a target_id argument')

        if not scanner_id:
            raise RequiredArgument('create_task requires a scanner_id argument')

        cmd = XmlCommand('create_task')
        cmd.add_element('name', name)
        cmd.add_element('config', attrs={'id': config_id})
        cmd.add_element('target', attrs={'id': target_id})
        cmd.add_element('scanner', attrs={'id': scanner_id})

        if comment:
            cmd.add_element('comment', comment)

        if not alterable is None:
            if alterable:
                cmd.add_element('alterable', '1')
            else:
                cmd.add_element('alterable', '0')

        if hosts_ordering:
            cmd.add_element('hosts_ordering', hosts_ordering)

        if alert_ids:
            if isinstance(alert_ids, str):
                logger.warning(
                    'Please pass a list as alert_ids parameter to create_task. '
                    'Passing a string is deprecated and will be removed in '
                    'future.')

                #if a single id is given as a string wrap it into a list
                alert_ids = [alert_ids]
            if isinstance(alert_ids, list):
                #parse all given alert id's
                for alert in alert_ids:
                    cmd.add_element('alert', attrs={'id': str(alert)})

        if schedule_id:
            cmd.add_element('schedule', schedule_id)

            if schedule_periods:
                cmd.add_element('schedule_periods', str(schedule_periods))

        if observers:
            cmd.add_element('observers', ' '.join(observers))

        return self._send_xml_command(cmd)

    def clone_task(self, task_id):
        """Clone an existing task

        Arguments:
            task_id (str): UUID of existing task to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_task')
        cmd.add_element('copy', task_id)
        return self._send_xml_command(cmd)

    def create_user(self, name, password=None, hosts=None, hosts_allow=False,
                    ifaces=None, ifaces_allow=False, role_ids=None):
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
            raise RequiredArgument('create_user requires a name argument')

        cmd = XmlCommand('create_user')
        cmd.add_element('name', name)

        if password:
            cmd.add_element('password', password)

        if hosts:
            cmd.add_element('hosts', ', '.join(hosts),
                            attrs={'allow': '1' if hosts_allow else '0'})

        if ifaces:
            cmd.add_element('ifaces', ', '.join(ifaces),
                            attrs={'allow': '1' if ifaces_allow else '0'})

        if role_ids:
            for role in role_ids:
                cmd.add_element('role', attrs={'id': role})

        return self._send_xml_command(cmd)

    def clone_user(self, user_id):
        """Clone an existing user

        Arguments:
            user_id (str): UUID of existing user to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('create_user')
        cmd.add_element('copy', user_id)
        return self._send_xml_command(cmd)

    def delete_agent(self, **kwargs):
        cmd = self._generator.delete_agent_command(kwargs)
        return self.send_command(cmd)

    def delete_alert(self, **kwargs):
        cmd = self._generator.delete_alert_command(kwargs)
        return self.send_command(cmd)

    def delete_asset(self, asset_id, ultimate=0):
        cmd = self._generator.delete_asset_command(asset_id, ultimate)
        return self.send_command(cmd)

    def delete_config(self, config_id, ultimate=0):
        cmd = self._generator.delete_config_command(config_id, ultimate)
        return self.send_command(cmd)

    def delete_credential(self, credential_id, ultimate=0):
        cmd = self._generator.delete_credential_command(credential_id, ultimate)
        return self.send_command(cmd)

    def delete_filter(self, filter_id, ultimate=0):
        cmd = self._generator.delete_filter_command(filter_id, ultimate)
        return self.send_command(cmd)

    def delete_group(self, group_id, ultimate=0):
        cmd = self._generator.delete_group_command(group_id, ultimate)
        return self.send_command(cmd)

    def delete_note(self, note_id, ultimate=0):
        cmd = self._generator.delete_note_command(note_id, ultimate)
        return self.send_command(cmd)

    def delete_override(self, override_id, ultimate=0):
        cmd = self._generator.delete_override_command(override_id, ultimate)
        return self.send_command(cmd)

    def delete_permission(self, permission_id, ultimate=0):
        cmd = self._generator.delete_permission_command(permission_id, ultimate)
        return self.send_command(cmd)

    def delete_port_list(self, port_list_id, ultimate=0):
        cmd = self._generator.delete_port_list_command(port_list_id, ultimate)
        return self.send_command(cmd)

    def delete_port_range(self, port_range_id):
        cmd = self._generator.delete_port_range_command(port_range_id)
        return self.send_command(cmd)

    def delete_report(self, report_id):
        cmd = self._generator.delete_report_command(report_id)
        return self.send_command(cmd)

    def delete_report_format(self, report_format_id, ultimate=0):
        cmd = self._generator.delete_report_format_command(
            report_format_id, ultimate)
        return self.send_command(cmd)

    def delete_role(self, role_id, ultimate=0):
        cmd = self._generator.delete_role_command(role_id, ultimate)
        return self.send_command(cmd)

    def delete_scanner(self, scanner_id, ultimate=0):
        cmd = self._generator.delete_scanner_command(scanner_id, ultimate)
        return self.send_command(cmd)

    def delete_schedule(self, schedule_id, ultimate=0):
        cmd = self._generator.delete_schedule_command(schedule_id, ultimate)
        return self.send_command(cmd)

    def delete_tag(self, tag_id, ultimate=0):
        cmd = self._generator.delete_tag_command(tag_id, ultimate)
        return self.send_command(cmd)

    def delete_target(self, target_id, ultimate=0):
        cmd = self._generator.delete_target_command(target_id, ultimate)
        return self.send_command(cmd)

    def delete_task(self, task_id, ultimate=0):
        cmd = self._generator.delete_task_command(task_id, ultimate)
        return self.send_command(cmd)

    def delete_user(self, **kwargs):
        cmd = self._generator.delete_user_command(kwargs)
        return self.send_command(cmd)

    def describe_auth(self):
        cmd = self._generator.describe_auth_command()
        return self.send_command(cmd)

    def empty_trashcan(self):
        cmd = self._generator.empty_trashcan_command()
        return self.send_command(cmd)

    def get_agents(self, filter=None, filter_id=None, trash=None, details=None,
                   format=None):
        """Request a list of agents

        Arguments:
            filter (str, optional): Filter term to use for the query
            filter_id (str, optional): UUID of an existing filter to use for
                the query
            trash (boolean, optional): True to request the filters in the
                trashcan
            details (boolean, optional): Whether to include agents package
                information when no format was provided
            format (str, optional): One of "installer", "howto_install" or
                "howto_use"

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_agents')

        if filter:
            cmd.set_attribute('filter', filter)

        if filter_id:
            cmd.set_attribute('filt_id', filter_id)

        if not trash is None:
            cmd.set_attribute('trash', _to_bool(trash))

        if not details is None:
            cmd.set_attribute('details', _to_bool(details))

        if format:
            if not format in ('installer', 'howto_install', 'howto_use'):
                raise InvalidArgument(
                    'installer argument needs to be one of installer, '
                    'howto_install or howto_use')

            cmd.set_attribute('format', format)

        return self._send_xml_command(cmd)

    def get_agent(self, agent_id):
        """Request a single agent

        Arguments:
            agent_id (str): UUID of an existing agent

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_agents')
        cmd.set_attribute('agent_id', agent_id)
        return self._send_xml_command(cmd)

    def get_aggregates(self, **kwargs):
        cmd = XmlCommand('get_aggregates')
        cmd.set_attributes(kwargs)
        return self._send_xml_command(cmd)

    def get_alerts(self, filter=None, filter_id=None, trash=None, tasks=None):
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
        cmd = XmlCommand('get_alerts')

        if filter:
            cmd.set_attribute('filter', filter)

        if filter_id:
            cmd.set_attribute('filt_id', filter_id)

        if not trash is None:
            cmd.set_attribute('trash', _to_bool(trash))

        if not tasks is None:
            cmd.set_attribute('tasks', _to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_alert(self, alert_id):
        """Request a single alert

        Arguments:
            alert_id (str): UUID of an existing alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_alerts')
        cmd.set_attribute('alert_id', alert_id)
        return self._send_xml_command(cmd)

    def get_assets(self, **kwargs):
        cmd = self._generator.get_assets_command(kwargs)
        return self.send_command(cmd)

    def get_asset(self, asset_id):
        """Request a single asset

        Arguments:
            asset_id (str): UUID of an existing asset

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_assets')
        cmd.set_attribute('asset_id', asset_id)
        return self._send_xml_command(cmd)

    def get_credentials(self, **kwargs):
        cmd = self._generator.get_credentials_command(kwargs)
        return self.send_command(cmd)

    def get_credential(self, credential_id):
        """Request a single credential

        Arguments:
            credential_id (str): UUID of an existing credential

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_credentials')
        cmd.set_attribute('credential_id', credential_id)
        return self._send_xml_command(cmd)

    def get_configs(self, **kwargs):
        cmd = self._generator.get_configs_command(kwargs)
        return self.send_command(cmd)

    def get_config(self, config_id):
        """Request a single scan config

        Arguments:
            config_id (str): UUID of an existing scan config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_configs')
        cmd.set_attribute('config_id', config_id)
        return self._send_xml_command(cmd)

    def get_feeds(self, **kwargs):
        cmd = self._generator.get_feeds_command(kwargs)
        return self.send_command(cmd)

    def get_filters(self, **kwargs):
        cmd = self._generator.get_filters_command(kwargs)
        return self.send_command(cmd)

    def get_filter(self, filter_id):
        """Request a single filter

        Arguments:
            filter_id (str): UUID of an existing filter

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_filters')
        cmd.set_attribute('filter_id', filter_id)
        return self._send_xml_command(cmd)

    def get_groups(self, **kwargs):
        cmd = self._generator.get_groups_command(kwargs)
        return self.send_command(cmd)

    def get_group(self, group_id):
        """Request a single group

        Arguments:
            group_id (str): UUID of an existing group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_groups')
        cmd.set_attribute('group_id', group_id)
        return self._send_xml_command(cmd)

    def get_info_list(self, **kwargs):
        cmd = self._generator.get_info_command(kwargs)
        return self.send_command(cmd)

    def get_info(self, info_id):
        """Request a single secinfo

        Arguments:
            info_id (str): UUID of an existing secinfo

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_infos')
        cmd.set_attribute('info_id', info_id)
        return self._send_xml_command(cmd)

    def get_notes(self, **kwargs):
        cmd = self._generator.get_notes_command(kwargs)
        return self.send_command(cmd)

    def get_note(self, note_id):
        """Request a single note

        Arguments:
            note_id (str): UUID of an existing note

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_notes')
        cmd.set_attribute('note_id', note_id)
        return self._send_xml_command(cmd)

    def get_nvts(self, **kwargs):
        cmd = self._generator.get_nvts_command(kwargs)
        return self.send_command(cmd)

    def get_nvt(self, nvt_id):
        """Request a single nvt

        Arguments:
            nvt_id (str): UUID of an existing nvt

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_nvts')
        cmd.set_attribute('nvt_id', nvt_id)
        return self._send_xml_command(cmd)

    def get_nvt_families(self, **kwargs):
        cmd = self._generator.get_nvt_families_command(kwargs)
        return self.send_command(cmd)

    def get_overrides(self, **kwargs):
        cmd = self._generator.get_overrides_command(kwargs)
        return self.send_command(cmd)

    def get_override(self, override_id):
        """Request a single override

        Arguments:
            override_id (str): UUID of an existing override

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_overrides')
        cmd.set_attribute('override_id', override_id)
        return self._send_xml_command(cmd)

    def get_permissions(self, **kwargs):
        cmd = self._generator.get_permissions_command(kwargs)
        return self.send_command(cmd)

    def get_permission(self, permission_id):
        """Request a single permission

        Arguments:
            permission_id (str): UUID of an existing permission

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_permissions')
        cmd.set_attribute('permission_id', permission_id)
        return self._send_xml_command(cmd)

    def get_port_lists(self, **kwargs):
        cmd = self._generator.get_port_lists_command(kwargs)
        return self.send_command(cmd)

    def get_port_list(self, port_list_id):
        """Request a single port list

        Arguments:
            port_list_id (str): UUID of an existing port list

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_port_lists')
        cmd.set_attribute('port_list_id', port_list_id)
        return self._send_xml_command(cmd)

    def get_preferences(self, **kwargs):
        cmd = self._generator.get_preferences_command(kwargs)
        return self.send_command(cmd)

    def get_reports(self, **kwargs):
        cmd = self._generator.get_reports_command(kwargs)
        return self.send_command(cmd)

    def get_report(self, report_id):
        """Request a single report

        Arguments:
            report_id (str): UUID of an existing report

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_reports')
        cmd.set_attribute('report_id', report_id)
        return self._send_xml_command(cmd)

    def get_report_formats(self, **kwargs):
        cmd = self._generator.get_report_formats_command(kwargs)
        return self.send_command(cmd)

    def get_report_format(self, report_format_id):
        """Request a single report format

        Arguments:
            report_format_id (str): UUID of an existing report format

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_report_formats')
        cmd.set_attribute('report_format_id', report_format_id)
        return self._send_xml_command(cmd)

    def get_results(self, **kwargs):
        cmd = self._generator.get_results_command(kwargs)
        return self.send_command(cmd)

    def get_result(self, result_id):
        """Request a single result

        Arguments:
            result_id (str): UUID of an existing result

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_results')
        cmd.set_attribute('result_id', result_id)
        return self._send_xml_command(cmd)

    def get_roles(self, **kwargs):
        cmd = self._generator.get_roles_command(kwargs)
        return self.send_command(cmd)

    def get_role(self, role_id):
        """Request a single role

        Arguments:
            role_id (str): UUID of an existing role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_roles')
        cmd.set_attribute('role_id', role_id)
        return self._send_xml_command(cmd)

    def get_scanners(self, **kwargs):
        cmd = self._generator.get_scanners_command(kwargs)
        return self.send_command(cmd)

    def get_scanner(self, scanner_id):
        """Request a single scanner

        Arguments:
            scanner_id (str): UUID of an existing scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_scanners')
        cmd.set_attribute('scanner_id', scanner_id)
        return self._send_xml_command(cmd)

    def get_schedules(self, **kwargs):
        cmd = self._generator.get_schedules_command(kwargs)
        return self.send_command(cmd)

    def get_schedule(self, schedule_id):
        """Request a single schedule

        Arguments:
            schedule_id (str): UUID of an existing schedule

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_schedules')
        cmd.set_attribute('schedule_id', schedule_id)
        return self._send_xml_command(cmd)

    def get_settings(self, **kwargs):
        cmd = self._generator.get_settings_command(kwargs)
        return self.send_command(cmd)

    def get_setting(self, setting_id):
        """Request a single setting

        Arguments:
            setting_id (str): UUID of an existing setting

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_settings')
        cmd.set_attribute('setting_id', setting_id)
        return self._send_xml_command(cmd)

    def get_system_reports(self, **kwargs):
        cmd = self._generator.get_system_reports_command(kwargs)
        return self.send_command(cmd)

    def get_tags(self, **kwargs):
        cmd = self._generator.get_tags_command(kwargs)
        return self.send_command(cmd)

    def get_tag(self, tag_id):
        """Request a single tag

        Arguments:
            tag_id (str): UUID of an existing tag

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_tags')
        cmd.set_attribute('tag_id', tag_id)
        return self._send_xml_command(cmd)

    def get_targets(self, **kwargs):
        cmd = self._generator.get_targets_command(kwargs)
        return self.send_command(cmd)

    def get_target(self, target_id):
        """Request a single target

        Arguments:
            target_id (str): UUID of an existing target

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_targets')
        cmd.set_attribute('target_id', target_id)
        return self._send_xml_command(cmd)

    def get_tasks(self, **kwargs):
        cmd = self._generator.get_tasks_command(kwargs)
        return self.send_command(cmd)

    def get_task(self, task_id):
        """Request a single task

        Arguments:
            task_id (str): UUID of an existing task

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_tasks')
        cmd.set_attribute('task_id', task_id)
        return self._send_xml_command(cmd)

    def get_users(self, **kwargs):
        cmd = self._generator.get_users_command(kwargs)
        return self.send_command(cmd)

    def get_user(self, user_id):
        """Request a single user

        Arguments:
            user_id (str): UUID of an existing user

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand('get_users')
        cmd.set_attribute('user_id', user_id)
        return self._send_xml_command(cmd)

    def get_version(self):
        cmd = self._generator.get_version_command()
        return self.send_command(cmd)

    def help(self, **kwargs):
        cmd = self._generator.help_command(kwargs)
        return self.send_command(cmd)

    def modify_agent(self, agent_id, name=None, comment=None):
        """Modifies an existing agent

        Arguments:
            agent_id (str) UUID of the agent to be modified.
            name (str, optional): Name of the new credential
            comment (str, optional): Comment for the credential
        """
        if not agent_id:
            raise RequiredArgument('modify_agent requires agent_id argument')

        cmd = XmlCommand('modify_agent')
        cmd.set_attribute('agent_id', str(agent_id))
        if name:
            cmd.add_element('name', name)
        if comment:
            cmd.add_element('comment', comment)

        return self._send_xml_command(cmd)

    def modify_alert(self, alert_id, name=None, comment=None,
                     filter_id=None, event=None, event_data=None,
                     condition=None, condition_data=None, method=None,
                     method_data=None):
        """Modifies an existing alert.

        Arguments:
            alert_id (str) UUID of the alert to be modified.
            name (str, optional): Name of the Alert.
            condition (str, optional): The condition that must be satisfied
                for the alert to occur.
            condition_data (dict, optional): Data that defines the condition
            event (str, optional): The event that must happen for the alert
               to occur.
            event_data (dict, optional): Data that defines the event
            method (str, optional): The method by which the user is alerted
            method_data (dict, optional): Data that defines the method
            filter_id (str, optional): Filter to apply when executing alert
            comment (str, optional): Comment for the alert
        """

        if not alert_id:
            raise RequiredArgument('modify_alert requires an alert_id argument')

        cmd = XmlCommand('modify_alert')
        cmd.set_attribute('alert_id', str(alert_id))

        if name:
            cmd.add_element('name', name)

        if comment:
            cmd.add_element('comment', comment)

        if filter_id:
            cmd.add_element('filter', attrs={'id': filter_id})

        conditions = cmd.add_element('condition', condition)

        if not condition_data is None:
            for value, key in condition_data.items():
                _data = conditions.add_element('data', value)
                _data.add_element('name', key)

        events = cmd.add_element('event', event)

        if not event_data is None:
            for value, key in event_data.items():
                _data = events.add_element('data', value)
                _data.add_element('name', key)

        methods = cmd.add_element('method', method)

        if not method_data is None:
            for value, key in method_data.items():
                _data = methods.add_element('data', value)
                _data.add_element('name', key)

        return self._send_xml_command(cmd)

    def modify_asset(self, asset_id, comment):
        """Modifies an existing asset.

        Arguments:
            asset_id (str) UUID of the asset to be modified.
            comment (str, optional): Comment for the asset.
        """
        if not asset_id:
            raise RequiredArgument('modify_asset requires an asset_id argument')

        cmd = XmlCommand('modify_asset')
        cmd.set_attribute('asset_id', asset_id)
        cmd.add_element('comment', comment)

        return self._send_xml_command(cmd)

    def modify_auth(self, group_name, auth_conf_settings):
        """Modifies an existing auth.
        Arguments:
            group_name (str) Name of the group to be modified.
            auth_conf_settings (dict): The new auth config.
        """
        if not group_name:
            raise RequiredArgument('modify_auth requires a group_name argument')
        if not auth_conf_settings:
            raise RequiredArgument('modify_auth requires an '
                                   'auth_conf_settings argument')
        cmd = XmlCommand('modify_auth')
        _xmlgroup = cmd.add_element('group', attrs={'name': str(group_name)})

        for key, value in auth_conf_settings.items():
            _xmlauthconf = _xmlgroup.add_element('auth_conf_setting')
            _xmlauthconf.add_element('key', key)
            _xmlauthconf.add_element('value', value)

        return self._send_xml_command(cmd)

    def modify_config(self, selection, config_id=None, nvt_oids=None, name=None,
                      value=None, family=None):
        """Modifies an existing existing scan config.

        Arguments:
            selection (str): one of 'nvt_pref', nvt_selection or
                family_selection'
            config_id (str, optional): UUID of scan config to modify.
            name (str, optional): New name for preference.
            value(str, optional): New value for preference.
            nvt_oids (list, optional): List of NVTs associated with preference
                to modify.
            family (str,optional): Name of family to modify.
        """
        if selection not in ('nvt_pref', 'scan_pref',
                             'family_selection', 'nvt_selection'):
            raise InvalidArgument('selection must be one of nvt_pref, '
                                  'scan_pref, family_selection or '
                                  'nvt_selection')

        cmd = XmlCommand('modify_config')
        cmd.set_attribute('config_id', str(config_id))

        if selection == 'nvt_pref':
            _xmlpref = cmd.add_element('preference')
            if not nvt_oids:
                raise InvalidArgument('modify_config requires a nvt_oids '
                                      'argument')
            _xmlpref.add_element('nvt', attrs={'oid': nvt_oids[0]})
            _xmlpref.add_element('name', name)
            _xmlpref.add_element('value', value)

        elif selection == 'nvt_selection':
            _xmlnvtsel = cmd.add_element('nvt_selection')
            _xmlnvtsel.add_element('family', family)

            if nvt_oids:
                for nvt in nvt_oids:
                    _xmlnvtsel.add_element('nvt', attrs={'oid': nvt})
            else:
                raise InvalidArgument('modify_config requires a nvt_oid '
                                      'argument')

        elif selection == 'family_selection':
            _xmlfamsel = cmd.add_element('family_selection')
            _xmlfamsel.add_element('growing', '1')
            _xmlfamily = _xmlfamsel.add_element('family')
            _xmlfamily.add_element('name', family)
            _xmlfamily.add_element('all', '1')
            _xmlfamily.add_element('growing', '1')

        return self._send_xml_command(cmd)

    def modify_credential(self, credential_id, name=None, comment=None,
                          allow_insecure=None, certificate=None,
                          key_phrase=None, private_key=None, login=None,
                          password=None, auth_algorithm=None, community=None,
                          privacy_algorithm=None, privacy_password=None,
                          credential_type=None):
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
                'snmp', 'up', 'usk'
        """
        if not credential_id:
            raise RequiredArgument('modify_credential requires '
                                   'a credential_id attribute')

        cmd = XmlCommand('modify_credential')
        cmd.set_attribute('credential_id', credential_id)

        if comment:
            cmd.add_element('comment', comment)

        if name:
            cmd.add_element('name', name)

        if allow_insecure:
            cmd.add_element('allow_insecure', allow_insecure)

        if certificate:
            cmd.add_element('certificate', certificate)

        if key_phrase or private_key:
            if not key_phrase or not private_key:
                raise RequiredArgument('modify_credential requires '
                                       'a key_phrase and private_key arguments')
            _xmlkey = cmd.add_element('key')
            _xmlkey.add_element('phrase', key_phrase)
            _xmlkey.add_element('private', private_key)

        if login:
            cmd.add_element('login', login)

        if password:
            cmd.add_element('password', password)

        if auth_algorithm:
            if auth_algorithm not in ('md5', 'sha1'):
                raise RequiredArgument('modify_credential requires '
                                       'auth_algorithm to be either '
                                       'md5 or sha1')
            cmd.add_element('auth_algorithm', auth_algorithm)

        if community:
            cmd.add_element('community', community)

        if privacy_algorithm:
            if privacy_algorithm not in ('aes', 'des'):
                raise RequiredArgument('modify_credential requires '
                                       'privacy_algorithm to be either'
                                       'aes or des')
            _xmlprivacy = cmd.add_element('privacy')
            _xmlprivacy.add_element('algorithm', privacy_algorithm)
            _xmlprivacy.add_element('password', privacy_password)

        if credential_type:
            if credential_type not in ('cc', 'snmp', 'up', 'usk'):
                raise RequiredArgument('modify_credential requires type '
                                       'to be either cc, snmp, up or usk')
            cmd.add_element('type', credential_type)

        return self._send_xml_command(cmd)

    def modify_filter(self, filter_id, comment=None, name=None, term=None,
                      filter_type=None):
        """Modifies an existing filter.

        Arguments:
            filter_id (str): UUID of the filter to be modified
            comment (str, optional): Comment on filter.
            name (str, optional): Name of filter.
            term (str, optional): Filter term.
            filter_type (str, optional): Resource type filter applies to.
        """
        if not filter_id:
            raise RequiredArgument('modify_filter requires a filter_id '
                                   'attribute')

        cmd = XmlCommand('modify_filter')
        cmd.set_attribute('filter_id', filter_id)

        if comment:
            cmd.add_element('comment', comment)

        if name:
            cmd.add_element('name', name)

        if term:
            cmd.add_element('term', term)

        if filter_type:
            filter_type = filter_type.lower()
            if filter_type not in FILTER_TYPES:
                raise InvalidArgument(
                    'modify_filter requires type to be one of {0} but '
                    'was {1}'.format(', '.join(FILTER_TYPES), filter_type))
            cmd.add_element('type', filter_type)

        return self._send_xml_command(cmd)

    def modify_group(self, group_id, comment=None, name=None,
                     users=None):
        """Modifies an existing group.

        Arguments:
            group_id (str): UUID of group to modify.
            comment (str, optional): Comment on group.
            name (str, optional): Name of group.
            users (list, optional): List of user names to be in the group
        """
        if not group_id:
            raise RequiredArgument('modify_group requires a group_id argument')

        cmd = XmlCommand('modify_group')
        cmd.set_attribute('group_id', group_id)

        if comment:
            cmd.add_element('comment', comment)

        if name:
            cmd.add_element('name', name)

        if users:
            cmd.add_element('users', ','.join(users))

        return self._send_xml_command(cmd)

    def modify_note(self, note_id, text, seconds_active=None, hosts=None,
                    port=None, result_id=None, severity=None, task_id=None,
                    threat=None):
        """Modifies an existing note.

        Arguments:
            note_id (str): UUID of note to modify.
            text (str): The text of the note.
            seconds_active (int, optional): Seconds note will be active.
                -1 on always, 0 off.
            hosts (list, optional): A list of hosts addresses
            port (str, optional): Port to which note applies.
            result_id (str, optional): Result to which note applies.
            severity (str, optional): Severity to which note applies.
            task_id (str, optional): Task to which note applies.
            threat (str, optional): Threat level to which note applies.
        """
        if not note_id:
            raise RequiredArgument('modify_note requires a note_id attribute')
        if not text:
            raise RequiredArgument('modify_note requires a text element')

        cmd = XmlCommand('modify_note')
        cmd.set_attribute('note_id', note_id)
        cmd.add_element('text', text)

        if not seconds_active is None:
            cmd.add_element('active', str(seconds_active))

        if hosts:
            cmd.add_element('hosts', ', '.join(hosts))

        if port:
            cmd.add_element('port', port)

        if result_id:
            cmd.add_element('result', attrs={'id': result_id})

        if severity:
            cmd.add_element('severity', severity)

        if task_id:
            cmd.add_element('task', attrs={'id': task_id})

        if threat:
            cmd.add_element('threat', threat)

        return self._send_xml_command(cmd)

    def modify_override(self, override_id, text, seconds_active=None,
                        hosts=None, port=None, result_id=None, severity=None,
                        new_severity=None, task_id=None, threat=None,
                        new_threat=None):
        """Modifies an existing override.

        Arguments:
            override_id (str): UUID of override to modify.
            text (str): The text of the override.
            seconds_active (int, optional): Seconds override will be active.
                -1 on always, 0 off.
            hosts (list, optional): A list of host addresses
            port (str, optional): Port to which override applies.
            result_id (str, optional): Result to which override applies.
            severity (str, optional): Severity to which override applies.
            new_severity (str, optional): New severity score for result.
            task_id (str, optional): Task to which override applies.
            threat (str, optional): Threat level to which override applies.
            new_threat (str, optional): New threat level for results.
        """
        if not override_id:
            raise RequiredArgument('modify_override requires a override_id '
                                   'argument')
        if not text:
            raise RequiredArgument('modify_override requires a text argument')

        cmd = XmlCommand('modify_override')
        cmd.set_attribute('override_id', override_id)
        cmd.add_element('text', text)

        if not seconds_active is None:
            cmd.add_element('active', str(seconds_active))

        if hosts:
            cmd.add_element('hosts', ', '.join(hosts))

        if port:
            cmd.add_element('port', port)

        if result_id:
            cmd.add_element('result', attrs={'id': result_id})

        if severity:
            cmd.add_element('severity', severity)

        if new_severity:
            cmd.add_element('new_severity', new_severity)

        if task_id:
            cmd.add_element('task', attrs={'id': task_id})

        if threat:
            cmd.add_element('threat', threat)

        if new_threat:
            cmd.add_element('new_threat', new_threat)

        return self._send_xml_command(cmd)

    def modify_permission(self, permission_id, comment=None, name=None,
                          resource_id=None, resource_type=None,
                          subject_id=None, subject_type=None):
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
        """
        if not permission_id:
            raise RequiredArgument('modify_permission requires '
                                   'a permission_id element')

        cmd = XmlCommand('modify_permission')
        cmd.set_attribute('permission_id', permission_id)

        if comment:
            cmd.add_element('comment', comment)

        if name:
            cmd.add_element('name', name)

        if resource_id and resource_type:
            _xmlresource = cmd.add_element('resource',
                                           attrs={'id': resource_id})
            _xmlresource.add_element('type', resource_type)

        if subject_id and subject_type:
            _xmlsubject = cmd.add_element('subject',
                                           attrs={'id': subject_id})
            _xmlsubject.add_element('type', subject_type)

        return self._send_xml_command(cmd)

    def modify_port_list(self, port_list_id, comment=None, name=None, ):
        """Modifies an existing port list.

        Arguments:
            port_list_id (str): UUID of port list to modify.
            name (str, optional): Name of port list.
            comment (str, optional): Comment on port list.
        """
        if not port_list_id:
            raise RequiredArgument('modify_port_list requires '
                                   'a port_list_id attribute')
        cmd = XmlCommand('modify_port_list')
        cmd.set_attribute('port_list_id', port_list_id)

        if comment:
            cmd.add_element('comment', comment)

        if name:
            cmd.add_element('name', name)

        return self._send_xml_command(cmd)

    def modify_report(self, report_id, comment):
        """Modifies an existing report.

        Arguments:
            report_id (str): UUID of report to modify.
            comment (str): The comment on the report.
        """
        if not report_id:
            raise RequiredArgument('modify_report requires '
                                   'a report_id attribute')
        if not comment:
            raise RequiredArgument('modify_report requires '
                                   'a comment attribute')
        cmd = XmlCommand('modify_report')
        cmd.set_attribute('report_id', report_id)
        cmd.add_element('comment', comment)

        return self._send_xml_command(cmd)

    def modify_report_format(self, report_format_id, active=None, name=None,
                             summary=None, param_name=None, param_value=None):
        """Modifies an existing report format on gvmd.

        Arguments:
            report_format_id (str) UUID of report format to modify.
            active (boolean, optional): Whether the report format is active.
            name (str, optional): The name of the report format.
            summary (str, optional): A summary of the report format.
            param_name (str, optional): The name of the param.
            param_value (str, optional): The value of the param.
        """
        if not report_format_id:
            raise RequiredArgument('modify_report requires '
                                   'a report_format_id attribute')
        cmd = XmlCommand('modify_report_format')
        cmd.set_attribute('report_format_id', report_format_id)

        if not active is None:
            cmd.add_element('active', '1' if active else '0')

        if name:
            cmd.add_element('name', name)

        if summary:
            cmd.add_element('summary', summary)

        if param_name and param_value:
            _xmlparam = cmd.add_element('param')
            _xmlparam.add_element('name', param_name)
            _xmlparam.add_element('value', param_value)

        return self._send_xml_command(cmd)

    def modify_role(self, role_id, comment=None, name=None, users=None):
        """Modifies an existing role.

        Arguments:
            role_id (str): UUID of role to modify.
            comment (str, optional): Name of role.
            name (str, optional): Comment on role.
            users  (list, optional): List of user names.
        """
        if not role_id:
            raise RequiredArgument('modify_role requires a role_id argument')

        cmd = XmlCommand('modify_role')
        cmd.set_attribute('role_id', role_id)

        if comment:
            cmd.add_element('comment', comment)

        if name:
            cmd.add_element('name', name)

        if users:
            cmd.add_element('users', ",".join(users))

        return self._send_xml_command(cmd)

    def modify_scanner(self, scanner_id, host, port, scanner_type, **kwargs):
        cmd = self._generator.modify_scanner_command(scanner_id, host, port,
                                                     scanner_type, kwargs)
        return self.send_command(cmd)

    def modify_schedule(self, schedule_id, **kwargs):
        cmd = self._generator.modify_schedule_command(schedule_id, kwargs)
        return self.send_command(cmd)

    def modify_setting(self, setting_id, name, value):
        cmd = self._generator.modify_setting_command(setting_id, name, value)
        return self.send_command(cmd)

    def modify_tag(self, tag_id, **kwargs):
        cmd = self._generator.modify_tag_command(tag_id, kwargs)
        return self.send_command(cmd)

    def modify_target(self, target_id, **kwargs):
        cmd = self._generator.modify_target_command(target_id, kwargs)
        return self.send_command(cmd)

    def modify_task(self, task_id, **kwargs):
        cmd = self._generator.modify_task_command(task_id, kwargs)
        return self.send_command(cmd)

    def modify_user(self, **kwargs):
        cmd = self._generator.modify_user_command(kwargs)
        return self.send_command(cmd)

    def move_task(self, task_id, slave_id):
        cmd = self._generator.move_task_command(task_id, slave_id)
        return self.send_command(cmd)

    def restore(self, entity_id):
        cmd = self._generator.restore_command(entity_id)
        return self.send_command(cmd)

    def resume_task(self, task_id):
        cmd = self._generator.resume_task_command(task_id)
        return self.send_command(cmd)

    def start_task(self, task_id):
        cmd = self._generator.start_task_command(task_id)
        return self.send_command(cmd)

    def stop_task(self, task_id):
        cmd = self._generator.stop_task_command(task_id)
        return self.send_command(cmd)

    def sync_cert(self):
        cmd = self._generator.sync_cert_command()
        return self.send_command(cmd)

    def sync_config(self):
        cmd = self._generator.sync_config_command()
        return self.send_command(cmd)

    def sync_feed(self):
        cmd = self._generator.sync_feed_command()
        return self.send_command(cmd)

    def sync_scap(self):
        cmd = self._generator.sync_scap_command()
        return self.send_command(cmd)

    def test_alert(self, alert_id):
        cmd = self._generator.test_alert_command(alert_id)
        return self.send_command(cmd)

    def verify_agent(self, agent_id):
        cmd = self._generator.verify_agent_command(agent_id)
        return self.send_command(cmd)

    def verify_report_format(self, report_format_id):
        cmd = self._generator.verify_report_format_command(report_format_id)
        return self.send_command(cmd)

    def verify_scanner(self, scanner_id):
        cmd = self._generator.verify_scanner_command(scanner_id)
        return self.send_command(cmd)
