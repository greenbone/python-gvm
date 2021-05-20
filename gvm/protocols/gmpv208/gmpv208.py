# -*- coding: utf-8 -*-
# Copyright (C) 2018-2021 Greenbone Networks GmbH
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
Module for communication with gvmd in
`Greenbone Management Protocol version 20.08`_

.. _Greenbone Management Protocol version 20.08:
    https://docs.greenbone.net/API/GMP/gmp-20.08.html
"""
import logging
from numbers import Integral

from typing import Any, List, Optional, Callable, Union
from lxml import etree

from gvm.connections import GvmConnection
from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.protocols.base import GvmProtocol
from gvm.protocols.gmpv208.entities.report_formats import (
    ReportFormatType,
)
from gvm.protocols.gmpv208.entities.tickets import TicketStatus

from gvm.utils import (
    check_command_status,
    to_base64,
    to_bool,
    to_comma_list,
    add_filter,
)
from gvm.xml import XmlCommand

PROTOCOL_VERSION = (20, 8)


logger = logging.getLogger(__name__)


class GmpV208Mixin(GvmProtocol):
    """Python interface for Greenbone Management Protocol

    This class implements the `Greenbone Management Protocol version 20.08`_

    Arguments:
        connection: Connection to use to talk with the gvmd daemon. See
            :mod:`gvm.connections` for possible connection types.
        transform: Optional transform `callable`_ to convert response data.
            After each request the callable gets passed the plain response data
            which can be used to check the data and/or conversion into different
            representations like a xml dom.

            See :mod:`gvm.transforms` for existing transforms.

    .. _Greenbone Management Protocol version 20.08:
        https://docs.greenbone.net/API/GMP/gmp-20.08.html
    .. _callable:
        https://docs.python.org/3/library/functions.html#callable
    """

    def __init__(
        self,
        connection: GvmConnection,
        *,
        transform: Optional[Callable[[str], Any]] = None,
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

        if check_command_status(response):
            self._authenticated = True

        return self._transform(response)

    def clone_ticket(self, ticket_id: str) -> Any:
        """Clone an existing ticket

        Arguments:
            ticket_id: UUID of an existing ticket to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not ticket_id:
            raise RequiredArgument(
                function=self.clone_ticket.__name__, argument='ticket_id'
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
        comment: Optional[str] = None,
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
                function=self.create_ticket.__name__, argument='result_id'
            )

        if not assigned_to_user_id:
            raise RequiredArgument(
                function=self.create_ticket.__name__,
                argument='assigned_to_user_id',
            )

        if not note:
            raise RequiredArgument(
                function=self.create_ticket.__name__, argument='note'
            )

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
                function=self.delete_ticket.__name__, argument='ticket_id'
            )

        cmd = XmlCommand("delete_ticket")
        cmd.set_attribute("ticket_id", ticket_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_tickets(
        self,
        *,
        trash: Optional[bool] = None,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
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

        add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_ticket(self, ticket_id: str) -> Any:
        """Request a single ticket

        Arguments:
            ticket_id: UUID of an existing ticket

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not ticket_id:
            raise RequiredArgument(
                function=self.get_ticket.__name__, argument='ticket_id'
            )

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

        add_filter(cmd, filter, filter_id)

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
                function=self.get_vulnerability.__name__,
                argument='vulnerability_id',
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
        comment: Optional[str] = None,
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
                function=self.modify_ticket.__name__, argument='ticket_id'
            )

        if status and not note:
            raise RequiredArgument(
                function=self.modify_ticket.__name__, argument='note'
            )

        if note and not status:
            raise RequiredArgument(
                function=self.modify_ticket.__name__, argument='status'
            )

        cmd = XmlCommand("modify_ticket")
        cmd.set_attribute("ticket_id", ticket_id)

        if assigned_to_user_id:
            _assigned = cmd.add_element("assigned_to")
            _user = _assigned.add_element("user")
            _user.set_attribute("id", assigned_to_user_id)

        if status:
            if not isinstance(status, TicketStatus):
                raise InvalidArgumentType(
                    function=self.modify_ticket.__name__,
                    argument='status',
                    arg_type=TicketStatus.__name__,
                )

            cmd.add_element('status', status.value)
            cmd.add_element('{}_note'.format(status.name.lower()), note)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def create_group(
        self,
        name: str,
        *,
        comment: Optional[str] = None,
        special: Optional[bool] = False,
        users: Optional[List[str]] = None,
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
            cmd.add_element("users", to_comma_list(users))

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

    def clone_report_format(
        self, report_format_id: [Union[str, ReportFormatType]]
    ) -> Any:
        """Clone a report format from an existing one

        Arguments:
            report_format_id: UUID of the existing report format
                              or ReportFormatType (enum)

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.clone_report_format.__name__,
                argument='report_format_id',
            )

        cmd = XmlCommand("create_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.add_element("copy", report_format_id)
        return self._send_xml_command(cmd)

    def import_report_format(self, report_format: str) -> Any:
        """Import a report format from XML

        Arguments:
            report_format: Report format XML as string to import. This XML must
                contain a :code:`<get_report_formats_response>` root element.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format:
            raise RequiredArgument(
                function=self.import_report_format.__name__,
                argument='report_format',
            )

        cmd = XmlCommand("create_report_format")

        try:
            cmd.append_xml_str(report_format)
        except etree.XMLSyntaxError as e:
            raise InvalidArgument(
                function=self.import_report_format.__name__,
                argument='report_format',
            ) from e

        return self._send_xml_command(cmd)

    def create_role(
        self,
        name: str,
        *,
        comment: Optional[str] = None,
        users: Optional[List[str]] = None,
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
            cmd.add_element("users", to_comma_list(users))

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
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_report_format(
        self,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        *,
        ultimate: Optional[bool] = False,
    ) -> Any:
        """Deletes an existing report format

        Arguments:
            report_format_id: UUID of the report format to be deleted.
                              or ReportFormatType (enum)
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.delete_report_format.__name__,
                argument='report_format_id',
            )

        cmd = XmlCommand("delete_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        cmd.set_attribute("ultimate", to_bool(ultimate))

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
        cmd.set_attribute("ultimate", to_bool(ultimate))

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

    def get_groups(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
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

        add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_group(self, group_id: str) -> Any:
        """Request a single group

        Arguments:
            group_id: UUID of an existing group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_groups")

        if not group_id:
            raise RequiredArgument(
                function=self.get_group.__name__, argument='group_id'
            )

        cmd.set_attribute("group_id", group_id)
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

    def get_preference(
        self,
        name: str,
        *,
        nvt_oid: Optional[str] = None,
        config_id: Optional[str] = None,
    ) -> Any:
        """Request a nvt preference

        Arguments:
            name: name of a particular preference
            nvt_oid: OID of nvt
            config_id: UUID of scan config of which to show preference values

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_preferences")

        if not name:
            raise RequiredArgument(
                function=self.get_preference.__name__, argument='name'
            )

        cmd.set_attribute("preference", name)

        if nvt_oid:
            cmd.set_attribute("nvt_oid", nvt_oid)

        if config_id:
            cmd.set_attribute("config_id", config_id)

        return self._send_xml_command(cmd)

    def get_report_formats(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        alerts: Optional[bool] = None,
        params: Optional[bool] = None,
        details: Optional[bool] = None,
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

        add_filter(cmd, filter, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if alerts is not None:
            cmd.set_attribute("alerts", to_bool(alerts))

        if params is not None:
            cmd.set_attribute("params", to_bool(params))

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_report_format(
        self, report_format_id: Union[str, ReportFormatType]
    ) -> Any:
        """Request a single report format

        Arguments:
            report_format_id: UUID of an existing report format
                              or ReportFormatType (enum)
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_report_formats")
        if not report_format_id:
            raise RequiredArgument(
                function=self.get_report_format.__name__,
                argument='report_format_id',
            )

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_roles(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
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

        add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

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
        cmd = XmlCommand("get_settings")

        if not setting_id:
            raise RequiredArgument(
                function=self.get_setting.__name__, argument='setting_id'
            )

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
        slave_id: Optional[str] = None,
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
            if not isinstance(duration, Integral):
                raise InvalidArgument("duration needs to be an integer number")

            cmd.set_attribute("duration", str(duration))

        if start_time:
            cmd.set_attribute("start_time", str(start_time))

        if end_time:
            cmd.set_attribute("end_time", str(end_time))

        if brief is not None:
            cmd.set_attribute("brief", to_bool(brief))

        if slave_id:
            cmd.set_attribute("slave_id", slave_id)

        return self._send_xml_command(cmd)

    def get_version(self) -> Any:
        """Get the Greenbone Manager Protocol version used by the remote gvmd
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("get_version"))

    def help(
        self, *, format: Optional[str] = None, help_type: Optional[str] = None
    ) -> Any:
        """Get the help text

        Arguments:
            format: One of "html", "rnc", "text" or "xml
            help_type: One of "brief" or "". Default ""

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("help")

        if not help_type:
            help_type = ""

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

    def modify_group(
        self,
        group_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        users: Optional[List[str]] = None,
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
            cmd.add_element("users", to_comma_list(users))

        return self._send_xml_command(cmd)

    def modify_report_format(
        self,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        *,
        active: Optional[bool] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        param_name: Optional[str] = None,
        param_value: Optional[str] = None,
    ) -> Any:
        """Modifies an existing report format.

        Arguments:
            report_format_id: UUID of report format to modify
                              or ReportFormatType (enum)
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
                argument='report_format_id ',
            )

        cmd = XmlCommand("modify_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        if active is not None:
            cmd.add_element("active", to_bool(active))

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
        users: Optional[List[str]] = None,
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
            cmd.add_element("users", to_comma_list(users))

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

        cmd.add_element("value", to_base64(value))

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

    def sync_cert(self) -> Any:
        """Request a synchronization with the CERT feed service

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_cert"))

    def sync_scap(self) -> Any:
        """Request a synchronization with the SCAP feed service

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_scap"))

    def verify_report_format(
        self, report_format_id: Union[str, ReportFormatType]
    ) -> Any:
        """Verify an existing report format

        Verifies the trust level of an existing report format. It will be
        checked whether the signature of the report format currently matches the
        report format. This includes the script and files used to generate
        reports of this format. It is *not* verified if the report format works
        as expected by the user.

        Arguments:
            report_format_id: UUID of the report format to be verified
                              or ReportFormatType (enum)

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.verify_report_format.__name__,
                argument='report_format_id',
            )

        cmd = XmlCommand("verify_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        return self._send_xml_command(cmd)
