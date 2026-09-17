from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests import EntityID
from gvm.utils import to_bool
from gvm.xml import XmlCommand


class AuditReport:
    @classmethod
    def get_audit_report(
        cls,
        audit_report_id: EntityID,
        *,
        filter_string: str | None = None,
        filter_id: str | None = None,
    ) -> Request:
        """Request a structured summary of a single audit report.

        Args:
            audit_report_id: UUID of an existing audit report.
            filter_string: Filter term to apply to the report results.
            filter_id: UUID of a saved filter to apply to the report results.

        Returns:
            A request for the get_audit_report GMP command.

        Raises:
            RequiredArgument: If audit_report_id is not provided.
        """
        if not audit_report_id:
            raise RequiredArgument(
                function=cls.get_audit_report.__name__,
                argument="audit_report_id",
            )

        cmd = XmlCommand("get_audit_report")
        cmd.set_attribute("audit_report_id", str(audit_report_id))
        cmd.add_filter(filter_string, filter_id)

        return cmd

    @classmethod
    def export_audit_report(
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
        """Request an asynchronous export of an audit report.

        If an identical export is already pending or running, the existing
        report export is returned instead of creating a duplicate.

        Args:
            report_id: UUID of the audit report to export.
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
            A request for the export_audit_report GMP command.

        Raises:
            RequiredArgument: If report_id is not provided.
        """
        if not report_id:
            raise RequiredArgument(
                function=cls.export_audit_report.__name__,
                argument="report_id",
            )

        cmd = XmlCommand("export_audit_report")
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

    @classmethod
    def export_delta_audit_report(
        cls,
        report_id: EntityID,
        delta_report_id: EntityID,
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
        """Request an asynchronous export of a delta audit report.

        If an identical export is already pending or running, the existing
        report export is returned instead of creating a duplicate.

        Args:
            report_id: UUID of the audit report to export.
            delta_report_id: UUID of the report used for delta comparison.
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
            A request for the export_delta_audit_report GMP command.

        Raises:
            RequiredArgument: If report_id or delta_report_id is not provided.
        """
        if not report_id:
            raise RequiredArgument(
                function=cls.export_delta_audit_report.__name__,
                argument="report_id",
            )

        if not delta_report_id:
            raise RequiredArgument(
                function=cls.export_delta_audit_report.__name__,
                argument="delta_report_id",
            )

        cmd = XmlCommand("export_delta_audit_report")
        cmd.set_attribute("report_id", str(report_id))
        cmd.set_attribute("delta_report_id", str(delta_report_id))
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
