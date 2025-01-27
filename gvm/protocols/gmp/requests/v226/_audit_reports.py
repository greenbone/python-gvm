# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID
from ..v224._report_formats import ReportFormatType


class AuditReports:

    @classmethod
    def delete_report(cls, audit_report_id: EntityID) -> Request:
        """Deletes an existing audit report

        Args:
            audit_report_id: UUID of the report to be deleted.
        """
        if not audit_report_id:
            raise RequiredArgument(
                function=cls.delete_report.__name__, argument="audit_report_id"
            )

        cmd = XmlCommand("delete_report")
        cmd.set_attribute("report_id", str(audit_report_id))

        return cmd

    @classmethod
    def get_report(
        cls,
        report_id: EntityID,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        delta_report_id: Optional[EntityID] = None,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        ignore_pagination: Optional[bool] = None,
        details: Optional[bool] = True,
    ) -> Request:
        """Request a single audit report

        Args:
            report_id: UUID of an existing report
            filter_string: Filter term to use to filter results in the report
            filter_id: UUID of filter to use to filter results in the report
            delta_report_id: UUID of an existing audit report to compare report to.
            report_format_id: UUID of report format to use
                              or ReportFormatType (enum)
            ignore_pagination: Whether to ignore the filter terms "first" and
                "rows".
            details: Request additional report information details
                     defaults to True
        """
        cmd = XmlCommand("get_reports")

        if not report_id:
            raise RequiredArgument(
                function=cls.get_report.__name__, argument="report_id"
            )

        cmd.set_attribute("report_id", str(report_id))
        cmd.set_attribute("usage_type", "audit")

        cmd.add_filter(filter_string, filter_id)

        if delta_report_id:
            cmd.set_attribute("delta_report_id", str(delta_report_id))

        if report_format_id:
            cmd.set_attribute("format_id", str(report_format_id))

        if ignore_pagination is not None:
            cmd.set_attribute("ignore_pagination", to_bool(ignore_pagination))

        cmd.set_attribute("details", to_bool(details))

        return cmd

    @staticmethod
    def get_reports(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        note_details: Optional[bool] = None,
        override_details: Optional[bool] = None,
        ignore_pagination: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of audit reports

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            note_details: If notes are included, whether to include note details
            override_details: If overrides are included, whether to include
                override details
            ignore_pagination: Whether to ignore the filter terms "first" and
                "rows".
            details: Whether to exclude results
        """
        cmd = XmlCommand("get_reports")
        cmd.set_attribute("usage_type", "audit")

        if filter_string:
            cmd.set_attribute("report_filter", filter_string)

        if filter_id:
            cmd.set_attribute("report_filt_id", str(filter_id))

        if note_details is not None:
            cmd.set_attribute("note_details", to_bool(note_details))

        if override_details is not None:
            cmd.set_attribute("override_details", to_bool(override_details))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if ignore_pagination is not None:
            cmd.set_attribute("ignore_pagination", to_bool(ignore_pagination))

        return cmd
