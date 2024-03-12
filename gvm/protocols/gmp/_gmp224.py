# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from .._protocol import GvmProtocol, T
from .requests import (
    Authentication,
    PortList,
    PortRangeType,
    Version,
)


class GMPv224(GvmProtocol[T]):
    _authenticated = False

    @staticmethod
    def get_protocol_version() -> tuple[int, int]:
        """
        Return the supported GMP version as major, minor version tuple
        """
        return (22, 4)

    def is_authenticated(self) -> bool:
        """Checks if the user is authenticated

        If the user is authenticated privileged GMP commands like get_tasks
        may be send to gvmd.

        Returns:
            bool: True if an authenticated connection to gvmd has been
            established.
        """
        return self._authenticated

    def authenticate(self, username: str, password: str) -> T:
        """Authenticate to gvmd.

        The generated authenticate command will be send to server.
        Afterwards the response is read, transformed and returned.

        Args:
            username: Username
            password: Password
        """
        response = self._send_command(
            Authentication.authenticate(username=username, password=password)
        )

        if response.is_success:
            self._authenticated = True

        return self._transform(response)

    def describe_auth(self) -> T:
        """Describe authentication methods

        Returns a list of all used authentication methods if such a list is
        available.
        """
        return self._send_and_transform_command(Authentication.describe_auth())

    def modify_auth(
        self, group_name: str, auth_conf_settings: dict[str, str]
    ) -> T:
        """Modifies an existing auth.

        Args:
            group_name: Name of the group to be modified.
            auth_conf_settings: The new auth config.
        """
        return self._send_and_transform_command(
            Authentication.modify_auth(group_name, auth_conf_settings)
        )

    def get_version(self) -> T:
        """Get the Greenbone Vulnerability Management Protocol (GMP) version
        used by the remote gvmd.
        """
        return self._send_and_transform_command(Version.get_version())

    def clone_port_list(self, port_list_id: str) -> T:
        """Clone an existing port list

        Args:
            port_list_id: UUID of an existing port list to clone from
        """
        return self._send_and_transform_command(
            PortList.clone_port_list(port_list_id)
        )

    def create_port_list(
        self, name: str, port_range: str, *, comment: Optional[str] = None
    ) -> T:
        """Create a new port list

        Args:
            name: Name of the new port list
            port_range: Port list ranges e.g. `"T: 1-1234"` for tcp port
                1 - 1234
            comment: Comment for the port list
        """
        return self._send_and_transform_command(
            PortList.create_port_list(name, port_range, comment=comment)
        )

    def create_port_range(
        self,
        port_list_id: str,
        start: int,
        end: int,
        port_range_type: Union[str, PortRangeType],
        *,
        comment: Optional[str] = None,
    ) -> T:
        """Create new port range

        Args:
            port_list_id: UUID of the port list to which to add the range
            start: The first port in the range
            end: The last port in the range
            port_range_type: The type of the ports: TCP, UDP, ...
            comment: Comment for the port range
        """
        return self._send_and_transform_command(
            PortList.create_port_range(
                port_list_id, start, end, port_range_type, comment=comment
            )
        )

    def delete_port_list(
        self, port_list_id: str, *, ultimate: bool = False
    ) -> T:
        """Delete an existing port list

        Args:
            port_list_id: UUID of the port list to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_and_transform_command(
            PortList.delete_port_list(port_list_id, ultimate=ultimate)
        )

    def delete_port_range(self, port_range_id: str) -> T:
        """Delete an existing port range

        Args:
            port_range_id: UUID of the port range to be deleted.
        """
        return self._send_and_transform_command(
            PortList.delete_port_range(port_range_id)
        )

    def get_port_lists(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        details: Optional[bool] = None,
        targets: Optional[bool] = None,
        trash: Optional[bool] = None,
    ) -> T:
        """Request a list of port lists

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include full port list details
            targets: Whether to include targets using this port list
            trash: Whether to get port lists in the trashcan instead
        """
        return self._send_and_transform_command(
            PortList.get_port_lists(
                filter_string=filter_string,
                filter_id=filter_id,
                details=details,
                targets=targets,
                trash=trash,
            )
        )

    def get_port_list(self, port_list_id: str) -> T:
        """Request a single port list

        Args:
            port_list_id: UUID of an existing port list
        """
        return self._send_and_transform_command(
            PortList.get_port_list(port_list_id)
        )

    def modify_port_list(
        self,
        port_list_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
    ) -> T:
        """Modify an existing port list.

        Args:
            port_list_id: UUID of port list to modify.
            name: Name of port list.
            comment: Comment on port list.
        """
        return self._send_and_transform_command(
            PortList.modify_port_list(port_list_id, comment=comment, name=name)
        )
