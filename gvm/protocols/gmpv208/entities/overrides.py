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

from typing import Any, List, Optional

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv208.entities.severity import Severity, SeverityLevel
from gvm.utils import add_filter, check_port, to_bool, to_comma_list
from gvm.xml import XmlCommand


class OverridesMixin:
    def create_override(
        self,
        text: str,
        nvt_oid: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[List[str]] = None,
        port: Optional[str] = None,
        result_id: Optional[str] = None,
        severity: Optional[Severity] = None,
        new_severity: Optional[Severity] = None,
        task_id: Optional[str] = None,
        threat: Optional[SeverityLevel] = None,
        new_threat: Optional[SeverityLevel] = None,
    ) -> Any:
        """Create a new override

        Arguments:
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
            threat: Severity level to which override applies. Will be converted
                to severity.
            new_threat: New severity level for results. Will be converted to
                new_severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not text:
            raise RequiredArgument(
                function=self.create_override.__name__, argument="text"
            )

        if not nvt_oid:
            raise RequiredArgument(
                function=self.create_override.__name__, argument="nvt_oid"
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
                cmd.add_element("port", str(port))
            else:
                raise InvalidArgument(
                    function=self.create_override.__name__, argument="port"
                )

        if result_id:
            cmd.add_element("result", attrs={"id": result_id})

        if severity is not None:
            cmd.add_element("severity", str(severity))

        if new_severity is not None:
            cmd.add_element("new_severity", str(new_severity))

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})

        if threat is not None:
            if not isinstance(threat, SeverityLevel):
                raise InvalidArgumentType(
                    function=self.create_override.__name__,
                    argument="threat",
                    arg_type=SeverityLevel.__name__,
                )

            cmd.add_element("threat", threat.value)

        if new_threat is not None:
            if not isinstance(new_threat, SeverityLevel):
                raise InvalidArgumentType(
                    function=self.create_override.__name__,
                    argument="new_threat",
                    arg_type=SeverityLevel.__name__,
                )

            cmd.add_element("new_threat", new_threat.value)

        return self._send_xml_command(cmd)

    def clone_override(self, override_id: str) -> Any:
        """Clone an existing override

        Arguments:
            override_id: UUID of an existing override to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not override_id:
            raise RequiredArgument(
                function=self.clone_override.__name__, argument="override_id"
            )

        cmd = XmlCommand("create_override")
        cmd.add_element("copy", override_id)
        return self._send_xml_command(cmd)

    def delete_override(
        self, override_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing override

        Arguments:
            override_id: UUID of the override to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not override_id:
            raise RequiredArgument(
                function=self.delete_override.__name__, argument="override_id"
            )

        cmd = XmlCommand("delete_override")
        cmd.set_attribute("override_id", override_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_overrides(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        details: Optional[bool] = None,
        result: Optional[bool] = None,
    ) -> Any:
        """Request a list of overrides

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include full details
            result: Whether to include results using the override

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_overrides")

        add_filter(cmd, filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if result is not None:
            cmd.set_attribute("result", to_bool(result))

        return self._send_xml_command(cmd)

    def get_override(self, override_id: str) -> Any:
        """Request a single override

        Arguments:
            override_id: UUID of an existing override

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_overrides")

        if not override_id:
            raise RequiredArgument(
                function=self.get_override.__name__, argument="override_id"
            )

        cmd.set_attribute("override_id", override_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def modify_override(
        self,
        override_id: str,
        text: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[List[str]] = None,
        port: Optional[str] = None,
        result_id: Optional[str] = None,
        severity: Optional[Severity] = None,
        new_severity: Optional[Severity] = None,
        task_id: Optional[str] = None,
        threat: Optional[SeverityLevel] = None,
        new_threat: Optional[SeverityLevel] = None,
    ) -> Any:
        """Modifies an existing override.

        Arguments:
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
            threat: Threat level to which override applies.
                Will be converted to severity.
            new_threat: New threat level for results. Will be converted to
                new_severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not override_id:
            raise RequiredArgument(
                function=self.modify_override.__name__, argument="override_id"
            )
        if not text:
            raise RequiredArgument(
                function=self.modify_override.__name__, argument="text"
            )

        cmd = XmlCommand("modify_override")
        cmd.set_attribute("override_id", override_id)
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
                    function=self.modify_override.__name__, argument="port"
                )

        if result_id:
            cmd.add_element("result", attrs={"id": result_id})

        if severity is not None:
            cmd.add_element("severity", str(severity))

        if new_severity is not None:
            cmd.add_element("new_severity", str(new_severity))

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})

        if threat is not None:
            if not isinstance(threat, SeverityLevel):
                raise InvalidArgumentType(
                    function=self.modify_override.__name__,
                    argument="threat",
                    arg_type=SeverityLevel.__name__,
                )
            cmd.add_element("threat", threat.value)

        if new_threat is not None:
            if not isinstance(new_threat, SeverityLevel):
                raise InvalidArgumentType(
                    function=self.modify_override.__name__,
                    argument="new_threat",
                    arg_type=SeverityLevel.__name__,
                )

            cmd.add_element("new_threat", new_threat.value)

        return self._send_xml_command(cmd)
