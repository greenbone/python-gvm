# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import is_list_like, to_base64, to_bool
from gvm.xml import XmlCommand, XmlError

from .._entity_id import EntityID


class ScanConfigs:
    @classmethod
    def clone_scan_config(cls, config_id: EntityID) -> Request:
        """Clone a scan config from an existing one

        Args:
            config_id: UUID of the existing scan config
        """
        if not config_id:
            raise RequiredArgument(
                function=cls.clone_scan_config.__name__, argument="config_id"
            )

        cmd = XmlCommand("create_config")
        cmd.add_element("copy", str(config_id))
        return cmd

    @classmethod
    def create_scan_config(
        cls,
        config_id: EntityID,
        name: str,
        *,
        comment: Optional[str] = None,
    ) -> Request:
        """Create a new scan config

        Args:
            config_id: UUID of the existing scan config
            name: Name of the new scan config
            comment: A comment on the config
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_scan_config.__name__, argument="name"
            )

        if not config_id:
            raise RequiredArgument(
                function=cls.create_scan_config.__name__, argument="config_id"
            )

        cmd = XmlCommand("create_config")
        if comment is not None:
            cmd.add_element("comment", comment)

        cmd.add_element("copy", str(config_id))
        cmd.add_element("name", name)
        cmd.add_element("usage_type", "scan")

        return cmd

    @classmethod
    def delete_scan_config(
        cls, config_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Deletes an existing config

        Args:
            config_id: UUID of the config to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not config_id:
            raise RequiredArgument(
                function=cls.delete_scan_config.__name__, argument="config_id"
            )

        cmd = XmlCommand("delete_config")
        cmd.set_attribute("config_id", str(config_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @staticmethod
    def get_scan_configs(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        families: Optional[bool] = None,
        preferences: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> Request:
        """Request a list of scan configs

        Args:
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
        """
        cmd = XmlCommand("get_configs")
        cmd.set_attribute("usage_type", "scan")

        cmd.add_filter(filter_string, filter_id)

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

        return cmd

    @classmethod
    def get_scan_config(
        cls, config_id: EntityID, *, tasks: Optional[bool] = None
    ) -> Request:
        """Request a single scan config

        Args:
            config_id: UUID of an existing scan config
            tasks: Whether to get tasks using this config
        """
        if not config_id:
            raise RequiredArgument(
                function=cls.get_scan_config.__name__, argument="config_id"
            )

        cmd = XmlCommand("get_configs")
        cmd.set_attribute("config_id", str(config_id))

        cmd.set_attribute("usage_type", "scan")

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        # for single entity always request all details
        cmd.set_attribute("details", "1")

        return cmd

    @classmethod
    def get_scan_config_preferences(
        cls,
        *,
        nvt_oid: Optional[str] = None,
        config_id: Optional[EntityID] = None,
    ) -> Request:
        """Request a list of scan_config preferences

        When the command includes a config_id attribute, the preference element
        includes the preference name, type and value, and the NVT to which the
        preference applies.
        If the command includes a config_id and an nvt_oid, the preferences for
        the given nvt in the config will be shown.

        Args:
            nvt_oid: OID of nvt
            config_id: UUID of scan config of which to show preference values
        """
        cmd = XmlCommand("get_preferences")

        if nvt_oid:
            cmd.set_attribute("nvt_oid", str(nvt_oid))

        if config_id:
            cmd.set_attribute("config_id", str(config_id))

        return cmd

    @classmethod
    def get_scan_config_preference(
        cls,
        name: str,
        *,
        nvt_oid: Optional[str] = None,
        config_id: Optional[EntityID] = None,
    ) -> Request:
        """Request a nvt preference

        Args:
            name: name of a particular preference
            nvt_oid: OID of nvt
            config_id: UUID of scan config of which to show preference values
        """
        cmd = XmlCommand("get_preferences")

        if not name:
            raise RequiredArgument(
                function=cls.get_scan_config_preference.__name__,
                argument="name",
            )

        cmd.set_attribute("preference", name)

        if nvt_oid:
            cmd.set_attribute("nvt_oid", str(nvt_oid))

        if config_id:
            cmd.set_attribute("config_id", str(config_id))

        return cmd

    @classmethod
    def import_scan_config(cls, config: str) -> Request:
        """Import a scan config from XML

        Args:
            config: Scan Config XML as string to import. This XML must
                contain a :code:`<get_configs_response>` root element.
        """
        if not config:
            raise RequiredArgument(
                function=cls.import_scan_config.__name__, argument="config"
            )

        cmd = XmlCommand("create_config")

        try:
            cmd.append_xml_str(config)
        except XmlError as e:
            raise InvalidArgument(
                function=cls.import_scan_config.__name__, argument="config"
            ) from e

        return cmd

    @classmethod
    def modify_scan_config_set_nvt_preference(
        cls,
        config_id: EntityID,
        name: str,
        nvt_oid: str,
        *,
        value: Optional[str] = None,
    ) -> Request:
        """Modifies the nvt preferences of an existing scan config.

        Args:
            config_id: UUID of scan config to modify.
            name: Name for nvt preference to change.
            nvt_oid: OID of the NVT associated with preference to modify
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        if not config_id:
            raise RequiredArgument(
                function=cls.modify_scan_config_set_nvt_preference.__name__,
                argument="config_id",
            )

        if not nvt_oid:
            raise RequiredArgument(
                function=cls.modify_scan_config_set_nvt_preference.__name__,
                argument="nvt_oid",
            )

        if not name:
            raise RequiredArgument(
                function=cls.modify_scan_config_set_nvt_preference.__name__,
                argument="name",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        xml_preference = cmd.add_element("preference")

        xml_preference.add_element("nvt", attrs={"oid": str(nvt_oid)})
        xml_preference.add_element("name", name)

        if value:
            xml_preference.add_element("value", to_base64(value))

        return cmd

    @classmethod
    def modify_scan_config_set_name(
        cls, config_id: EntityID, name: str
    ) -> Request:
        """Modifies the name of an existing scan config

        Args:
            config_id: UUID of scan config to modify.
            name: New name for the config.
        """
        if not config_id:
            raise RequiredArgument(
                function=cls.modify_scan_config_set_name.__name__,
                argument="config_id",
            )

        if not name:
            raise RequiredArgument(
                function=cls.modify_scan_config_set_name.__name__,
                argument="name",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        cmd.add_element("name", name)

        return cmd

    @classmethod
    def modify_scan_config_set_comment(
        cls, config_id: EntityID, *, comment: Optional[str] = None
    ) -> Request:
        """Modifies the comment of an existing scan config

        Args:
            config_id: UUID of scan config to modify.
            comment: Comment to set on a config. Default is an
                empty comment and the previous comment will be
                removed.
        """
        if not config_id:
            raise RequiredArgument(
                function=cls.modify_scan_config_set_comment.__name__,
                argument="config_id argument",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        if not comment:
            comment = ""

        cmd.add_element("comment", comment)

        return cmd

    @classmethod
    def modify_scan_config_set_scanner_preference(
        cls,
        config_id: EntityID,
        name: str,
        *,
        value: Optional[str] = None,
    ) -> Request:
        """Modifies the scanner preferences of an existing scan config

        Args:
            config_id: UUID of scan config to modify.
            name: Name of the scanner preference to change
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        if not config_id:
            raise RequiredArgument(
                function=(
                    cls.modify_scan_config_set_scanner_preference.__name__
                ),
                argument="config_id",
            )

        if not name:
            raise RequiredArgument(
                function=(
                    cls.modify_scan_config_set_scanner_preference.__name__
                ),
                argument="name argument",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        xml_preference = cmd.add_element("preference")

        xml_preference.add_element("name", name)

        if value:
            xml_preference.add_element("value", to_base64(value))

        return cmd

    @classmethod
    def modify_scan_config_set_nvt_selection(
        cls,
        config_id: EntityID,
        family: str,
        nvt_oids: Union[tuple[str], list[str]],
    ) -> Request:
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
                function=cls.modify_scan_config_set_nvt_selection.__name__,
                argument="config_id",
            )

        if not family:
            raise RequiredArgument(
                function=cls.modify_scan_config_set_nvt_selection.__name__,
                argument="family argument",
            )

        if not is_list_like(nvt_oids):
            raise InvalidArgumentType(
                function=cls.modify_scan_config_set_nvt_selection.__name__,
                argument="nvt_oids",
                arg_type="list",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        xmlnvtsel = cmd.add_element("nvt_selection")
        xmlnvtsel.add_element("family", family)

        for nvt in nvt_oids:
            xmlnvtsel.add_element("nvt", attrs={"oid": nvt})

        return cmd

    @classmethod
    def modify_scan_config_set_family_selection(
        cls,
        config_id: EntityID,
        families: list[tuple[str, bool, bool]],
        *,
        auto_add_new_families: Optional[bool] = True,
    ) -> Request:
        """
        Selected the NVTs of a scan config at a family level.

        Args:
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
                function=cls.modify_scan_config_set_family_selection.__name__,
                argument="config_id",
            )

        if not is_list_like(families):
            raise InvalidArgumentType(
                function=cls.modify_scan_config_set_family_selection.__name__,
                argument="families",
                arg_type="list",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(config_id))

        xml_family_selection = cmd.add_element("family_selection")
        xml_family_selection.add_element(
            "growing", to_bool(auto_add_new_families)
        )

        for family in families:
            xml_family = xml_family_selection.add_element("family")
            xml_family.add_element("name", family[0])

            if len(family) != 3:
                raise InvalidArgument(
                    "Family must be a tuple of 3. (str, bool, bool)"
                )

            if not isinstance(family[1], bool) or not isinstance(
                family[2], bool
            ):
                raise InvalidArgumentType(
                    function=(
                        cls.modify_scan_config_set_family_selection.__name__
                    ),
                    argument="families",
                    arg_type="[tuple(str, bool, bool)]",
                )

            xml_family.add_element("all", to_bool(family[2]))
            xml_family.add_element("growing", to_bool(family[1]))

        return cmd
