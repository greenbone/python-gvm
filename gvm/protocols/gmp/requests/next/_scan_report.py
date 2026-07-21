from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests import EntityID
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
