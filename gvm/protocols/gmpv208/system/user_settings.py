# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Any, Optional

from gvm.errors import RequiredArgument
from gvm.utils import to_base64
from gvm.xml import XmlCommand


class UserSettingsMixin:
    def get_user_settings(self, *, filter_string: Optional[str] = None) -> Any:
        """Request a list of user settings

        Arguments:
            filter_string: Filter term to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_settings")

        if filter_string:
            cmd.set_attribute("filter", filter_string)

        return self._send_xml_command(cmd)

    def get_user_setting(self, setting_id: str) -> Any:
        """Request a single user setting

        Arguments:
            setting_id: UUID of an existing setting

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_settings")

        if not setting_id:
            raise RequiredArgument(
                function=self.get_user_setting.__name__, argument="setting_id"
            )

        cmd.set_attribute("setting_id", setting_id)
        return self._send_xml_command(cmd)

    def modify_user_setting(
        self,
        setting_id: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ) -> Any:
        """Modifies an existing user setting.

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
                function=self.modify_user_setting.__name__,
                argument="setting_id or name argument",
            )

        if value is None:
            raise RequiredArgument(
                function=self.modify_user_setting.__name__,
                argument="value argument",
            )

        cmd = XmlCommand("modify_setting")

        if setting_id:
            cmd.set_attribute("setting_id", setting_id)
        else:
            cmd.add_element("name", name)

        cmd.add_element("value", to_base64(value))

        return self._send_xml_command(cmd)
