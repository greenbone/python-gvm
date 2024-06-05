# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Optional, Union

from gvm._enum import Enum
from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand, XmlError

from .._entity_id import EntityID


class ReportFormatType(Enum):
    """Enum for builtin report formats"""

    ANONYMOUS_XML = "5057e5cc-b825-11e4-9d0e-28d24461215b"
    ARF = "910200ca-dc05-11e1-954f-406186ea4fc5"
    CPE = "5ceff8ba-1f62-11e1-ab9f-406186ea4fc5"
    CSV_HOSTS = '9087b18c-626c-11e3-8892-406186ea4fc5"'
    CSV_RESULTS = "c1645568-627a-11e3-a660-406186ea4fc5"
    GCR_PDF = "dc51a40a-c022-11e9-b02d-3f7ca5bdcb11"
    GSR_HTML = "ffa123c9-a2d2-409e-bbbb-a6c1385dbeaa"
    GSR_PDF = "35ba7077-dc85-42ef-87c9-b0eda7e903b6"
    GXCR_PDF = "f0d348de-c022-11e9-bc4c-4bf1d5e1a8ca"
    GXR_PDF = "ebbc7f34-8ae5-11e1-b07b-001f29eadec8"
    ITG = "77bd6c4a-1f62-11e1-abf0-406186ea4fc5"
    LATEX = "a684c02c-b531-11e1-bdc2-406186ea4fc5"
    NBE = "9ca6fe72-1f62-11e1-9e7c-406186ea4fc5"
    PDF = "c402cc3e-b531-11e1-9163-406186ea4fc5"
    SVG = "9e5e5deb-879e-4ecc-8be6-a71cd0875cdd"
    TXT = "a3810a62-1f62-11e1-9219-406186ea4fc5"
    VERINICE_ISM = "c15ad349-bd8d-457a-880a-c7056532ee15"
    VERINICE_ITG = "50c9950a-f326-11e4-800c-28d24461215b"
    XML = "a994b278-1f62-11e1-96ac-406186ea4fc5"

    def __str__(self) -> str:
        return self.value


class ReportFormats:

    @classmethod
    def clone_report_format(
        cls, report_format_id: Union[EntityID, ReportFormatType]
    ) -> Request:
        """Clone a report format from an existing one

        Args:
            report_format_id: UUID of the existing report format
                              or ReportFormatType (enum)
        """
        if not report_format_id:
            raise RequiredArgument(
                function=cls.clone_report_format.__name__,
                argument="report_format_id",
            )

        cmd = XmlCommand("create_report_format")
        cmd.add_element("copy", str(report_format_id))
        return cmd

    @classmethod
    def delete_report_format(
        cls,
        report_format_id: Union[EntityID, ReportFormatType],
        *,
        ultimate: Optional[bool] = False,
    ) -> Request:
        """Deletes an existing report format

        Args:
            report_format_id: UUID of the report format to be deleted.
                              or ReportFormatType (enum)
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=cls.delete_report_format.__name__,
                argument="report_format_id",
            )

        cmd = XmlCommand("delete_report_format")

        cmd.set_attribute("report_format_id", str(report_format_id))

        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @staticmethod
    def get_report_formats(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        alerts: Optional[bool] = None,
        params: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of report formats

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan report formats instead
            alerts: Whether to include alerts that use the report format
            params: Whether to include report format parameters
            details: Include report format file, signature and parameters
        """
        cmd = XmlCommand("get_report_formats")

        cmd.add_filter(filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if alerts is not None:
            cmd.set_attribute("alerts", to_bool(alerts))

        if params is not None:
            cmd.set_attribute("params", to_bool(params))

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return cmd

    @classmethod
    def get_report_format(
        cls, report_format_id: Union[EntityID, ReportFormatType]
    ) -> Request:
        """Request a single report format

        Args:
            report_format_id: UUID of an existing report format
                              or ReportFormatType (enum)
        """
        if not report_format_id:
            raise RequiredArgument(
                function=cls.get_report_format.__name__,
                argument="report_format_id",
            )

        cmd = XmlCommand("get_report_formats")

        cmd.set_attribute("report_format_id", str(report_format_id))

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return cmd

    @classmethod
    def import_report_format(cls, report_format: str) -> Request:
        """Import a report format from XML

        Args:
            report_format: Report format XML as string to import. This XML must
                contain a :code:`<get_report_formats_response>` root element.
        """
        if not report_format:
            raise RequiredArgument(
                function=cls.import_report_format.__name__,
                argument="report_format",
            )

        cmd = XmlCommand("create_report_format")

        try:
            cmd.append_xml_str(report_format)
        except XmlError as e:
            raise InvalidArgument(
                function=cls.import_report_format.__name__,
                argument="report_format",
            ) from e

        return cmd

    @classmethod
    def modify_report_format(
        cls,
        report_format_id: Union[EntityID, ReportFormatType],
        *,
        active: Optional[bool] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        param_name: Optional[str] = None,
        param_value: Optional[str] = None,
    ) -> Request:
        """Modifies an existing report format.

        Args:
            report_format_id: UUID of report format to modify
                              or ReportFormatType (enum)
            active: Whether the report format is active.
            name: The name of the report format.
            summary: A summary of the report format.
            param_name: The name of the param.
            param_value: The value of the param.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=cls.modify_report_format.__name__,
                argument="report_format_id ",
            )

        cmd = XmlCommand("modify_report_format")

        cmd.set_attribute("report_format_id", str(report_format_id))

        if active is not None:
            cmd.add_element("active", to_bool(active))

        if name:
            cmd.add_element("name", name)

        if summary:
            cmd.add_element("summary", summary)

        if param_name:
            xml_param = cmd.add_element("param")
            xml_param.add_element("name", param_name)

            if param_value is not None:
                xml_param.add_element("value", param_value)

        return cmd

    @classmethod
    def verify_report_format(
        cls, report_format_id: Union[EntityID, ReportFormatType]
    ) -> Request:
        """Verify an existing report format

        Verifies the trust level of an existing report format. It will be
        checked whether the signature of the report format currently matches the
        report format. This includes the script and files used to generate
        reports of this format. It is *not* verified if the report format works
        as expected by the user.

        Args:
            report_format_id: UUID of the report format to be verified
                              or ReportFormatType (enum)
        """
        if not report_format_id:
            raise RequiredArgument(
                function=cls.verify_report_format.__name__,
                argument="report_format_id",
            )

        cmd = XmlCommand("verify_report_format")
        cmd.set_attribute("report_format_id", str(report_format_id))
        return cmd
