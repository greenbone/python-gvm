# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm._enum import Enum
from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool, to_comma_list
from gvm.xml import XmlCommand

from .._entity_id import EntityID


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


class Targets:
    @classmethod
    def create_target(
        cls,
        name: str,
        *,
        asset_hosts_filter: Optional[str] = None,
        hosts: Optional[list[str]] = None,
        comment: Optional[str] = None,
        exclude_hosts: Optional[list[str]] = None,
        ssh_credential_id: Optional[EntityID] = None,
        ssh_credential_port: Optional[Union[int, str]] = None,
        smb_credential_id: Optional[EntityID] = None,
        esxi_credential_id: Optional[EntityID] = None,
        snmp_credential_id: Optional[EntityID] = None,
        alive_test: Optional[Union[str, AliveTest]] = None,
        allow_simultaneous_ips: Optional[bool] = None,
        reverse_lookup_only: Optional[bool] = None,
        reverse_lookup_unify: Optional[bool] = None,
        port_range: Optional[str] = None,
        port_list_id: Optional[EntityID] = None,
    ) -> Request:
        """Create a new target

        Args:
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
            allow_simultaneous_ips: Whether to scan multiple IPs of the
                same host simultaneously
            reverse_lookup_only: Whether to scan only hosts that have names
            reverse_lookup_unify: Whether to scan only one IP when multiple IPs
                have the same name.
            port_range: Port range for the target
            port_list_id: UUID of the port list to use on target
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_target.__name__, argument="name"
            )

        cmd = XmlCommand("create_target")
        cmd.add_element("name", name)

        if asset_hosts_filter:
            cmd.add_element(
                "asset_hosts", attrs={"filter": str(asset_hosts_filter)}
            )
        elif hosts:
            cmd.add_element("hosts", to_comma_list(hosts))
        else:
            raise RequiredArgument(
                function=cls.create_target.__name__,
                argument="hosts or asset_hosts_filter",
            )

        if comment:
            cmd.add_element("comment", comment)

        if exclude_hosts:
            cmd.add_element("exclude_hosts", to_comma_list(exclude_hosts))

        if ssh_credential_id:
            xml_ssh = cmd.add_element(
                "ssh_credential", attrs={"id": str(ssh_credential_id)}
            )
            if ssh_credential_port:
                xml_ssh.add_element("port", str(ssh_credential_port))

        if smb_credential_id:
            cmd.add_element(
                "smb_credential", attrs={"id": str(smb_credential_id)}
            )

        if esxi_credential_id:
            cmd.add_element(
                "esxi_credential", attrs={"id": str(esxi_credential_id)}
            )

        if snmp_credential_id:
            cmd.add_element(
                "snmp_credential", attrs={"id": str(snmp_credential_id)}
            )

        if alive_test:
            if not isinstance(alive_test, AliveTest):
                alive_test = AliveTest(alive_test)
            cmd.add_element("alive_tests", alive_test.value)

        if allow_simultaneous_ips is not None:
            cmd.add_element(
                "allow_simultaneous_ips", to_bool(allow_simultaneous_ips)
            )

        if reverse_lookup_only is not None:
            cmd.add_element("reverse_lookup_only", to_bool(reverse_lookup_only))

        if reverse_lookup_unify is not None:
            cmd.add_element(
                "reverse_lookup_unify", to_bool(reverse_lookup_unify)
            )

        if port_range:
            cmd.add_element("port_range", port_range)

        if port_list_id:
            cmd.add_element("port_list", attrs={"id": str(port_list_id)})

        return cmd

    @classmethod
    def modify_target(
        cls,
        target_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        hosts: Optional[list[str]] = None,
        exclude_hosts: Optional[list[str]] = None,
        ssh_credential_id: Optional[EntityID] = None,
        ssh_credential_port: Optional[Union[str, int]] = None,
        smb_credential_id: Optional[EntityID] = None,
        esxi_credential_id: Optional[EntityID] = None,
        snmp_credential_id: Optional[EntityID] = None,
        alive_test: Optional[Union[AliveTest, str]] = None,
        allow_simultaneous_ips: Optional[bool] = None,
        reverse_lookup_only: Optional[bool] = None,
        reverse_lookup_unify: Optional[bool] = None,
        port_list_id: Optional[EntityID] = None,
    ) -> Request:
        """Modify an existing target.

        Args:
            target_id: UUID of target to modify.
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
            allow_simultaneous_ips: Whether to scan multiple IPs of the
                same host simultaneously
            reverse_lookup_only: Whether to scan only hosts that have names.
            reverse_lookup_unify: Whether to scan only one IP when multiple IPs
                have the same name.
        """
        if not target_id:
            raise RequiredArgument(
                function=cls.modify_target.__name__, argument="target_id"
            )

        cmd = XmlCommand("modify_target")
        cmd.set_attribute("target_id", str(target_id))

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
                alive_test = AliveTest(alive_test)
            cmd.add_element("alive_tests", alive_test.value)

        if ssh_credential_id:
            xml_ssh = cmd.add_element(
                "ssh_credential", attrs={"id": str(ssh_credential_id)}
            )

            if ssh_credential_port:
                xml_ssh.add_element("port", str(ssh_credential_port))

        if smb_credential_id:
            cmd.add_element(
                "smb_credential", attrs={"id": str(smb_credential_id)}
            )

        if esxi_credential_id:
            cmd.add_element(
                "esxi_credential", attrs={"id": str(esxi_credential_id)}
            )

        if snmp_credential_id:
            cmd.add_element(
                "snmp_credential", attrs={"id": str(snmp_credential_id)}
            )

        if allow_simultaneous_ips is not None:
            cmd.add_element(
                "allow_simultaneous_ips", to_bool(allow_simultaneous_ips)
            )

        if reverse_lookup_only is not None:
            cmd.add_element("reverse_lookup_only", to_bool(reverse_lookup_only))

        if reverse_lookup_unify is not None:
            cmd.add_element(
                "reverse_lookup_unify", to_bool(reverse_lookup_unify)
            )

        if port_list_id:
            cmd.add_element("port_list", attrs={"id": str(port_list_id)})

        return cmd

    @classmethod
    def clone_target(cls, target_id: EntityID) -> Request:
        """Clone an existing target.

        Args:
            target_id: UUID of an existing target to clone.
        """
        if not target_id:
            raise RequiredArgument(
                function=cls.clone_target.__name__, argument="target_id"
            )

        cmd = XmlCommand("create_target")
        cmd.add_element("copy", str(target_id))
        return cmd

    @classmethod
    def delete_target(
        cls, target_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Delete an existing target.

        Args:
            target_id: UUID of an existing target to delete.
            ultimate: Whether to remove entirely or to the trashcan.
        """
        if not target_id:
            raise RequiredArgument(
                function=cls.delete_target.__name__, argument="target_id"
            )

        cmd = XmlCommand("delete_target")
        cmd.set_attribute("target_id", str(target_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))
        return cmd

    @classmethod
    def get_target(
        cls, target_id: EntityID, *, tasks: Optional[bool] = None
    ) -> Request:
        """Request a single target.

        Args:
            target_id: UUID of the target to request.
            tasks: Whether to include list of tasks that use the target
        """
        if not target_id:
            raise RequiredArgument(
                function=cls.get_target.__name__, argument="target_id"
            )

        cmd = XmlCommand("get_targets")
        cmd.set_attribute("target_id", str(target_id))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return cmd

    @classmethod
    def get_targets(
        cls,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> Request:
        """Request a list of targets.

        Args:
            filter_string: Filter term to use for the query.
            filter_id: UUID of an existing filter to use for the query.
            trash: Whether to include targets in the trashcan.
            tasks: Whether to include list of tasks that use the target.
        """
        cmd = XmlCommand("get_targets")
        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return cmd
