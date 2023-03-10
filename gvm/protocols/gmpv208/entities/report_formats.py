# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from enum import Enum
from typing import Any, Optional, Union

from lxml.etree import XMLSyntaxError

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


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

    @classmethod
    def from_string(
        cls,
        report_format: Optional[str],
    ) -> Optional["ReportFormatType"]:
        """Convert an report format name into a ReportFormatType instance"""
        if not report_format:
            return None

        try:
            return cls[report_format.replace(" ", "_").upper()]
        except KeyError:
            raise InvalidArgument(
                argument="report_format",
                function=cls.from_string.__name__,
            ) from KeyError


class ReportFormatsMixin:
    def clone_report_format(
        self, report_format_id: Union[str, ReportFormatType]
    ) -> Any:
        """Clone a report format from an existing one

        Arguments:
            report_format_id: UUID of the existing report format
                              or ReportFormatType (enum)

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.clone_report_format.__name__,
                argument="report_format_id",
            )

        cmd = XmlCommand("create_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.add_element("copy", report_format_id)
        return self._send_xml_command(cmd)

    def delete_report_format(
        self,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        *,
        ultimate: Optional[bool] = False,
    ) -> Any:
        """Deletes an existing report format

        Arguments:
            report_format_id: UUID of the report format to be deleted.
                              or ReportFormatType (enum)
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.delete_report_format.__name__,
                argument="report_format_id",
            )

        cmd = XmlCommand("delete_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_report_formats(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        alerts: Optional[bool] = None,
        params: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of report formats

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan report formats instead
            alerts: Whether to include alerts that use the report format
            params: Whether to include report format parameters
            details: Include report format file, signature and parameters

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_report_formats")

        add_filter(cmd, filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if alerts is not None:
            cmd.set_attribute("alerts", to_bool(alerts))

        if params is not None:
            cmd.set_attribute("params", to_bool(params))

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_report_format(
        self, report_format_id: Union[str, ReportFormatType]
    ) -> Any:
        """Request a single report format

        Arguments:
            report_format_id: UUID of an existing report format
                              or ReportFormatType (enum)
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_report_formats")
        if not report_format_id:
            raise RequiredArgument(
                function=self.get_report_format.__name__,
                argument="report_format_id",
            )

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def import_report_format(self, report_format: str) -> Any:
        """Import a report format from XML

        Arguments:
            report_format: Report format XML as string to import. This XML must
                contain a :code:`<get_report_formats_response>` root element.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format:
            raise RequiredArgument(
                function=self.import_report_format.__name__,
                argument="report_format",
            )

        cmd = XmlCommand("create_report_format")

        try:
            cmd.append_xml_str(report_format)
        except XMLSyntaxError as e:
            raise InvalidArgument(
                function=self.import_report_format.__name__,
                argument="report_format",
            ) from e

        return self._send_xml_command(cmd)

    def modify_report_format(
        self,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        *,
        active: Optional[bool] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        param_name: Optional[str] = None,
        param_value: Optional[str] = None,
    ) -> Any:
        """Modifies an existing report format.

        Arguments:
            report_format_id: UUID of report format to modify
                              or ReportFormatType (enum)
            active: Whether the report format is active.
            name: The name of the report format.
            summary: A summary of the report format.
            param_name: The name of the param.
            param_value: The value of the param.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.modify_report_format.__name__,
                argument="report_format_id ",
            )

        cmd = XmlCommand("modify_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        if active is not None:
            cmd.add_element("active", to_bool(active))

        if name:
            cmd.add_element("name", name)

        if summary:
            cmd.add_element("summary", summary)

        if param_name:
            _xmlparam = cmd.add_element("param")
            _xmlparam.add_element("name", param_name)

            if param_value is not None:
                _xmlparam.add_element("value", param_value)

        return self._send_xml_command(cmd)

    def verify_report_format(
        self, report_format_id: Union[str, ReportFormatType]
    ) -> Any:
        """Verify an existing report format

        Verifies the trust level of an existing report format. It will be
        checked whether the signature of the report format currently matches the
        report format. This includes the script and files used to generate
        reports of this format. It is *not* verified if the report format works
        as expected by the user.

        Arguments:
            report_format_id: UUID of the report format to be verified
                              or ReportFormatType (enum)

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.verify_report_format.__name__,
                argument="report_format_id",
            )

        cmd = XmlCommand("verify_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        return self._send_xml_command(cmd)
