# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Greenbone Management Protocol (GMP) version 22.6
"""

from typing import Optional, Sequence, Union

from .._protocol import T
from ._gmp225 import GMPv225
from .requests.v226 import (
    AuditReports,
    EntityID,
    Filters,
    FilterType,
    ReportConfigParameter,
    ReportConfigs,
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
        return self._send_request_and_transform_response(
            ResourceNames.get_resource_names(
                resource_type, filter_string=filter_string
            )
        )

    def get_resource_name(
        self,
        resource_id: str,
        resource_type: ResourceType,  # type: ignore[override]
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
        return self._send_request_and_transform_response(
            ResourceNames.get_resource_name(resource_id, resource_type)
        )

    def delete_report(self, report_id: EntityID) -> T:
        """Deletes an existing scan report

        Args:
            report_id: UUID of the report to be deleted.
        """
        return self._send_request_and_transform_response(
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
        report_config_id: Optional[str] = None,
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
            report_config_id: UUID of report format config to use
            ignore_pagination: Whether to ignore the filter terms "first" and
                "rows".
            details: Request additional report information details
                     defaults to True
        """
        return self._send_request_and_transform_response(
            Reports.get_report(
                report_id,
                filter_string=filter_string,
                filter_id=filter_id,
                delta_report_id=delta_report_id,
                report_format_id=report_format_id,
                report_config_id=report_config_id,
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
        return self._send_request_and_transform_response(
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
        return self._send_request_and_transform_response(
            Reports.import_report(report, task_id, in_assets=in_assets)
        )

    def delete_audit_report(self, report_id: EntityID) -> T:
        """Deletes an existing audit report

        Args:
            report_id: UUID of the report to be deleted.
        """
        return self._send_request_and_transform_response(
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
        return self._send_request_and_transform_response(
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
        return self._send_request_and_transform_response(
            AuditReports.get_reports(
                filter_string=filter_string,
                filter_id=filter_id,
                note_details=note_details,
                override_details=override_details,
                ignore_pagination=ignore_pagination,
                details=details,
            )
        )

    def create_filter(
        self,
        name: str,
        *,
        filter_type: Optional[FilterType] = None,  # type: ignore[override]
        comment: Optional[str] = None,
        term: Optional[str] = None,
    ) -> T:
        """Create a new filter

        Args:
            name: Name of the new filter
            filter_type: Filter for entity type
            comment: Comment for the filter
            term: Filter term e.g. 'name=foo'
        """
        # override create_filter because of the different FilterType enum
        # this avoids warnings with type checkers
        return self._send_request_and_transform_response(
            Filters.create_filter(
                name, filter_type=filter_type, comment=comment, term=term
            )
        )

    def modify_filter(
        self,
        filter_id: EntityID,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        term: Optional[str] = None,
        filter_type: Optional[FilterType] = None,  # type: ignore[override]
    ) -> T:
        """Modifies an existing filter.

        Args:
            filter_id: UUID of the filter to be modified
            comment: Comment on filter.
            name: Name of filter.
            term: Filter term.
            filter_type: Resource type filter applies to.
        """
        # override create_filter because of the different FilterType enum
        # this avoids warnings with type checkers
        return self._send_request_and_transform_response(
            Filters.modify_filter(
                filter_id,
                comment=comment,
                name=name,
                term=term,
                filter_type=filter_type,
            )
        )

    def clone_report_config(self, report_config_id: EntityID) -> T:
        """Clone a report config from an existing one

        Args:
            report_config_id: UUID of the existing report config
        """
        return self._send_request_and_transform_response(
            ReportConfigs.clone_report_config(report_config_id)
        )

    def delete_report_config(
        self,
        report_config_id: EntityID,
        *,
        ultimate: Optional[bool] = False,
    ) -> T:
        """Deletes an existing report config

        Args:
            report_config_id: UUID of the report config to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        return self._send_request_and_transform_response(
            ReportConfigs.delete_report_config(
                report_config_id, ultimate=ultimate
            )
        )

    def get_report_configs(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> T:
        """Request a list of report configs

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan report configs instead
            details: Include report config details
        """
        return self._send_request_and_transform_response(
            ReportConfigs.get_report_configs(
                filter_string=filter_string,
                filter_id=filter_id,
                trash=trash,
                details=details,
            )
        )

    def get_report_config(
        self,
        report_config_id: EntityID,
    ) -> T:
        """Request a single report config

        Args:
            report_config_id: UUID of an existing report config
        """
        return self._send_request_and_transform_response(
            ReportConfigs.get_report_config(report_config_id)
        )

    def create_report_config(
        self,
        name: str,
        report_format_id: Union[EntityID, ReportFormatType],
        *,
        comment: Optional[str] = None,
        params: Optional[Sequence[ReportConfigParameter]] = None,
    ) -> T:
        """Create a report config

        Args:
            name: Name of the new report config
            report_format_id: UUID of the report format to be used or ReportFormatType.
            comment: An optional comment for the report config.
            params: A list of report config parameters.
        """
        return self._send_request_and_transform_response(
            ReportConfigs.create_report_config(
                name, report_format_id, comment=comment, params=params
            )
        )

    def modify_report_config(
        self,
        report_config_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        params: Optional[Sequence[ReportConfigParameter]] = None,
    ) -> T:
        """Create a report config

        Args:
            name: Name of the report config
            report_config_id: UUID of the report config to be modified.
            comment: An optional comment for the report config.
            params: A list of report config parameters.
        """
        return self._send_request_and_transform_response(
            ReportConfigs.modify_report_config(
                report_config_id, name=name, comment=comment, params=params
            )
        )
