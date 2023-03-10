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
from typing import Any, List, Optional

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.utils import add_filter, to_bool, to_comma_list
from gvm.xml import XmlCommand


class AliveTest(Enum):
    """Enum for choosing an alive test"""

    SCAN_CONFIG_DEFAULT = "Scan Config Default"
    ICMP_PING = "ICMP Ping"
    TCP_ACK_SERVICE_PING = "TCP-ACK Service Ping"
    TCP_SYN_SERVICE_PING = "TCP-SYN Service Ping"
    ARP_PING = "ARP Ping"
    APR_PING = "ARP Ping"  # Alias for ARP_PING
    ICMP_AND_TCP_ACK_SERVICE_PING = "ICMP & TCP-ACK Service Ping"
    ICMP_AND_ARP_PING = "ICMP & ARP Ping"
    TCP_ACK_SERVICE_AND_ARP_PING = "TCP-ACK Service & ARP Ping"
    ICMP_TCP_ACK_SERVICE_AND_ARP_PING = (  # pylint: disable=invalid-name
        "ICMP, TCP-ACK Service & ARP Ping"
    )
    CONSIDER_ALIVE = "Consider Alive"

    @classmethod
    def from_string(
        cls,
        alive_test: Optional[str],
    ) -> Optional["AliveTest"]:
        """Convert an alive test string into a AliveTest instance"""
        if not alive_test:
            return None

        alive_test = alive_test.lower()

        try:
            return cls[
                alive_test.replace(",", "")
                .replace(" ", "_")
                .replace("-", "_")
                .replace("&", "and")
                .upper()
            ]
        except KeyError:
            raise InvalidArgument(
                argument="alive_test",
                function=cls.from_string.__name__,
            ) from None


class TargetsMixin:
    def clone_target(self, target_id: str) -> Any:
        """Clone an existing target

        Arguments:
            target_id: UUID of an existing target to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not target_id:
            raise RequiredArgument(
                function=self.clone_target.__name__, argument="target_id"
            )

        cmd = XmlCommand("create_target")
        cmd.add_element("copy", target_id)
        return self._send_xml_command(cmd)

    def create_target(
        self,
        name: str,
        *,
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
        port_list_id: Optional[str] = None,
    ) -> Any:
        """Create a new target

        Arguments:
            name: Name of the target
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

        cmd = XmlCommand("create_target")
        cmd.add_element("name", name)

        if not name:
            raise RequiredArgument(
                function=self.create_target.__name__, argument="name"
            )

        if asset_hosts_filter:
            cmd.add_element(
                "asset_hosts", attrs={"filter": str(asset_hosts_filter)}
            )
        elif hosts:
            cmd.add_element("hosts", to_comma_list(hosts))
        else:
            raise RequiredArgument(
                function=self.create_target.__name__,
                argument="hosts or asset_hosts_filter",
            )

        if comment:
            cmd.add_element("comment", comment)

        if exclude_hosts:
            cmd.add_element("exclude_hosts", to_comma_list(exclude_hosts))

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
                    argument="alive_test",
                    arg_type=AliveTest.__name__,
                )

            cmd.add_element("alive_tests", alive_test.value)

        if reverse_lookup_only is not None:
            cmd.add_element("reverse_lookup_only", to_bool(reverse_lookup_only))

        if reverse_lookup_unify is not None:
            cmd.add_element(
                "reverse_lookup_unify", to_bool(reverse_lookup_unify)
            )

        # since 20.08 one of port_range or port_list_id is required!
        if not port_range and not port_list_id:
            raise RequiredArgument(
                function=self.create_target.__name__,
                argument="port_range or port_list_id",
            )

        if port_range:
            cmd.add_element("port_range", port_range)

        if port_list_id:
            cmd.add_element("port_list", attrs={"id": port_list_id})

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
                function=self.delete_target.__name__, argument="target_id"
            )

        cmd = XmlCommand("delete_target")
        cmd.set_attribute("target_id", target_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_target(
        self, target_id: str, *, tasks: Optional[bool] = None
    ) -> Any:
        """Request a single target

        Arguments:
            target_id: UUID of an existing target
            tasks: Whether to include list of tasks that use the target

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_targets")

        if not target_id:
            raise RequiredArgument(
                function=self.get_target.__name__, argument="target_id"
            )

        cmd.set_attribute("target_id", target_id)

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_targets(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> Any:
        """Request a list of targets

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan targets instead
            tasks: Whether to include list of tasks that use the target

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_targets")

        add_filter(cmd, filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

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
        port_list_id: Optional[str] = None,
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
                function=self.modify_target.__name__, argument="target_id"
            )

        cmd = XmlCommand("modify_target")
        cmd.set_attribute("target_id", target_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if hosts:
            cmd.add_element("hosts", to_comma_list(hosts))
            if exclude_hosts is None:
                exclude_hosts = [""]

        if exclude_hosts:
            cmd.add_element("exclude_hosts", to_comma_list(exclude_hosts))

        if alive_test:
            if not isinstance(alive_test, AliveTest):
                raise InvalidArgumentType(
                    function=self.modify_target.__name__,
                    argument="alive_test",
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
            cmd.add_element("reverse_lookup_only", to_bool(reverse_lookup_only))

        if reverse_lookup_unify is not None:
            cmd.add_element(
                "reverse_lookup_unify", to_bool(reverse_lookup_unify)
            )

        if port_list_id:
            cmd.add_element("port_list", attrs={"id": port_list_id})

        return self._send_xml_command(cmd)
