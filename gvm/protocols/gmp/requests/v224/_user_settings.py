# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_base64
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class UserSettings:
    @staticmethod
    def get_user_settings(*, filter_string: Optional[str] = None) -> Request:
        """Request a list of user settings

        Args:
            filter_string: Filter term to use for the query
        """
        cmd = XmlCommand("get_settings")

        if filter_string:
            cmd.set_attribute("filter", filter_string)

        return cmd

    @classmethod
    def get_user_setting(cls, setting_id: EntityID) -> Request:
        """Request a single user setting

        Args:
            setting_id: UUID of an existing setting
        """
        cmd = XmlCommand("get_settings")

        if not setting_id:
            raise RequiredArgument(
                function=cls.get_user_setting.__name__, argument="setting_id"
            )

        cmd.set_attribute("setting_id", str(setting_id))
        return cmd

    @classmethod
    def modify_user_setting(
        cls,
        *,
        setting_id: Optional[EntityID] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ) -> Request:
        """Modifies an existing user setting.

        Args:
            setting_id: UUID of the setting to be changed.
            name: The name of the setting. Either setting_id or name must be
                passed.
            value: The value of the setting.
        """
        if not setting_id and not name:
            raise RequiredArgument(
                function=cls.modify_user_setting.__name__,
                argument="setting_id or name argument",
            )

        if value is None:
            raise RequiredArgument(
                function=cls.modify_user_setting.__name__,
                argument="value argument",
            )

        cmd = XmlCommand("modify_setting")

        if setting_id:
            cmd.set_attribute("setting_id", str(setting_id))
        else:
            cmd.add_element("name", name)

        cmd.add_element("value", to_base64(value))

        return cmd
