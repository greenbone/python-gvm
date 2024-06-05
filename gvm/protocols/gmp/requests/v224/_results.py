# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class Results:

    @classmethod
    def get_result(cls, result_id: EntityID) -> Request:
        """Request a single result

        Args:
            result_id: UUID of an existing result
        """
        cmd = XmlCommand("get_results")

        if not result_id:
            raise RequiredArgument(
                function=cls.get_result.__name__, argument="result_id"
            )

        cmd.set_attribute("result_id", str(result_id))

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return cmd

    @staticmethod
    def get_results(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        task_id: Optional[str] = None,
        note_details: Optional[bool] = None,
        override_details: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of results

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            task_id: UUID of task for note and override handling
            note_details: If notes are included, whether to include note details
            override_details: If overrides are included, whether to include
                override details
            details: Whether to include additional details of the results
        """
        cmd = XmlCommand("get_results")

        cmd.add_filter(filter_string, filter_id)

        if task_id:
            cmd.set_attribute("task_id", task_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if note_details is not None:
            cmd.set_attribute("note_details", to_bool(note_details))

        if override_details is not None:
            cmd.set_attribute("override_details", to_bool(override_details))

        return cmd
