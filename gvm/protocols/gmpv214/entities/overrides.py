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

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmpv208.entities.overrides import (
    OverridesMixin as Gmp208OverridesMixin,
)
from gvm.protocols.gmpv208.entities.severity import Severity
from gvm.utils import check_port, deprecation, to_comma_list
from gvm.xml import XmlCommand


class OverridesMixin(Gmp208OverridesMixin):
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
        threat: Any = None,
        new_threat: Any = None,
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
            threat: deprecated
            new_threat: deprecated

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
            major, minor = self.get_protocol_version()
            deprecation(
                "The threat parameter has been removed in GMP"
                f" version {major}{minor}"
            )

        if new_threat is not None:
            major, minor = self.get_protocol_version()
            deprecation(
                "The new_threat parameter has been removed in GMP"
                f" version {major}{minor}"
            )

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
        threat: Any = None,
        new_threat: Any = None,
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
            threat: deprecated
            new_threat: deprecated

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
            major, minor = self.get_protocol_version()
            deprecation(
                "The threat parameter has been removed in GMP"
                f" version {major}{minor}"
            )

        if new_threat is not None:
            major, minor = self.get_protocol_version()
            deprecation(
                "The new_threat parameter has been removed in GMP"
                f" version {major}{minor}"
            )

        return self._send_xml_command(cmd)
