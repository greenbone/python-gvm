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


class Notes:
    @classmethod
    def create_note(
        cls,
        text: str,
        nvt_oid: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[list[str]] = None,
        port: Optional[str] = None,
        result_id: Optional[EntityID] = None,
        severity: Optional[Severity] = None,
        task_id: Optional[EntityID] = None,
    ) -> Request:
        """Create a new note

        Args:
            text: Text of the new note
            nvt_id: OID of the nvt to which note applies
            days_active: Days note will be active. -1 on
                always, 0 off
            hosts: A list of host addresses
            port: Port to which the override applies, needs to be a string
                  in the form {number}/{protocol}
            result_id: UUID of a result to which note applies
            severity: Severity to which note applies
            task_id: UUID of task to which note applies
        """
        if not text:
            raise RequiredArgument(
                function=cls.create_note.__name__, argument="text"
            )

        if not nvt_oid:
            raise RequiredArgument(
                function=cls.create_note.__name__, argument="nvt_oid"
            )

        cmd = XmlCommand("create_note")
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
                    function=cls.create_note.__name__, argument="port"
                )

        if result_id:
            cmd.add_element("result", attrs={"id": str(result_id)})

        if severity is not None:
            cmd.add_element("severity", str(severity))

        if task_id:
            cmd.add_element("task", attrs={"id": str(task_id)})

        return cmd

    @classmethod
    def modify_note(
        cls,
        note_id: EntityID,
        text: str,
        *,
        days_active: Optional[int] = None,
        hosts: Optional[list[str]] = None,
        port: Optional[str] = None,
        result_id: Optional[EntityID] = None,
        severity: Optional[Severity] = None,
        task_id: Optional[EntityID] = None,
    ) -> Request:
        """Modify a note

        Args:
            note_id: The UUID of the note to modify
            text: Text of the note
            days_active: Days note will be active. -1 on always, 0 off
            hosts: A list of host addresses
            port: Port to which the override applies, needs to be a string
                  in the form {number}/{protocol}
            result_id: UUID of a result to which note applies
            severity: Severity to which note applies
            task_id: UUID of task to which note applies
        """
        if not note_id:
            raise RequiredArgument(
                function=cls.modify_note.__name__, argument="note_id"
            )

        if not text:
            raise RequiredArgument(
                function=cls.modify_note.__name__, argument="text"
            )

        cmd = XmlCommand("modify_note")
        cmd.set_attribute("note_id", str(note_id))
        cmd.add_element("text", text)

        if days_active is not None:
            cmd.add_element("active", str(days_active))

        if hosts:
            cmd.add_element("hosts", to_comma_list(hosts))

        if port:
            if check_port(port):
                cmd.add_element("port", port)
            else:
                raise InvalidArgument(
                    function=cls.modify_note.__name__, argument="port"
                )

        if result_id:
            cmd.add_element("result", attrs={"id": str(result_id)})

        if severity is not None:
            cmd.add_element("severity", str(severity))

        if task_id:
            cmd.add_element("task", attrs={"id": str(task_id)})

        return cmd

    @classmethod
    def clone_note(cls, note_id: EntityID) -> Request:
        """Clone an existing note

        Args:
            note_id: UUID of an existing note to clone from
        """
        if not note_id:
            raise RequiredArgument(
                function=cls.clone_note.__name__, argument="note_id"
            )

        cmd = XmlCommand("create_note")
        cmd.add_element("copy", str(note_id))
        return cmd

    @classmethod
    def delete_note(
        cls, note_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Delete an existing note

        Args:
            note_id: UUID of the note to be deleted.
            ultimate: Whether to remove entirely or to the trashcan.
        """
        if not note_id:
            raise RequiredArgument(
                function=cls.delete_note.__name__, argument="note_id"
            )

        cmd = XmlCommand("delete_note")
        cmd.set_attribute("note_id", str(note_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))
        return cmd

    @classmethod
    def get_notes(
        cls,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        details: Optional[bool] = None,
        result: Optional[bool] = None,
    ) -> Request:
        """Request a list of notes

        Args:
            filter_string: Filter notes by a string
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Add info about connected results and tasks
            result: Return the details of possible connected results.
        """
        cmd = XmlCommand("get_notes")
        cmd.add_filter(filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if result is not None:
            cmd.set_attribute("result", to_bool(result))

        return cmd

    @classmethod
    def get_note(cls, note_id: EntityID) -> Request:
        """Request a single note

        Arguments:
            note_id: UUID of an existing note
        """
        if not note_id:
            raise RequiredArgument(
                function=cls.get_note.__name__, argument="note_id"
            )

        cmd = XmlCommand("get_notes")
        cmd.set_attribute("note_id", str(note_id))

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return cmd
