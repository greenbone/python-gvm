# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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

# pylint: disable=arguments-differ, redefined-builtin, too-many-lines

"""
Module for communication with gvmd in
`Greenbone Management Protocol version 21.04`_

.. _Greenbone Management Protocol version 21.04:
    https://docs.greenbone.net/API/GMP/gmp-21.04.html
"""

from typing import Any, List, Optional, Callable
import numbers

from gvm.utils import deprecation
from gvm.xml import XmlCommand
from gvm.protocols.gmpv7.gmpv7 import _to_comma_list

from gvm.connections import GvmConnection
from gvm.errors import RequiredArgument

from gvm.protocols.base import GvmProtocol

from . import types
from .types import *  # pylint: disable=unused-wildcard-import, wildcard-import

_EMPTY_POLICY_ID = '085569ce-73ed-11df-83c3-002264764cea'

PROTOCOL_VERSION = (21, 4)

Severity = numbers.Real


class GmpV214Mixin(GvmProtocol):
    types = types

    def __init__(
        self,
        connection: GvmConnection,
        *,
        transform: Optional[Callable[[str], Any]] = None
    ):
        super().__init__(connection, transform=transform)

        # Is authenticated on gvmd
        self._authenticated = False

    def create_note(
        self,
        text: str,
        nvt_oid: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[List[str]] = None,
        port: Optional[int] = None,
        result_id: Optional[str] = None,
        severity: Optional[Severity] = None,
        task_id: Optional[str] = None,
        threat: Optional[SeverityLevel] = None
    ) -> Any:
        """Create a new note

        Arguments:
            text: Text of the new note
            nvt_id: OID of the nvt to which note applies
            days_active: Days note will be active. -1 on
                always, 0 off
            hosts: A list of hosts addresses
            port: Port to which the note applies
            result_id: UUID of a result to which note applies
            severity: Severity to which note applies
            task_id: UUID of task to which note applies
            threat: Severity level to which note applies. Will be converted to
                severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not text:
            raise RequiredArgument(
                function=self.create_note.__name__, argument='text'
            )

        if not nvt_oid:
            raise RequiredArgument(
                function=self.create_note.__name__, argument='nvt_oid'
            )

        cmd = XmlCommand("create_note")
        cmd.add_element("text", text)
        cmd.add_element("nvt", attrs={"oid": nvt_oid})

        if days_active is not None:
            cmd.add_element("active", str(days_active))

        if hosts:
            cmd.add_element("hosts", _to_comma_list(hosts))

        if port:
            cmd.add_element("port", str(port))

        if result_id:
            cmd.add_element("result", attrs={"id": result_id})

        if severity:
            cmd.add_element("severity", str(severity))

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})

        if threat is not None:
            deprecation(
                "The threat parameter has been removed in GMP"
                " version {}{}".format(
                    self.get_protocol_version()[0],
                    self.get_protocol_version()[1],
                )
            )

        return self._send_xml_command(cmd)

    def create_override(
        self,
        text: str,
        nvt_oid: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[List[str]] = None,
        port: Optional[int] = None,
        result_id: Optional[str] = None,
        severity: Optional[Severity] = None,
        new_severity: Optional[Severity] = None,
        task_id: Optional[str] = None,
        threat: Optional[SeverityLevel] = None,
        new_threat: Optional[SeverityLevel] = None
    ) -> Any:
        """Create a new override

        Arguments:
            text: Text of the new override
            nvt_id: OID of the nvt to which override applies
            days_active: Days override will be active. -1 on always, 0 off
            hosts: A list of host addresses
            port: Port to which the override applies
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
                function=self.create_override.__name__, argument='text'
            )

        if not nvt_oid:
            raise RequiredArgument(
                function=self.create_override.__name__, argument='nvt_oid'
            )

        cmd = XmlCommand("create_override")
        cmd.add_element("text", text)
        cmd.add_element("nvt", attrs={"oid": nvt_oid})

        if days_active is not None:
            cmd.add_element("active", str(days_active))

        if hosts:
            cmd.add_element("hosts", _to_comma_list(hosts))

        if port:
            cmd.add_element("port", str(port))

        if result_id:
            cmd.add_element("result", attrs={"id": result_id})

        if severity:
            cmd.add_element("severity", str(severity))

        if new_severity:
            cmd.add_element("new_severity", str(new_severity))

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})

        if threat is not None:
            deprecation(
                "The threat parameter has been removed in GMP"
                " version {}{}".format(
                    self.get_protocol_version()[0],
                    self.get_protocol_version()[1],
                )
            )

        if new_threat is not None:
            deprecation(
                "The new_threat parameter has been removed in GMP"
                " version {}{}".format(
                    self.get_protocol_version()[0],
                    self.get_protocol_version()[1],
                )
            )

        return self._send_xml_command(cmd)

    def modify_note(
        self,
        note_id: str,
        text: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[List[str]] = None,
        port: Optional[int] = None,
        result_id: Optional[str] = None,
        severity: Optional[Severity] = None,
        task_id: Optional[str] = None,
        threat: Optional[SeverityLevel] = None
    ) -> Any:
        """Modifies an existing note.

        Arguments:
            note_id: UUID of note to modify.
            text: The text of the note.
            days_active: Days note will be active. -1 on always, 0 off.
            hosts: A list of hosts addresses
            port: Port to which note applies.
            result_id: Result to which note applies.
            severity: Severity to which note applies.
            task_id: Task to which note applies.
            threat: Threat level to which note applies. Will be converted to
                severity.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not note_id:
            raise RequiredArgument(
                function=self.modify_note.__name__, argument='note_id'
            )

        if not text:
            raise RequiredArgument(
                function=self.modify_note.__name__, argument='text'
            )

        cmd = XmlCommand("modify_note")
        cmd.set_attribute("note_id", note_id)
        cmd.add_element("text", text)

        if days_active is not None:
            cmd.add_element("active", str(days_active))

        if hosts:
            cmd.add_element("hosts", _to_comma_list(hosts))

        if port:
            cmd.add_element("port", str(port))

        if result_id:
            cmd.add_element("result", attrs={"id": result_id})

        if severity:
            cmd.add_element("severity", str(severity))

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})

        if threat is not None:
            deprecation(
                "The threat parameter has been removed in GMP"
                " version {}{}".format(
                    self.get_protocol_version()[0],
                    self.get_protocol_version()[1],
                )
            )

        return self._send_xml_command(cmd)

    def modify_override(
        self,
        override_id: str,
        text: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[List[str]] = None,
        port: Optional[int] = None,
        result_id: Optional[str] = None,
        severity: Optional[Severity] = None,
        new_severity: Optional[Severity] = None,
        task_id: Optional[str] = None,
        threat: Optional[SeverityLevel] = None,
        new_threat: Optional[SeverityLevel] = None
    ) -> Any:
        """Modifies an existing override.

        Arguments:
            override_id: UUID of override to modify.
            text: The text of the override.
            days_active: Days override will be active. -1 on always,
                0 off.
            hosts: A list of host addresses
            port: Port to which override applies.
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
                function=self.modify_override.__name__, argument='override_id'
            )
        if not text:
            raise RequiredArgument(
                function=self.modify_override.__name__, argument='text'
            )

        cmd = XmlCommand("modify_override")
        cmd.set_attribute("override_id", override_id)
        cmd.add_element("text", text)

        if days_active is not None:
            cmd.add_element("active", str(days_active))

        if hosts:
            cmd.add_element("hosts", _to_comma_list(hosts))

        if port:
            cmd.add_element("port", str(port))

        if result_id:
            cmd.add_element("result", attrs={"id": result_id})

        if severity:
            cmd.add_element("severity", str(severity))

        if new_severity:
            cmd.add_element("new_severity", str(new_severity))

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})

        if threat is not None:
            deprecation(
                "The threat parameter has been removed in GMP"
                " version {}{}".format(
                    self.get_protocol_version()[0],
                    self.get_protocol_version()[1],
                )
            )

        if new_threat is not None:
            deprecation(
                "The new_threat parameter has been removed in GMP"
                " version {}{}".format(
                    self.get_protocol_version()[0],
                    self.get_protocol_version()[1],
                )
            )

        return self._send_xml_command(cmd)
