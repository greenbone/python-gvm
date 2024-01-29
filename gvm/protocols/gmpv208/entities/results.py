# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Any, Optional

from gvm.errors import RequiredArgument
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class ResultsMixin:
    def get_result(self, result_id: str) -> Any:
        """Request a single result

        Arguments:
            result_id: UUID of an existing result

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_results")

        if not result_id:
            raise RequiredArgument(
                function=self.get_result.__name__, argument="result_id"
            )

        cmd.set_attribute("result_id", result_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_results(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        task_id: Optional[str] = None,
        note_details: Optional[bool] = None,
        override_details: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of results

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            task_id: UUID of task for note and override handling
            note_details: If notes are included, whether to include note details
            override_details: If overrides are included, whether to include
                override details
            details: Whether to include additional details of the results

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_results")

        add_filter(cmd, filter_string, filter_id)

        if task_id:
            cmd.set_attribute("task_id", task_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))
        if note_details is not None:
            cmd.set_attribute("note_details", to_bool(note_details))

        if override_details is not None:
            cmd.set_attribute("override_details", to_bool(override_details))

        return self._send_xml_command(cmd)
