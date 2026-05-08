from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests import EntityID
from gvm.utils import to_bool
from gvm.xml import XmlCommand


class ReportClosedCVEs:
    @classmethod
    def get_report_closed_cves(
        cls,
        report_id: EntityID,
        *,
        ignore_pagination: bool | None = None,
        details: bool | None = True,
    ) -> Request:
        """Request closed CVEs of a single report.

        Args:
            report_id: UUID of an existing report.
            ignore_pagination: Whether to ignore the filter terms "first" and
                "rows".
            details: Request additional report closed CVE information details.
                Defaults to True.
        """
        cmd = XmlCommand("get_report_closed_cves")

        if not report_id:
            raise RequiredArgument(
                function=cls.get_report_closed_cves.__name__,
                argument="report_id",
            )

        cmd.set_attribute("report_id", str(report_id))

        if ignore_pagination is not None:
            cmd.set_attribute("ignore_pagination", to_bool(ignore_pagination))

        cmd.set_attribute("details", to_bool(details))

        return cmd
