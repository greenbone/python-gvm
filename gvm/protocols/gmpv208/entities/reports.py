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

from typing import Any, Optional, Union

from lxml.etree import XMLSyntaxError

from gvm.errors import InvalidArgument, RequiredArgument

# if I use latest, I get circular import :/
from gvm.protocols.gmpv208.entities.report_formats import ReportFormatType
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class ReportsMixin:
    def delete_report(self, report_id: str) -> Any:
        """Deletes an existing report

        Arguments:
            report_id: UUID of the report to be deleted.
        """
        if not report_id:
            raise RequiredArgument(
                function=self.delete_report.__name__, argument="report_id"
            )

        cmd = XmlCommand("delete_report")
        cmd.set_attribute("report_id", report_id)

        return self._send_xml_command(cmd)

    def get_report(
        self,
        report_id: str,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        delta_report_id: Optional[str] = None,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        ignore_pagination: Optional[bool] = None,
        details: Optional[bool] = True,
    ) -> Any:
        """Request a single report

        Arguments:
            report_id: UUID of an existing report
            filter_string: Filter term to use to filter results in the report
            filter_id: UUID of filter to use to filter results in the report
            delta_report_id: UUID of an existing report to compare report to.
            report_format_id: UUID of report format to use
                              or ReportFormatType (enum)
            ignore_pagination: Whether to ignore the filter terms "first" and
                "rows".
            details: Request additional report information details
                     defaults to True

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_reports")

        if not report_id:
            raise RequiredArgument(
                function=self.get_report.__name__, argument="report_id"
            )

        cmd.set_attribute("report_id", report_id)

        add_filter(cmd, filter_string, filter_id)

        if delta_report_id:
            cmd.set_attribute("delta_report_id", delta_report_id)

        if report_format_id:
            if isinstance(report_format_id, ReportFormatType):
                report_format_id = report_format_id.value

            cmd.set_attribute("format_id", report_format_id)

        if ignore_pagination is not None:
            cmd.set_attribute("ignore_pagination", to_bool(ignore_pagination))

        cmd.set_attribute("details", to_bool(details))

        return self._send_xml_command(cmd)

    def get_reports(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        note_details: Optional[bool] = None,
        override_details: Optional[bool] = None,
        ignore_pagination: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of reports

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            note_details: If notes are included, whether to include note details
            override_details: If overrides are included, whether to include
                override details
            ignore_pagination: Whether to ignore the filter terms "first" and
                "rows".
            details: Whether to exclude results

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_reports")

        if filter_string:
            cmd.set_attribute("report_filter", filter_string)

        if filter_id:
            cmd.set_attribute("report_filt_id", filter_id)

        if note_details is not None:
            cmd.set_attribute("note_details", to_bool(note_details))

        if override_details is not None:
            cmd.set_attribute("override_details", to_bool(override_details))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if ignore_pagination is not None:
            cmd.set_attribute("ignore_pagination", to_bool(ignore_pagination))

        return self._send_xml_command(cmd)

    def import_report(
        self,
        report: str,
        *,
        task_id: Optional[str] = None,
        in_assets: Optional[bool] = None,
    ) -> Any:
        """Import a Report from XML

        Arguments:
            report: Report XML as string to import. This XML must contain
                a :code:`<report>` root element.
            task_id: UUID of task to import report to
            in_asset: Whether to create or update assets using the report

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report:
            raise RequiredArgument(
                function=self.import_report.__name__, argument="report"
            )

        cmd = XmlCommand("create_report")

        if task_id:
            cmd.add_element("task", attrs={"id": task_id})
        else:
            raise RequiredArgument(
                function=self.import_report.__name__, argument="task_id"
            )

        if in_assets is not None:
            cmd.add_element("in_assets", to_bool(in_assets))

        try:
            cmd.append_xml_str(report)
        except XMLSyntaxError as e:
            raise InvalidArgument(
                f"Invalid xml passed as report to import_report {e}"
            ) from None

        return self._send_xml_command(cmd)
