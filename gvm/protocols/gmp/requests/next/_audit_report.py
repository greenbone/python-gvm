from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests import EntityID
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
