# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import check_port, to_bool, to_comma_list
from gvm.xml import XmlCommand

from .._entity_id import EntityID
from ._severity import Severity


class Overrides:

    @classmethod
    def create_override(
        cls,
        text: str,
        nvt_oid: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[list[str]] = None,
        port: Optional[str] = None,
        result_id: Optional[EntityID] = None,
        severity: Optional[Severity] = None,
        new_severity: Optional[Severity] = None,
        task_id: Optional[EntityID] = None,
    ) -> Request:
        """Create a new override

        Args:
            text: Text of the new override
            nvt_id: OID of the nvt to which override applies
            days_active: Days override will be active. -1 on always, 0 off
            hosts: A list of host addresses
            port: Port to which the override applies, needs to be a string
                  in the form {number}/{protocol}
            result_id: UUID of a result to which override applies
            severity: Severity to which override applies
            new_severity: New severity for result
            task_id: UUID of task to which override applies
        """
        if not text:
            raise RequiredArgument(
                function=cls.create_override.__name__, argument="text"
            )

        if not nvt_oid:
            raise RequiredArgument(
                function=cls.create_override.__name__, argument="nvt_oid"
            )

        cmd = XmlCommand("create_override")
        cmd.add_element("text", text)
        cmd.add_element("nvt", attrs={"oid": nvt_oid})

        if days_active is not None:
            cmd.add_element("active", str(days_active))

        if hosts:
            cmd.add_element("hosts", to_comma_list(hosts))

        if port:
            if check_port(port):
                cmd.add_element("port", port)
            else:
                raise InvalidArgument(
                    function=cls.create_override.__name__, argument="port"
                )

        if result_id:
            cmd.add_element("result", attrs={"id": result_id})

        if severity is not None:
            cmd.add_element("severity", str(severity))

        if new_severity is not None:
            cmd.add_element("new_severity", str(new_severity))

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})

        return cmd

    @classmethod
    def modify_override(
        cls,
        override_id: EntityID,
        text: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[list[str]] = None,
        port: Optional[str] = None,
        result_id: Optional[EntityID] = None,
        severity: Optional[Severity] = None,
        new_severity: Optional[Severity] = None,
        task_id: Optional[EntityID] = None,
    ) -> Request:
        """Modify an existing override.

        Args:
            override_id: UUID of override to modify.
            text: The text of the override.
            days_active: Days override will be active. -1 on always,
                0 off.
            hosts: A list of host addresses
            port: Port to which the override applies, needs to be a string
                  in the form {number}/{protocol}
            result_id: Result to which override applies.
            severity: Severity to which override applies.
            new_severity: New severity score for result.
            task_id: Task to which override applies.
        """
        if not override_id:
            raise RequiredArgument(
                function=cls.modify_override.__name__, argument="override_id"
            )

        if not text:
            raise RequiredArgument(
                function=cls.modify_override.__name__, argument="text"
            )

        cmd = XmlCommand("modify_override")
        cmd.set_attribute("override_id", str(override_id))
        cmd.add_element("text", text)

        if days_active is not None:
            cmd.add_element("active", str(days_active))

        if hosts:
            cmd.add_element("hosts", to_comma_list(hosts))

        if port:
            if check_port(port):
                cmd.add_element("port", str(port))
            else:
                raise InvalidArgument(
                    function=cls.modify_override.__name__, argument="port"
                )

        if result_id:
            cmd.add_element("result", attrs={"id": str(result_id)})

        if severity is not None:
            cmd.add_element("severity", str(severity))

        if new_severity is not None:
            cmd.add_element("new_severity", str(new_severity))

        if task_id:
            cmd.add_element("task", attrs={"id": str(task_id)})

        return cmd

    @classmethod
    def clone_override(cls, override_id: EntityID) -> Request:
        """Clone an existing override

        Args:
            override_id: UUID of an existing override to clone from
        """
        if not override_id:
            raise RequiredArgument(
                function=cls.clone_override.__name__, argument="override_id"
            )

        cmd = XmlCommand("create_override")
        cmd.add_element("copy", str(override_id))
        return cmd

    @classmethod
    def delete_override(
        cls, override_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Delete an existing override

        Args:
            override_id: UUID of an existing override to delete
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not override_id:
            raise RequiredArgument(
                function=cls.delete_override.__name__, argument="override_id"
            )

        cmd = XmlCommand("delete_override")
        cmd.set_attribute("override_id", str(override_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))
        return cmd

    @staticmethod
    def get_overrides(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
        result: Optional[bool] = None,
    ) -> Request:
        """Request a list of overrides

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include full details
            result: Whether to include results using the override
        """
        cmd = XmlCommand("get_overrides")
        cmd.add_filter(filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if result is not None:
            cmd.set_attribute("result", to_bool(result))

        return cmd

    @classmethod
    def get_override(cls, override_id: EntityID) -> Request:
        """Request a single override

        Args:
            override_id: UUID of an existing override
        """
        cmd = XmlCommand("get_overrides")

        if not override_id:
            raise RequiredArgument(
                function=cls.get_override.__name__, argument="override_id"
            )

        cmd.set_attribute("override_id", str(override_id))

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return cmd
