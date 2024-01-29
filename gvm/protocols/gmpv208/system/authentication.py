# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Any

from gvm.errors import RequiredArgument
from gvm.utils import check_command_status
from gvm.xml import XmlCommand


class AuthenticationMixin:
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
                function=self.authenticate.__name__, argument="username"
            )

        if not password:
            raise RequiredArgument(
                function=self.authenticate.__name__, argument="password"
            )

        credentials = cmd.add_element("credentials")
        credentials.add_element("username", username)
        credentials.add_element("password", password)

        self._send(cmd.to_string())
        response = self._read()

        if check_command_status(response):
            self._authenticated = True

        return self._transform(response)

    def describe_auth(self) -> Any:
        """Describe authentication methods

        Returns a list of all used authentication methods if such a list is
        available.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("describe_auth"))

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
                function=self.modify_auth.__name__, argument="group_name"
            )
        if not auth_conf_settings:
            raise RequiredArgument(
                function=self.modify_auth.__name__,
                argument="auth_conf_settings",
            )
        cmd = XmlCommand("modify_auth")
        _xmlgroup = cmd.add_element("group", attrs={"name": str(group_name)})

        for key, value in auth_conf_settings.items():
            _xmlauthconf = _xmlgroup.add_element("auth_conf_setting")
            _xmlauthconf.add_element("key", key)
            _xmlauthconf.add_element("value", value)

        return self._send_xml_command(cmd)
