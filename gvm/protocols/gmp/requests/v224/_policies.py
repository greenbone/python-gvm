# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Sequence

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_base64, to_bool
from gvm.xml import XmlCommand, XmlError

from .._entity_id import EntityID

_EMPTY_POLICY_ID = "085569ce-73ed-11df-83c3-002264764cea"


class Policies:

    @classmethod
    def clone_policy(cls, policy_id: EntityID) -> Request:
        """Clone a policy from an existing one

        Args:
            policy_id: UUID of the existing policy
        """
        if not policy_id:
            raise RequiredArgument(
                function=cls.clone_policy.__name__, argument="policy_id"
            )

        cmd = XmlCommand("create_config")
        cmd.add_element("copy", str(policy_id))
        return cmd

    @classmethod
    def create_policy(
        cls,
        name: str,
        *,
        policy_id: Optional[EntityID] = None,
        comment: Optional[str] = None,
    ) -> Request:
        """Create a new policy

        Args:
            name: Name of the new policy
            policy_id: UUID of an existing policy as base. By default the empty
                policy is used.
            comment: A comment on the policy
        """
        cmd = XmlCommand("create_config")

        if policy_id is None:
            policy_id = _EMPTY_POLICY_ID
        if not name:
            raise RequiredArgument(
                function=cls.create_policy.__name__, argument="name"
            )

        if comment is not None:
            cmd.add_element("comment", comment)

        cmd.add_element("copy", str(policy_id))
        cmd.add_element("name", name)
        cmd.add_element("usage_type", "policy")

        return cmd

    @classmethod
    def delete_policy(
        cls, policy_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Deletes an existing policy

        Args:
            policy_id: UUID of the policy to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not policy_id:
            raise RequiredArgument(
                function=cls.delete_policy.__name__, argument="policy_id"
            )

        cmd = XmlCommand("delete_config")
        cmd.set_attribute("config_id", str(policy_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @staticmethod
    def get_policies(
        *,
        audits: Optional[bool] = None,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
        families: Optional[bool] = None,
        preferences: Optional[bool] = None,
        trash: Optional[bool] = None,
    ) -> Request:
        """Request a list of policies

        Args:
            audits: Whether to get audits using the policy
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to get  families, preferences, nvt selectors
                and tasks.
            families: Whether to include the families if no details are
                requested
            preferences: Whether to include the preferences if no details are
                requested
            trash: Whether to get the trashcan audits instead
        """
        cmd = XmlCommand("get_configs")
        cmd.set_attribute("usage_type", "policy")

        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if families is not None:
            cmd.set_attribute("families", to_bool(families))

        if preferences is not None:
            cmd.set_attribute("preferences", to_bool(preferences))

        if audits is not None:
            cmd.set_attribute("tasks", to_bool(audits))

        return cmd

    @classmethod
    def get_policy(
        cls, policy_id: EntityID, *, audits: Optional[bool] = None
    ) -> Request:
        """Request a single policy

        Args:
            policy_id: UUID of an existing policy
            audits: Whether to get audits using this policy
        """
        if not policy_id:
            raise RequiredArgument(
                function=cls.get_policy.__name__, argument="policy_id"
            )

        cmd = XmlCommand("get_configs")
        cmd.set_attribute("config_id", str(policy_id))

        cmd.set_attribute("usage_type", "policy")

        if audits is not None:
            cmd.set_attribute("tasks", to_bool(audits))

        # for single entity always request all details
        cmd.set_attribute("details", "1")

        return cmd

    @classmethod
    def import_policy(cls, policy: str) -> Request:
        """Import a policy from XML

        Args:
            policy: Policy XML as string to import. This XML must
                contain a :code:`<get_configs_response>` root element.
        """
        if not policy:
            raise RequiredArgument(
                function=cls.import_policy.__name__, argument="policy"
            )

        cmd = XmlCommand("create_config")

        try:
            cmd.append_xml_str(policy)
        except XmlError as e:
            raise InvalidArgument(
                function=cls.import_policy.__name__, argument="policy"
            ) from e

        return cmd

    @classmethod
    def modify_policy_set_nvt_preference(
        cls,
        policy_id: EntityID,
        name: str,
        nvt_oid: str,
        *,
        value: Optional[str] = None,
    ) -> Request:
        """Modifies the nvt preferences of an existing policy.

        Args:
            policy_id: UUID of policy to modify.
            name: Name for preference to change.
            nvt_oid: OID of the NVT associated with preference to modify
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        if not policy_id:
            raise RequiredArgument(
                function=cls.modify_policy_set_nvt_preference.__name__,
                argument="policy_id",
            )

        if not nvt_oid:
            raise RequiredArgument(
                function=cls.modify_policy_set_nvt_preference.__name__,
                argument="nvt_oid",
            )

        if not name:
            raise RequiredArgument(
                function=cls.modify_policy_set_nvt_preference.__name__,
                argument="name",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(policy_id))

        xml_pref = cmd.add_element("preference")

        xml_pref.add_element("nvt", attrs={"oid": nvt_oid})
        xml_pref.add_element("name", name)

        if value:
            xml_pref.add_element("value", to_base64(value))

        return cmd

    @classmethod
    def modify_policy_set_name(cls, policy_id: EntityID, name: str) -> Request:
        """Modifies the name of an existing policy

        Args:
            policy_id: UUID of policy to modify.
            name: New name for the policy.
        """
        if not policy_id:
            raise RequiredArgument(
                function=cls.modify_policy_set_name.__name__,
                argument="policy_id",
            )

        if not name:
            raise RequiredArgument(
                function=cls.modify_policy_set_name.__name__,
                argument="name",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(policy_id))

        cmd.add_element("name", name)

        return cmd

    @classmethod
    def modify_policy_set_comment(
        cls, policy_id: EntityID, comment: Optional[str] = None
    ) -> Request:
        """Modifies the comment of an existing policy

        Args:
            policy_id: UUID of policy to modify.
            comment: Comment to set on a policy. Default is an
                empty comment and the previous comment will be
                removed.
        """
        if not policy_id:
            raise RequiredArgument(
                function=cls.modify_policy_set_comment.__name__,
                argument="policy_id",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(policy_id))
        if not comment:
            comment = ""
        cmd.add_element("comment", comment)

        return cmd

    @classmethod
    def modify_policy_set_scanner_preference(
        cls, policy_id: EntityID, name: str, *, value: Optional[str] = None
    ) -> Request:
        """Modifies the scanner preferences of an existing policy

        Args:
            policy_id: UUID of policy to modify.
            name: Name of the scanner preference to change
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        if not policy_id:
            raise RequiredArgument(
                function=cls.modify_policy_set_scanner_preference.__name__,
                argument="policy_id",
            )

        if not name:
            raise RequiredArgument(
                function=cls.modify_policy_set_scanner_preference.__name__,
                argument="name argument",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(policy_id))

        xml_pref = cmd.add_element("preference")

        xml_pref.add_element("name", name)

        if value:
            xml_pref.add_element("value", to_base64(value))

        return cmd

    @classmethod
    def modify_policy_set_nvt_selection(
        cls, policy_id: EntityID, family: str, nvt_oids: Sequence[str]
    ) -> Request:
        """Modifies the selected nvts of an existing policy

        The manager updates the given family in the policy to include only the
        given NVTs.

        Args:
            policy_id: UUID of policy to modify.
            family: Name of the NVT family to include NVTs from
            nvt_oids: List of NVTs to select for the family.
        """
        if not policy_id:
            raise RequiredArgument(
                function=cls.modify_policy_set_nvt_selection.__name__,
                argument="policy_id",
            )

        if not family:
            raise RequiredArgument(
                function=cls.modify_policy_set_nvt_selection.__name__,
                argument="family",
            )

        if nvt_oids is None:
            raise RequiredArgument(
                function=cls.modify_policy_set_nvt_selection.__name__,
                argument="nvt_oids",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(policy_id))

        xml_nvt_selection = cmd.add_element("nvt_selection")
        xml_nvt_selection.add_element("family", family)

        for nvt in nvt_oids:
            xml_nvt_selection.add_element("nvt", attrs={"oid": str(nvt)})

        return cmd

    @classmethod
    def modify_policy_set_family_selection(
        cls,
        policy_id: EntityID,
        families: Sequence[tuple[str, bool, bool]],
        *,
        auto_add_new_families: Optional[bool] = True,
    ) -> Request:
        """
        Selected the NVTs of a policy at a family level.

        Args:
            policy_id: UUID of policy to modify.
            families: A list of tuples with the first entry being the name
                of the NVT family selected, second entry a boolean indicating
                whether new NVTs should be added to the family automatically,
                and third entry a boolean indicating whether all nvts from
                the family should be included.
            auto_add_new_families: Whether new families should be added to the
                policy automatically. Default: True.
        """
        if not policy_id:
            raise RequiredArgument(
                function=cls.modify_policy_set_family_selection.__name__,
                argument="policy_id",
            )

        if families is None:
            raise RequiredArgument(
                function=cls.modify_policy_set_family_selection.__name__,
                argument="families",
            )

        cmd = XmlCommand("modify_config")
        cmd.set_attribute("config_id", str(policy_id))

        xml_family_selection = cmd.add_element("family_selection")
        xml_family_selection.add_element(
            "growing", to_bool(auto_add_new_families)
        )

        for family in families:
            xml_family = xml_family_selection.add_element("family")

            if len(family) != 3:
                raise InvalidArgument(
                    "Family must be a tuple of 3. (str, bool, bool)"
                )

            xml_family.add_element("name", family[0])
            xml_family.add_element("all", to_bool(family[2]))
            xml_family.add_element("growing", to_bool(family[1]))

        return cmd
