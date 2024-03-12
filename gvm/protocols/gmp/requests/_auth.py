# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.xml import XmlCommand


class Authentication:

    @classmethod
    def authenticate(cls, username: str, password: str) -> Request:
        """Authenticate to gvmd.

        The generated authenticate command will be send to server.
        Afterwards the response is read, transformed and returned.

        Args:
            username: Username
            password: Password
        """
        cmd = XmlCommand("authenticate")

        if not username:
            raise RequiredArgument(
                function=cls.authenticate.__name__, argument="username"
            )

        if not password:
            raise RequiredArgument(
                function=cls.authenticate.__name__, argument="password"
            )

        credentials = cmd.add_element("credentials")
        credentials.add_element("username", username)
        credentials.add_element("password", password)
        return cmd

    @staticmethod
    def describe_auth() -> Request:
        """Describe authentication methods

        Returns a list of all used authentication methods if such a list is
        available.
        """
        return XmlCommand("describe_auth")

    @classmethod
    def modify_auth(
        cls, group_name: str, auth_conf_settings: dict[str, str]
    ) -> Request:
        """Modifies an existing authentication.

        Args:
            group_name: Name of the group to be modified.
            auth_conf_settings: The new auth config.
        """
        if not group_name:
            raise RequiredArgument(
                function=cls.modify_auth.__name__, argument="group_name"
            )
        if not auth_conf_settings:
            raise RequiredArgument(
                function=cls.modify_auth.__name__,
                argument="auth_conf_settings",
            )

        cmd = XmlCommand("modify_auth")
        group = cmd.add_element("group", attrs={"name": str(group_name)})

        for key, value in auth_conf_settings.items():
            auth_conf = group.add_element("auth_conf_setting")
            auth_conf.add_element("key", key)
            auth_conf.add_element("value", value)

        return cmd
