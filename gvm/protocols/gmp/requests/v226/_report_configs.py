# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import Optional, Union

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand, XmlError

from .._entity_id import EntityID
from ..v224._report_formats import ReportFormatType


class ReportConfigs:

    @classmethod
    def clone_report_config(cls, report_config_id: EntityID) -> Request:
        """Clone a report config from an existing one

        Args:
            report_config_id: UUID of the existing report format
                              or ReportFormatType (enum)
        """
        if not report_config_id:
            raise RequiredArgument(
                function=cls.clone_report_config.__name__,
                argument="report_config_id",
            )

        cmd = XmlCommand("create_report_config")
        cmd.add_element("copy", str(report_config_id))
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
