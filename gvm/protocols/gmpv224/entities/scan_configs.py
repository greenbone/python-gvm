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

from typing import Any, List, Optional, Tuple

from lxml.etree import XMLSyntaxError

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.utils import add_filter, deprecation, is_list_like, to_base64, to_bool
from gvm.xml import XmlCommand


class ScanConfigsMixin:
    def clone_scan_config(self, config_id: str) -> Any:
        """Clone a scan config from an existing one

        Arguments:
            config_id: UUID of the existing scan config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.clone_scan_config.__name__, argument="config_id"
            )

        cmd = XmlCommand("create_config")
        cmd.add_element("copy", config_id)
        return self._send_xml_command(cmd)

    def create_scan_config(
        self, config_id: str, name: str, *, comment: Optional[str] = None
    ) -> Any:
        """Create a new scan config

        Arguments:
            config_id: UUID of the existing scan config
            name: Name of the new scan config
            comment: A comment on the config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_scan_config.__name__, argument="name"
            )

        if not config_id:
            raise RequiredArgument(
                function=self.create_scan_config.__name__, argument="config_id"
            )

        cmd = XmlCommand("create_config")
        if comment is not None:
            cmd.add_element("comment", comment)
        cmd.add_element("copy", config_id)
        cmd.add_element("name", name)
        cmd.add_element("usage_type", "scan")
        return self._send_xml_command(cmd)

    def delete_scan_config(
        self, config_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing config

        Arguments:
            config_id: UUID of the config to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.delete_scan_config.__name__, argument="config_id"
            )

        cmd = XmlCommand("delete_config")
        cmd.set_attribute("config_id", config_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_scan_configs(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        families: Optional[bool] = None,
        preferences: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> Any:
        """Request a list of scan configs

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scan configs instead
            details: Whether to get config families, preferences, nvt selectors
                and tasks.
            families: Whether to include the families if no details are
                requested
            preferences: Whether to include the preferences if no details are
                requested
            tasks: Whether to get tasks using this config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_configs")
        cmd.set_attribute("usage_type", "scan")

        add_filter(cmd, filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if families is not None:
            cmd.set_attribute("families", to_bool(families))

        if preferences is not None:
            cmd.set_attribute("preferences", to_bool(preferences))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_scan_config(
        self, config_id: str, *, tasks: Optional[bool] = None
    ) -> Any:
        """Request a single scan config

        Arguments:
            config_id: UUID of an existing scan config
            tasks: Whether to get tasks using this config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.get_scan_config.__name__, argument="config_id"
            )

        cmd = XmlCommand("get_configs")
        cmd.set_attribute("config_id", config_id)

        cmd.set_attribute("usage_type", "scan")

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        # for single entity always request all details
        cmd.set_attribute("details", "1")

        return self._send_xml_command(cmd)

    def get_scan_config_preferences(
        self, *, nvt_oid: Optional[str] = None, config_id: Optional[str] = None
    ) -> Any:
        """Request a list of scan_config preferences

        When the command includes a config_id attribute, the preference element
        includes the preference name, type and value, and the NVT to which the
        preference applies.
        If the command includes a config_id and an nvt_oid, the preferences for
        the given nvt in the config will be shown.

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

    def get_scan_config_preference(
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
                function=self.get_scan_config_preference.__name__,
                argument="name",
            )

        cmd.set_attribute("preference", name)

        if nvt_oid:
            cmd.set_attribute("nvt_oid", nvt_oid)

        if config_id:
            cmd.set_attribute("config_id", config_id)

        return self._send_xml_command(cmd)

    def import_scan_config(self, config: str) -> Any:
        """Import a scan config from XML

        Arguments:
            config: Scan Config XML as string to import. This XML must
                contain a :code:`<get_configs_response>` root element.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config:
            raise RequiredArgument(
                function=self.import_scan_config.__name__, argument="config"
            )

        cmd = XmlCommand("create_config")

        try:
            cmd.append_xml_str(config)
        except XMLSyntaxError as e:
            raise InvalidArgument(
                function=self.import_scan_config.__name__, argument="config"
            ) from e

        return self._send_xml_command(cmd)

    def modify_scan_config_set_nvt_preference(
        self,
        config_id: str,
        name: str,
        nvt_oid: str,
        *,
        value: Optional[str] = None,
    ) -> Any:
        """Modifies the nvt preferences of an existing scan config.

        Arguments:
            config_id: UUID of scan config to modify.
            name: Name for nvt preference to change.
            nvt_oid: OID of the NVT associated with preference to modify
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_scan_config_set_nvt_preference.__name__,
                argument="config_id",
            )

        if not nvt_oid:
            raise RequiredArgument(
                function=self.modify_scan_config_set_nvt_preference.__name__,
                argument="nvt_oid",
            )

        if not name:
            raise RequiredArgument(
                function=self.modify_scan_config_set_nvt_preference.__name__,
                argument="name",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        _xmlpref = cmd.add_element("preference")

        _xmlpref.add_element("nvt", attrs={"oid": nvt_oid})
        _xmlpref.add_element("name", name)

        if value:
            _xmlpref.add_element("value", to_base64(value))

        return self._send_xml_command(cmd)

    def modify_scan_config_set_name(self, config_id: str, name: str) -> Any:
        """Modifies the name of an existing scan config

        Arguments:
            config_id: UUID of scan config to modify.
            name: New name for the config.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_scan_config_set_name.__name__,
                argument="config_id",
            )

        if not name:
            raise RequiredArgument(
                function=self.modify_scan_config_set_name.__name__,
                argument="name",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        cmd.add_element("name", name)

        return self._send_xml_command(cmd)

    def modify_scan_config_set_comment(
        self, config_id: str, *, comment: Optional[str] = None
    ) -> Any:
        """Modifies the comment of an existing scan config

        Arguments:
            config_id: UUID of scan config to modify.
            comment: Comment to set on a config. Default is an
                empty comment and the previous comment will be
                removed.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_scan_config_set_comment.__name__,
                argument="config_id argument",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))
        if not comment:
            comment = ""
        cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def modify_scan_config_set_scanner_preference(
        self, config_id: str, name: str, *, value: Optional[str] = None
    ) -> Any:
        """Modifies the scanner preferences of an existing scan config

        Arguments:
            config_id: UUID of scan config to modify.
            name: Name of the scanner preference to change
            value: New value for the preference. None to delete the preference
                and to use the default instead.

        """
        if not config_id:
            raise RequiredArgument(
                function=(
                    self.modify_scan_config_set_scanner_preference.__name__
                ),
                argument="config_id",
            )

        if not name:
            raise RequiredArgument(
                function=(
                    self.modify_scan_config_set_scanner_preference.__name__
                ),
                argument="name argument",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        _xmlpref = cmd.add_element("preference")

        _xmlpref.add_element("name", name)

        if value:
            _xmlpref.add_element("value", to_base64(value))

        return self._send_xml_command(cmd)

    def modify_scan_config_set_nvt_selection(
        self, config_id: str, family: str, nvt_oids: List[str]
    ) -> Any:
        """Modifies the selected nvts of an existing scan config

        The manager updates the given family in the config to include only the
        given NVTs.

        Arguments:
            config_id: UUID of scan config to modify.
            family: Name of the NVT family to include NVTs from
            nvt_oids: List of NVTs to select for the family.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_scan_config_set_nvt_selection.__name__,
                argument="config_id",
            )

        if not family:
            raise RequiredArgument(
                function=self.modify_scan_config_set_nvt_selection.__name__,
                argument="family argument",
            )

        if not is_list_like(nvt_oids):
            raise InvalidArgumentType(
                function=self.modify_scan_config_set_nvt_selection.__name__,
                argument="nvt_oids",
                arg_type="list",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        _xmlnvtsel = cmd.add_element("nvt_selection")
        _xmlnvtsel.add_element("family", family)

        for nvt in nvt_oids:
            _xmlnvtsel.add_element("nvt", attrs={"oid": nvt})

        return self._send_xml_command(cmd)

    def modify_scan_config_set_family_selection(
        self,
        config_id: str,
        families: List[Tuple[str, bool, bool]],
        *,
        auto_add_new_families: Optional[bool] = True,
    ) -> Any:
        """
        Selected the NVTs of a scan config at a family level.

        Arguments:
            config_id: UUID of scan config to modify.
            families: A list of tuples (str, bool, bool):
                str: the name of the NVT family selected,
                bool: add new NVTs  to the family automatically,
                bool: include all NVTs from the family
            auto_add_new_families: Whether new families should be added to the
                scan config automatically. Default: True.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_scan_config_set_family_selection.__name__,
                argument="config_id",
            )

        if not is_list_like(families):
            raise InvalidArgumentType(
                function=self.modify_scan_config_set_family_selection.__name__,
                argument="families",
                arg_type="list",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        _xmlfamsel = cmd.add_element("family_selection")
        _xmlfamsel.add_element("growing", to_bool(auto_add_new_families))

        for family in families:
            _xmlfamily = _xmlfamsel.add_element("family")
            _xmlfamily.add_element("name", family[0])

            if len(family) != 3:
                raise InvalidArgument(
                    "Family must be a tuple of 3. (str, bool, bool)"
                )

            if not isinstance(family[1], bool) or not isinstance(
                family[2], bool
            ):
                raise InvalidArgumentType(
                    function=(
                        self.modify_scan_config_set_family_selection.__name__
                    ),
                    argument="families",
                    arg_type="[tuple(str, bool, bool)]",
                )

            _xmlfamily.add_element("all", to_bool(family[2]))
            _xmlfamily.add_element("growing", to_bool(family[1]))

        return self._send_xml_command(cmd)

    def modify_scan_config(
        self, config_id: str, selection: Optional[str] = None, **kwargs
    ) -> Any:
        """Modifies an existing scan config.

        DEPRECATED. Please use *modify_scan_config_set_* methods instead.

        modify_config has four modes to operate depending on the selection.

        Arguments:
            config_id: UUID of scan config to modify.
            selection: one of 'scan_pref', 'nvt_pref', 'nvt_selection' or
                'family_selection'
            name: New name for preference.
            value: New value for preference.
            nvt_oids: List of NVTs associated with preference to modify.
            family: Name of family to modify.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not config_id:
            raise RequiredArgument(
                function=self.modify_scan_config.__name__,
                argument="config_id argument",
            )

        if selection is None:
            deprecation(
                "Using modify_config to update the comment of a scan config is"
                "deprecated. Please use modify_scan_config_set_comment instead."
            )
            return self.modify_scan_config_set_comment(
                config_id, comment=kwargs.get("comment")
            )

        if selection not in (
            "nvt_pref",
            "scan_pref",
            "family_selection",
            "nvt_selection",
        ):
            raise InvalidArgument(
                "selection must be one of nvt_pref, "
                "scan_pref, family_selection or "
                "nvt_selection"
            )

        if selection == "nvt_pref":
            deprecation(
                "Using modify_scan_config to update a nvt preference of a scan "
                "config is deprecated. Please use "
                "modify_scan_config_set_nvt_preference instead."
            )
            return self.modify_scan_config_set_nvt_preference(
                config_id, **kwargs
            )

        if selection == "scan_pref":
            deprecation(
                "Using modify_scan_config to update a scanner preference of a "
                "scan config is deprecated. Please use "
                "modify_scan_config_set_scanner_preference instead."
            )
            return self.modify_scan_config_set_scanner_preference(
                config_id, **kwargs
            )

        if selection == "nvt_selection":
            deprecation(
                "Using modify_scan_config to update a nvt selection of a "
                "scan config is deprecated. Please use "
                "modify_scan_config_set_nvt_selection instead."
            )
            return self.modify_scan_config_set_nvt_selection(
                config_id, **kwargs
            )

        deprecation(
            "Using modify_scan_config to update a family selection of a "
            "scan config is deprecated. Please use "
            "modify_scan_config_set_family_selection instead."
        )
        return self.modify_scan_config_set_family_selection(config_id, **kwargs)
