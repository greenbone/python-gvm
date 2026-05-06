from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests import EntityID
from gvm.utils import to_bool
from gvm.xml import XmlCommand


class ReportOperatingSystems:
    @classmethod
    def get_report_operating_systems(
        cls,
        report_id: EntityID,
        *,
        filter_string: str | None = None,
        filter_id: str | None = None,
        ignore_pagination: bool | None = None,
        details: bool | None = True,
    ) -> Request:
        """Request operating systems of a single report.

        Args:
            report_id: UUID of an existing report.
            filter_string: Filter term to use to filter results in the report
            filter_id: UUID of filter to use to filter results in the report
            ignore_pagination: Whether to ignore the filter terms "first" and
                "rows".
            details: Request additional report operating systems information details.
                Defaults to True.
        """
        cmd = XmlCommand("get_report_operating_systems")

        if not report_id:
            raise RequiredArgument(
                function=cls.get_report_operating_systems.__name__,
                argument="report_id",
            )

        cmd.set_attribute("report_id", str(report_id))

        cmd.add_filter(filter_string, filter_id)

        if ignore_pagination is not None:
            cmd.set_attribute("ignore_pagination", to_bool(ignore_pagination))

        cmd.set_attribute("details", to_bool(details))

        return cmd
