# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from dataclasses import dataclass
from typing import Optional, Sequence, Union

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID
from ..v224._report_formats import ReportFormatType


@dataclass
class ReportConfigParameter:
    """
    A class to represent a parameter for a report configuration.

    Args:
        name: The name of the parameter.
        value: The value of the parameter.
        use_default (optional): A flag indicating whether to use the default value (default is False).
    """

    name: str
    value: Optional[str] = None
    use_default: bool = False


class ReportConfigs:
    @classmethod
    def clone_report_config(cls, report_config_id: EntityID) -> Request:
        """Clone a report config from an existing one

        Args:
            report_config_id: UUID of the existing report config

        Example:

            .. code-block:: python

                from gvm.protocols.gmp.requests.v226 import ReportConfigs

                request = ReportConfigs.clone_report_config("report_config_id")
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
    def delete_report_config(
        cls,
        report_config_id: EntityID,
        *,
        ultimate: Optional[bool] = False,
    ) -> Request:
        """Deletes an existing report config

        Args:
            report_config_id: UUID of the report config to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.

        Example:

            .. code-block:: python

                from gvm.protocols.gmp.requests.v226 import ReportConfigs

                request = ReportConfigs.delete_report_config("report_config_id", ultimate=True)
        """
        if not report_config_id:
            raise RequiredArgument(
                function=cls.delete_report_config.__name__,
                argument="report_config_id",
            )

        cmd = XmlCommand("delete_report_config")

        cmd.set_attribute("report_config_id", str(report_config_id))

        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @staticmethod
    def get_report_configs(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Request:
        """Request a list of report configs

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan report configs instead
            details: Include report config details

        Examples:

            .. code-block:: python

                from gvm.protocols.gmp.requests.v226 import ReportConfigs

                request = ReportConfigs.get_report_configs()

            .. code-block:: python

                from gvm.protocols.gmp.requests.v226 import ReportConfigs

                request = ReportConfigs.get_report_configs(filter_string="name=foo", details=True)
        """
        cmd = XmlCommand("get_report_configs")

        cmd.add_filter(filter_string, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return cmd

    @classmethod
    def get_report_config(
        cls,
        report_config_id: EntityID,
    ) -> Request:
        """Request a single report config

        Args:
            report_config_id: UUID of an existing report config

        Example:

            .. code-block:: python

                from gvm.protocols.gmp.requests.v226 import ReportConfigs

                request = ReportConfigs.get_report_config("report_config_id")
        """
        if not report_config_id:
            raise RequiredArgument(
                function=cls.get_report_config.__name__,
                argument="report_config_id",
            )

        cmd = XmlCommand("get_report_configs")

        cmd.set_attribute("report_config_id", str(report_config_id))

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return cmd

    @classmethod
    def create_report_config(
        cls,
        name: str,
        report_format_id: Union[EntityID, ReportFormatType],
        *,
        comment: Optional[str] = None,
        params: Optional[Sequence[ReportConfigParameter]] = None,
    ) -> Request:
        """Create a report config

        Args:
            name: The name of the report config.
            report_format_id: UUID of the report format to be used or ReportFormatType.
            comment: An optional comment for the report config.
            params: A list of report config parameters.

        Example:

            .. code-block:: python

                from gvm.protocols.gmp.requests.v226 import ReportConfigs, ReportFormatType

                request = ReportConfigs.create_report_config(
                    "Adjusted Node Distance",
                    ReportFormatType.SVG,
                    params=[
                        ReportConfigParameter("Graph Type", use_default=True),
                        ReportConfigParameter("Node Distance", "5"),
                    ],
                )
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_report_config.__name__,
                argument="name",
            )
        if not report_format_id:
            raise RequiredArgument(
                function=cls.create_report_config.__name__,
                argument="report_format_id",
            )

        cmd = XmlCommand("create_report_config")
        cmd.add_element("name", name)
        cmd.add_element("report_format", attrs={"id": str(report_format_id)})
        if comment:
            cmd.add_element("comment", comment)

        if params:
            for param in params:
                xml_param = cmd.add_element("param")
                xml_param.add_element("name", param.name)
                value = xml_param.add_element("value")
                value.set_attribute("use_default", to_bool(param.use_default))
                if param.value is not None and not param.use_default:
                    value.set_text(param.value)

        return cmd

    @classmethod
    def modify_report_config(
        cls,
        report_config_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        params: Optional[Sequence[ReportConfigParameter]] = None,
    ) -> Request:
        """Create a report config

        Args:
            name: The name of the report config.
            report_config_id: UUID of the report config to be modified.
            comment: An optional comment for the report config.
            params: A list of report config parameters.

        Examples:

            .. code-block:: python

                from gvm.protocols.gmp.requests.v226 import ReportConfigs

                request = ReportConfigs.create_report_config(
                    report_config_id,
                    params=[
                        ReportConfigParameter("Graph Type", use_default=True),
                        ReportConfigParameter("Node Distance", "5"),
                    ],
                )

            .. code-block:: python

                from gvm.protocols.gmp.requests.v226 import ReportConfigs

                request = ReportConfigs.create_report_config(
                    report_config_id,
                    name="Modified Report Config",
                )
        """
        if not report_config_id:
            raise RequiredArgument(
                function=cls.modify_report_config.__name__,
                argument="report_config_id",
            )

        cmd = XmlCommand("modify_report_config")
        cmd.set_attribute("report_config_id", str(report_config_id))

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if params:
            for param in params:
                xml_param = cmd.add_element("param")
                xml_param.add_element("name", param.name)
                value = xml_param.add_element("value")
                value.set_attribute("use_default", to_bool(param.use_default))
                if param.value is not None and not param.use_default:
                    value.set_text(param.value)

        return cmd
