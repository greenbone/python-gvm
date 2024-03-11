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

        Arguments:
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

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_and_transform_command(Authentication.describe_auth())

    def modify_auth(
        self, group_name: str, auth_conf_settings: dict[str, str]
    ) -> T:
        """Modifies an existing auth.

        Arguments:
            group_name: Name of the group to be modified.
            auth_conf_settings: The new auth config.
        """
        return self._send_and_transform_command(
            Authentication.modify_auth(group_name, auth_conf_settings)
        )

    def get_version(self) -> T:
        return self._send_and_transform_command(Version.get_version())

    def clone_port_list(self, port_list_id: str) -> T:
        return self._send_and_transform_command(
            PortList.clone_port_list(port_list_id)
        )

    def create_port_list(
        self, name: str, port_range: str, *, comment: Optional[str] = None
    ) -> T:
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
        return self._send_and_transform_command(
            PortList.create_port_range(
                port_list_id, start, end, port_range_type, comment=comment
            )
        )

    def delete_port_list(
        self, port_list_id: str, *, ultimate: bool = False
    ) -> T:
        return self._send_and_transform_command(
            PortList.delete_port_list(port_list_id, ultimate=ultimate)
        )

    def delete_port_range(self, port_range_id: str) -> T:
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
        return self._send_and_transform_command(
            PortList.modify_port_list(port_list_id, comment=comment, name=name)
        )
