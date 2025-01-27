# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Greenbone Management Protocol (GMP) version 22.6
"""

from typing import Optional, Union

from .._protocol import T
from ._gmp225 import GMPv225
from .requests.v226 import (
    AuditReports,
    EntityID,
    ReportFormatType,
    Reports,
    ResourceNames,
    ResourceType,
)


class GMPv226(GMPv225[T]):
    """
    A class implementing the Greenbone Management Protocol (GMP) version 22.6

    Example:

        .. code-block:: python

            from gvm.protocols.gmp import GMPv226 as GMP

            with GMP(connection) as gmp:
                resp = gmp.get_tasks()
    """

    def __init__(self, *args, **kwargs):
        """
        Create a new GMPv226 instance.

        Args:
            connection: Connection to use to talk with the remote daemon. See
                :mod:`gvm.connections` for possible connection types.
            transform: Optional transform `callable`_ to convert response data.
                After each request the callable gets passed the plain response data
                which can be used to check the data and/or conversion into different
                representations like a xml dom.

                See :mod:`gvm.transforms` for existing transforms.

        .. _callable:
            https://docs.python.org/3/library/functions.html#callable
        """
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_protocol_version() -> tuple[int, int]:
        return (22, 6)

    def get_resource_names(
        self,
        resource_type: ResourceType,  # type: ignore[override]
        *,
        filter_string: Optional[str] = None,
    ) -> T:
        """Request a list of resource names and IDs

        Arguments:
            resource_type: Type must be either ALERT, CERT_BUND_ADV,
                CONFIG, CPE, CREDENTIAL, CVE, DFN_CERT_ADV, FILTER,
                GROUP, HOST, NOTE, NVT, OS, OVERRIDE, PERMISSION,
                PORT_LIST, REPORT_FORMAT, REPORT, REPORT_CONFIG, RESULT, ROLE,
                SCANNER, SCHEDULE, TARGET, TASK, TLS_CERTIFICATE
                or USER
            filter_string: Filter term to use for the query
        """
        return self._send_and_transform_command(
            ResourceNames.get_resource_names(
                resource_type, filter_string=filter_string
            )
        )

    def get_resource_name(
        self, resource_id: str, resource_type: ResourceType  # type: ignore[override]
    ) -> T:
        """Request a single resource name

        Arguments:
            resource_id: ID of an existing resource
            resource_type: Type must be either ALERT, CERT_BUND_ADV,
                CONFIG, CPE, CREDENTIAL, CVE, DFN_CERT_ADV, FILTER,
                GROUP, HOST, NOTE, NVT, OS, OVERRIDE, PERMISSION,
                PORT_LIST, REPORT_FORMAT, REPORT, REPORT_CONFIG, RESULT, ROLE,
                SCANNER, SCHEDULE, TARGET, TASK, TLS_CERTIFICATE
                or USER
        """
        return self._send_and_transform_command(
            ResourceNames.get_resource_name(resource_id, resource_type)
        )

    def delete_report(self, report_id: EntityID) -> T:
        """Deletes an existing scan report

        Args:
            report_id: UUID of the report to be deleted.
        """
        return self._send_and_transform_command(
            Reports.delete_report(report_id)
        )

    def get_report(
        self,
        report_id: EntityID,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        delta_report_id: Optional[EntityID] = None,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        ignore_pagination: Optional[bool] = None,
        details: Optional[bool] = True,
    ) -> T:
        """Request a single scan report

        Args:
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
        """
        return self._send_and_transform_command(
            Reports.get_report(
                report_id,
                filter_string=filter_string,
                filter_id=filter_id,
                delta_report_id=delta_report_id,
                report_format_id=report_format_id,
                ignore_pagination=ignore_pagination,
                details=details,
            )
        )

    def get_reports(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        note_details: Optional[bool] = None,
        override_details: Optional[bool] = None,
        ignore_pagination: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> T:
        """Request a list of scan reports

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
        return self._send_and_transform_command(
            Reports.get_reports(
                filter_string=filter_string,
                filter_id=filter_id,
                note_details=note_details,
                override_details=override_details,
                ignore_pagination=ignore_pagination,
                details=details,
            )
        )

    def import_report(
        self,
        report: str,
        task_id: EntityID,
        *,
        in_assets: Optional[bool] = None,
    ) -> T:
        """Import a scan Report from XML

        Args:
            report: Report XML as string to import. This XML must contain
                a :code:`<report>` root element.
            task_id: UUID of task to import report to
            in_asset: Whether to create or update assets using the report
        """
        return self._send_and_transform_command(
            Reports.import_report(report, task_id, in_assets=in_assets)
        )

    def delete_audit_report(self, report_id: EntityID) -> T:
        """Deletes an existing audit report

        Args:
            report_id: UUID of the report to be deleted.
        """
        return self._send_and_transform_command(
            AuditReports.delete_report(report_id)
        )

    def get_audit_report(
        self,
        report_id: EntityID,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        delta_report_id: Optional[EntityID] = None,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        ignore_pagination: Optional[bool] = None,
        details: Optional[bool] = True,
    ) -> T:
        """Request a single audit report

        Args:
            report_id: UUID of an existing audit report
            filter_string: Filter term to use to filter results in the report
            filter_id: UUID of filter to use to filter results in the report
            delta_report_id: UUID of an existing report to compare report to.
            report_format_id: UUID of report format to use
                              or ReportFormatType (enum)
            ignore_pagination: Whether to ignore the filter terms "first" and
                "rows".
            details: Request additional report information details
                     defaults to True
        """
        return self._send_and_transform_command(
            AuditReports.get_report(
                report_id,
                filter_string=filter_string,
                filter_id=filter_id,
                delta_report_id=delta_report_id,
                report_format_id=report_format_id,
                ignore_pagination=ignore_pagination,
                details=details,
            )
        )

    def get_audit_reports(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        note_details: Optional[bool] = None,
        override_details: Optional[bool] = None,
        ignore_pagination: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> T:
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
        return self._send_and_transform_command(
            AuditReports.get_reports(
                filter_string=filter_string,
                filter_id=filter_id,
                note_details=note_details,
                override_details=override_details,
                ignore_pagination=ignore_pagination,
                details=details,
            )
        )
