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

from enum import Enum
from typing import Any, Optional

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class TicketStatus(Enum):
    """Enum for ticket status"""

    OPEN = "Open"
    FIXED = "Fixed"
    CLOSED = "Closed"

    @classmethod
    def from_string(
        cls,
        ticket_status: Optional[str],
    ) -> Optional["TicketStatus"]:
        """Convert a ticket status string into a TicketStatus instance"""
        if not ticket_status:
            return None

        try:
            return cls[ticket_status.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="ticket_status",
                function=cls.from_string.__name__,
            ) from None


class TicketsMixin:
    def clone_ticket(self, ticket_id: str) -> Any:
        """Clone an existing ticket

        Arguments:
            ticket_id: UUID of an existing ticket to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not ticket_id:
            raise RequiredArgument(
                function=self.clone_ticket.__name__, argument="ticket_id"
            )

        cmd = XmlCommand("create_ticket")

        _copy = cmd.add_element("copy", ticket_id)

        return self._send_xml_command(cmd)

    def create_ticket(
        self,
        *,
        result_id: str,
        assigned_to_user_id: str,
        note: str,
        comment: Optional[str] = None,
    ) -> Any:
        """Create a new ticket

        Arguments:
            result_id: UUID of the result the ticket applies to
            assigned_to_user_id: UUID of a user the ticket should be assigned to
            note: A note about opening the ticket
            comment: Comment for the ticket

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not result_id:
            raise RequiredArgument(
                function=self.create_ticket.__name__, argument="result_id"
            )

        if not assigned_to_user_id:
            raise RequiredArgument(
                function=self.create_ticket.__name__,
                argument="assigned_to_user_id",
            )

        if not note:
            raise RequiredArgument(
                function=self.create_ticket.__name__, argument="note"
            )

        cmd = XmlCommand("create_ticket")

        _result = cmd.add_element("result")
        _result.set_attribute("id", result_id)

        _assigned = cmd.add_element("assigned_to")
        _user = _assigned.add_element("user")
        _user.set_attribute("id", assigned_to_user_id)

        _note = cmd.add_element("open_note", note)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def delete_ticket(
        self, ticket_id: str, *, ultimate: Optional[bool] = False
    ):
        """Deletes an existing ticket

        Arguments:
            ticket_id: UUID of the ticket to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not ticket_id:
            raise RequiredArgument(
                function=self.delete_ticket.__name__, argument="ticket_id"
            )

        cmd = XmlCommand("delete_ticket")
        cmd.set_attribute("ticket_id", ticket_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_tickets(
        self,
        *,
        trash: Optional[bool] = None,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
    ) -> Any:
        """Request a list of tickets

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: True to request the tickets in the trashcan

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tickets")

        add_filter(cmd, filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_ticket(self, ticket_id: str) -> Any:
        """Request a single ticket

        Arguments:
            ticket_id: UUID of an existing ticket

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not ticket_id:
            raise RequiredArgument(
                function=self.get_ticket.__name__, argument="ticket_id"
            )

        cmd = XmlCommand("get_tickets")
        cmd.set_attribute("ticket_id", ticket_id)
        return self._send_xml_command(cmd)

    def modify_ticket(
        self,
        ticket_id: str,
        *,
        status: Optional[TicketStatus] = None,
        note: Optional[str] = None,
        assigned_to_user_id: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Modify a single ticket

        Arguments:
            ticket_id: UUID of an existing ticket
            status: New status for the ticket
            note: Note for the status change. Required if status is set.
            assigned_to_user_id: UUID of the user the ticket should be assigned
                to
            comment: Comment for the ticket

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not ticket_id:
            raise RequiredArgument(
                function=self.modify_ticket.__name__, argument="ticket_id"
            )

        if status and not note:
            raise RequiredArgument(
                function=self.modify_ticket.__name__, argument="note"
            )

        if note and not status:
            raise RequiredArgument(
                function=self.modify_ticket.__name__, argument="status"
            )

        cmd = XmlCommand("modify_ticket")
        cmd.set_attribute("ticket_id", ticket_id)

        if assigned_to_user_id:
            _assigned = cmd.add_element("assigned_to")
            _user = _assigned.add_element("user")
            _user.set_attribute("id", assigned_to_user_id)

        if status:
            if not isinstance(status, TicketStatus):
                raise InvalidArgumentType(
                    function=self.modify_ticket.__name__,
                    argument="status",
                    arg_type=TicketStatus.__name__,
                )

            cmd.add_element("status", status.value)
            cmd.add_element(f"{status.name.lower()}_note", note)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)
