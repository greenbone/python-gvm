# -*- coding: utf-8 -*-
# Copyright (C) 2021 Greenbone Networks GmbH
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

# pylint:  disable=redefined-builtin
# MAYBE we should change filter to filter_string (everywhere)


from typing import Any, List, Optional, Tuple

from gvm.errors import RequiredArgument
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand

_EMPTY_POLICY_ID = '085569ce-73ed-11df-83c3-002264764cea'


class PoliciesMixin:
    def clone_policy(self, policy_id: str) -> Any:
        """Clone a policy from an existing one

        Arguments:
            policy_id: UUID of the existing policy

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not policy_id:
            raise RequiredArgument(
                function=self.clone_policy.__name__, argument='policy_id'
            )

        cmd = XmlCommand("create_config")
        cmd.add_element("copy", policy_id)
        return self._send_xml_command(cmd)

    def create_policy(
        self, name: str, *, policy_id: str = None, comment: Optional[str] = None
    ) -> Any:
        """Create a new policy

        Arguments:
            name: Name of the new policy
            policy_id: UUID of an existing policy as base. By default the empty
                policy is used.
            comment: A comment on the policy

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("create_config")

        if policy_id is None:
            policy_id = _EMPTY_POLICY_ID
        if not name:
            raise RequiredArgument(
                function=self.create_policy.__name__, argument='name'
            )

        if comment is not None:
            cmd.add_element("comment", comment)
        cmd.add_element("copy", policy_id)
        cmd.add_element("name", name)
        cmd.add_element("usage_type", "policy")
        return self._send_xml_command(cmd)

    def delete_policy(
        self, policy_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing policy
        Arguments:
            policy_id: UUID of the policy to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not policy_id:
            raise RequiredArgument(
                function=self.delete_policy.__name__, argument='policy_id'
            )

        cmd = XmlCommand("delete_config")
        cmd.set_attribute("config_id", policy_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_policies(
        self,
        *,
        audits: Optional[bool] = None,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        details: Optional[bool] = None,
        families: Optional[bool] = None,
        preferences: Optional[bool] = None,
        trash: Optional[bool] = None,
    ) -> Any:
        """Request a list of policies

        Arguments:
            audits: Whether to get audits using the policy
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to get  families, preferences, nvt selectors
                and tasks.
            families: Whether to include the families if no details are
                requested
            preferences: Whether to include the preferences if no details are
                requested
            trash: Whether to get the trashcan audits instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_configs")
        cmd.set_attribute("usage_type", "policy")

        add_filter(cmd, filter, filter_id)

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

        return self._send_xml_command(cmd)

    def get_policy(
        self, policy_id: str, *, audits: Optional[bool] = None
    ) -> Any:
        """Request a single policy

        Arguments:
            policy_id: UUID of an existing policy
            audits: Whether to get audits using this policy

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not policy_id:
            raise RequiredArgument(
                function=self.get_policy.__name__, argument='policy_id'
            )

        cmd = XmlCommand("get_configs")
        cmd.set_attribute("config_id", policy_id)

        cmd.set_attribute("usage_type", "policy")

        if audits is not None:
            cmd.set_attribute("tasks", to_bool(audits))

        # for single entity always request all details
        cmd.set_attribute("details", "1")

        return self._send_xml_command(cmd)

    def modify_policy_set_nvt_preference(
        self,
        policy_id: str,
        name: str,
        nvt_oid: str,
        *,
        value: Optional[str] = None,
    ) -> Any:
        """Modifies the nvt preferences of an existing policy.

        Arguments:
            policy_id: UUID of policy to modify.
            name: Name for preference to change.
            nvt_oid: OID of the NVT associated with preference to modify
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        self.modify_scan_config_set_nvt_preference(
            config_id=policy_id, name=name, nvt_oid=nvt_oid, value=value
        )

    def modify_policy_set_name(self, policy_id: str, name: str) -> Any:
        """Modifies the name of an existing policy

        Arguments:
            policy_id: UUID of policy to modify.
            name: New name for the policy.
        """
        self.modify_scan_config_set_name(config_id=policy_id, name=name)

    def modify_policy_set_comment(
        self, policy_id: str, comment: Optional[str] = None
    ) -> Any:
        """Modifies the comment of an existing policy

        Arguments:
            policy_id: UUID of policy to modify.
            comment: Comment to set on a policy. Default is an
                empty comment and the previous comment will be
                removed.
        """
        self.modify_scan_config_set_comment(
            config_id=policy_id, comment=comment
        )

    def modify_policy_set_scanner_preference(
        self, policy_id: str, name: str, *, value: Optional[str] = None
    ) -> Any:
        """Modifies the scanner preferences of an existing policy

        Arguments:
            policy_id: UUID of policy to modify.
            name: Name of the scanner preference to change
            value: New value for the preference. None to delete the preference
                and to use the default instead.

        """
        self.modify_scan_config_set_scanner_preference(
            config_id=policy_id, name=name, value=value
        )

    def modify_policy_set_nvt_selection(
        self, policy_id: str, family: str, nvt_oids: List[str]
    ) -> Any:
        """Modifies the selected nvts of an existing policy

        The manager updates the given family in the policy to include only the
        given NVTs.

        Arguments:
            policy_id: UUID of policy to modify.
            family: Name of the NVT family to include NVTs from
            nvt_oids: List of NVTs to select for the family.
        """
        self.modify_scan_config_set_nvt_selection(
            config_id=policy_id, family=family, nvt_oids=nvt_oids
        )

    def modify_policy_set_family_selection(
        self,
        policy_id: str,
        families: List[Tuple[str, bool, bool]],
        *,
        auto_add_new_families: Optional[bool] = True,
    ) -> Any:
        """
        Selected the NVTs of a policy at a family level.

        Arguments:
            policy_id: UUID of policy to modify.
            families: A list of tuples with the first entry being the name
                of the NVT family selected, second entry a boolean indicating
                whether new NVTs should be added to the family automatically,
                and third entry a boolean indicating whether all nvts from
                the family should be included.
            auto_add_new_families: Whether new families should be added to the
                policy automatically. Default: True.
        """
        self.modify_scan_config_set_family_selection(
            config_id=policy_id,
            families=families,
            auto_add_new_families=auto_add_new_families,
        )
