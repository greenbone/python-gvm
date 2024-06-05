# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm._enum import Enum
from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class TicketStatus(Enum):
    """Enum for ticket status"""

    OPEN = "Open"
    FIXED = "Fixed"
    CLOSED = "Closed"


class Tickets:

    @classmethod
    def clone_ticket(cls, ticket_id: EntityID) -> Request:
        """Clone an existing ticket

        Args:
            ticket_id: UUID of an existing ticket to clone from
        """
        if not ticket_id:
            raise RequiredArgument(
                function=cls.clone_ticket.__name__, argument="ticket_id"
            )

        cmd = XmlCommand("create_ticket")

        cmd.add_element("copy", str(ticket_id))

        return cmd

    @classmethod
    def create_ticket(
        cls,
        *,
        result_id: EntityID,
        assigned_to_user_id: EntityID,
        note: str,
        comment: Optional[str] = None,
    ) -> Request:
        """Create a new ticket

        Args:
            result_id: UUID of the result the ticket applies to
            assigned_to_user_id: UUID of a user the ticket should be assigned to
            note: A note about opening the ticket
            comment: Comment for the ticket
        """
        if not result_id:
            raise RequiredArgument(
                function=cls.create_ticket.__name__, argument="result_id"
            )

        if not assigned_to_user_id:
            raise RequiredArgument(
                function=cls.create_ticket.__name__,
                argument="assigned_to_user_id",
            )

        if not note:
            raise RequiredArgument(
                function=cls.create_ticket.__name__, argument="note"
            )

        cmd = XmlCommand("create_ticket")

        result = cmd.add_element("result")
        result.set_attribute("id", str(result_id))

        assigned = cmd.add_element("assigned_to")
        user = assigned.add_element("user")
        user.set_attribute("id", str(assigned_to_user_id))

        cmd.add_element("open_note", note)

        if comment:
            cmd.add_element("comment", comment)

        return cmd

    @classmethod
    def delete_ticket(
        cls, ticket_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Deletes an existing ticket

        Args:
            ticket_id: UUID of the ticket to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not ticket_id:
            raise RequiredArgument(
                function=cls.delete_ticket.__name__, argument="ticket_id"
            )

        cmd = XmlCommand("delete_ticket")
        cmd.set_attribute("ticket_id", str(ticket_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @staticmethod
    def get_tickets(
        *,
        trash: Optional[bool] = None,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
    ) -> Request:
        """Request a list of tickets

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: True to request the tickets in the trashcan
        """
        cmd = XmlCommand("get_tickets")

        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return cmd

    @classmethod
    def get_ticket(cls, ticket_id: EntityID) -> Request:
        """Request a single ticket

        Args:
            ticket_id: UUID of an existing ticket
        """
        if not ticket_id:
            raise RequiredArgument(
                function=cls.get_ticket.__name__, argument="ticket_id"
            )

        cmd = XmlCommand("get_tickets")
        cmd.set_attribute("ticket_id", str(ticket_id))
        return cmd

    @classmethod
    def modify_ticket(
        cls,
        ticket_id: EntityID,
        *,
        status: Optional[Union[TicketStatus, str]] = None,
        note: Optional[str] = None,
        assigned_to_user_id: Optional[EntityID] = None,
        comment: Optional[str] = None,
    ) -> Request:
        """Modify a single ticket

        Args:
            ticket_id: UUID of an existing ticket
            status: New status for the ticket
            note: Note for the status change. Required if status is set.
            assigned_to_user_id: UUID of the user the ticket should be assigned
                to
            comment: Comment for the ticket
        """
        if not ticket_id:
            raise RequiredArgument(
                function=cls.modify_ticket.__name__, argument="ticket_id"
            )

        if status and not note:
            raise RequiredArgument(
                function=cls.modify_ticket.__name__, argument="note"
            )

        if note and not status:
            raise RequiredArgument(
                function=cls.modify_ticket.__name__, argument="status"
            )

        cmd = XmlCommand("modify_ticket")
        cmd.set_attribute("ticket_id", str(ticket_id))

        if assigned_to_user_id:
            assigned = cmd.add_element("assigned_to")
            user = assigned.add_element("user")
            user.set_attribute("id", str(assigned_to_user_id))

        if status:
            if not isinstance(status, TicketStatus):
                status = TicketStatus(status)

            cmd.add_element("status", status.value)
            cmd.add_element(f"{status.name.lower()}_note", note)

        if comment:
            cmd.add_element("comment", comment)

        return cmd
