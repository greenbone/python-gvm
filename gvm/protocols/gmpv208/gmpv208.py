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

# pylint: disable=arguments-differ, redefined-builtin, too-many-lines

"""
Module for communication with gvmd in
`Greenbone Management Protocol version 20.08`_

.. _Greenbone Management Protocol version 20.08:
    https://docs.greenbone.net/API/GMP/gmp-20.08.html
"""
import warnings

from typing import Any, List, Optional, Callable

from gvm.utils import deprecation
from gvm.xml import XmlCommand

from gvm.protocols.gmpv7.gmpv7 import (
    _to_bool,
    _to_comma_list,
)
from gvm.connections import GvmConnection
from gvm.errors import InvalidArgumentType, RequiredArgument

from gvm.protocols.base import GvmProtocol

from . import types
from .types import *  # pylint: disable=unused-wildcard-import, wildcard-import

_EMPTY_POLICY_ID = '085569ce-73ed-11df-83c3-002264764cea'

PROTOCOL_VERSION = (20, 8)


class GmpV208Mixin(GvmProtocol):
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

    def create_agent(
        self,
        installer: str,
        signature: str,
        name: str,
        *,
        comment: Optional[str] = None,
        howto_install: Optional[str] = None,
        howto_use: Optional[str] = None
    ) -> None:
        # pylint: disable=unused-argument
        deprecation(
            "{} has been removed in GMP version {}.{}".format(
                self.create_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def clone_agent(self, agent_id: str) -> None:
        # pylint: disable=unused-argument
        deprecation(
            "{} has been removed in GMP version {}.{}".format(
                self.clone_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def modify_agent(
        self,
        agent_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None
    ) -> None:
        # pylint: disable=unused-argument
        deprecation(
            "{} has been removed in GMP version {}.{}".format(
                self.clone_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def delete_agent(
        self,
        agent_id: str,
        *,
        ultimate: Optional[bool] = False
        # pylint: disable=unused-argument
    ) -> None:
        deprecation(
            "{} has been removed in GMP version {}.{}".format(
                self.delete_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def verify_agent(self, agent_id: str) -> None:
        # pylint: disable=unused-argument
        deprecation(
            "{} has been removed in GMP version {}.{}".format(
                self.verify_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def get_agent(self, agent_id: str) -> None:
        # pylint: disable=unused-argument
        deprecation(
            "{} has been removed in GMP version {}.{}".format(
                self.get_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def get_info(self, info_id: str, info_type: InfoType) -> Any:
        """Request a single secinfo

        Arguments:
            info_id: UUID of an existing secinfo
            info_type: Type must be either CERT_BUND_ADV, CPE, CVE,
                DFN_CERT_ADV, OVALDEF, NVT

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

    def modify_schedule(
        self,
        schedule_id: str,
        *,
        name: Optional[str] = None,
        icalendar: Optional[str] = None,
        timezone: Optional[str] = None,
        comment: Optional[str] = None
    ) -> Any:
        """Modifies an existing schedule

        Arguments:
            schedule_id: UUID of the schedule to be modified
            name: Name of the schedule
            icalendar: `iCalendar`_ (RFC 5545) based data.
            timezone: Timezone to use for the icalender events e.g
                Europe/Berlin. If the datetime values in the icalendar data are
                missing timezone information this timezone gets applied.
                Otherwise the datetime values from the icalendar data are
                displayed in this timezone
            commenhedule.

        Returns:
            The response. See :py:meth:`send_command` for details.

        .. _iCalendar:
            https://tools.ietf.org/html/rfc5545
        """
        if not schedule_id:
            raise RequiredArgument(
                function=self.modify_schedule.__name__, argument='schedule_id'
            )

        cmd = XmlCommand("modify_schedule")
        cmd.set_attribute("schedule_id", schedule_id)

        if name:
            cmd.add_element("name", name)

        if icalendar:
            cmd.add_element("icalendar", icalendar)

        if timezone:
            cmd.add_element("timezone", timezone)

        if comment:
            cmd.add_element("comment", comment)

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
            make_unique: Deprecated. Will be ignored.
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
        if make_unique is not None:
            warnings.warn(
                'create_target make_unique argument is deprecated '
                'and will be ignored.',
                DeprecationWarning,
            )

        if not name:
            raise RequiredArgument(
                function=self.create_target.__name__, argument='name'
            )

        # since 20.08 one of port_range or port_list_id is required!
        if not port_range and not port_list_id:
            raise RequiredArgument(
                function=self.create_target.__name__,
                argument='port_range or port_list_id',
            )

        cmd = XmlCommand("create_target")
        _xmlname = cmd.add_element("name", name)

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
