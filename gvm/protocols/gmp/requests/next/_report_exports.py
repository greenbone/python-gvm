from gvm.protocols.core import Request
from gvm.protocols.gmp.requests import EntityID
from gvm.xml import XmlCommand


class ReportExports:
    @classmethod
    def get_report_exports(
        cls,
        *,
        report_export_id: EntityID | None = None,
    ) -> Request:
        """Request report exports.

        If report_export_id is provided, only the matching report export is
        requested. Otherwise, the command requests a list of report exports.

        Args:
            report_export_id: UUID of an optional report export.

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
