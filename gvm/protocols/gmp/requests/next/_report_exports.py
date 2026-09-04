from gvm.protocols.core import Request
from gvm.protocols.gmp.requests import EntityID
from gvm.xml import XmlCommand


class ReportExports:
    @classmethod
    def get_report_exports(
        cls,
    ) -> Request:
        """Request report exports.

        The command requests a list of report exports.

        Returns:
            A request for the get_report_exports GMP command.
        """
        cmd = XmlCommand("get_report_exports")

        return cmd

    @classmethod
    def get_report_export(
        cls,
        report_export_id: EntityID,
    ) -> Request:
        """Request a single report export.

        Args:
            report_export_id: UUID of the report export.

        Returns:
            A request for the get_report_exports GMP command.
        """
        cmd = XmlCommand("get_report_exports")

        if report_export_id:
            cmd.set_attribute(
                "report_export_id",
                str(report_export_id),
            )

        return cmd
