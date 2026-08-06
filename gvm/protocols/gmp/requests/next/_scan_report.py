from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests import EntityID
from gvm.utils import to_bool
from gvm.xml import XmlCommand


class ScanReports:
    @classmethod
    def get_scan_report(
        cls,
        scan_report_id: EntityID,
        *,
        filter_string: str | None = None,
        filter_id: str | None = None,
    ) -> Request:
        """Request a structured summary of a single scan report.

        Args:
            scan_report_id: UUID of an existing scan report.
            filter_string: Filter term to apply to the report results.
            filter_id: UUID of a saved filter to apply to the report results.

        Returns:
            A request for the get_scan_report GMP command.

        Raises:
            RequiredArgument: If scan_report_id is not provided.
        """
        if not scan_report_id:
            raise RequiredArgument(
                function=cls.get_scan_report.__name__,
                argument="scan_report_id",
            )

        cmd = XmlCommand("get_scan_report")
        cmd.set_attribute("scan_report_id", str(scan_report_id))
        cmd.add_filter(filter_string, filter_id)

        return cmd

    @classmethod
    def export_scan_report(
        cls,
        report_id: EntityID,
        format_id: EntityID,
        *,
        config_id: EntityID | None = None,
        filter_string: str | None = None,
        ignore_pagination: bool = False,
        lean: bool = False,
        notes_details: bool = False,
        overrides_details: bool = False,
        result_tags: bool = False,
    ) -> Request:
        """Request an asynchronous export of a scan report.

        If an identical export is already pending or running, the existing
        report export is returned instead of creating a duplicate.

        Args:
            report_id: UUID of the scan report to export.
            format_id: UUID of the report format to apply.
            config_id: UUID of an optional report configuration.
            filter_string: Filter term to apply while generating the report.
            ignore_pagination: Whether pagination settings in the filter
                should be ignored.
            lean: Whether lean report data should be generated.
            notes_details: Whether note details should be included.
            overrides_details: Whether override details should be included.
            result_tags: Whether result tags should be included.

        Returns:
            A request for the export_scan_report GMP command.

        Raises:
            RequiredArgument: If report_id is not provided.
        """
        if not report_id:
            raise RequiredArgument(
                function=cls.export_scan_report.__name__,
                argument="report_id",
            )

        cmd = XmlCommand("export_scan_report")
        cmd.set_attribute("report_id", str(report_id))
        cmd.set_attribute("format_id", str(format_id))

        if config_id:
            cmd.set_attribute("config_id", str(config_id))

        if filter_string is not None:
            cmd.set_attribute("filter", filter_string)

        cmd.set_attribute(
            "ignore_pagination",
            to_bool(ignore_pagination),
        )
        cmd.set_attribute("lean", to_bool(lean))
        cmd.set_attribute(
            "notes_details",
            to_bool(notes_details),
        )
        cmd.set_attribute(
            "overrides_details",
            to_bool(overrides_details),
        )
        cmd.set_attribute(
            "result_tags",
            to_bool(result_tags),
        )

        return cmd
