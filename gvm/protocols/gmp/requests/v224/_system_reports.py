# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from numbers import Integral
from typing import Optional

from gvm.errors import InvalidArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class SystemReports:
    @classmethod
    def get_system_reports(
        cls,
        *,
        name: Optional[str] = None,
        duration: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        brief: Optional[bool] = None,
        slave_id: Optional[EntityID] = None,
    ) -> Request:
        """Request a list of system reports

        Arguments:
            name: A string describing the required system report
            duration: The number of seconds into the past that the system report
                should include
            start_time: The start of the time interval the system report should
                include in ISO time format
            end_time: The end of the time interval the system report should
                include in ISO time format
            brief: Whether to include the actual system reports
            slave_id: UUID of GMP scanner from which to get the system reports
        """
        cmd = XmlCommand("get_system_reports")

        if name:
            cmd.set_attribute("name", name)

        if duration is not None:
            if not isinstance(duration, Integral):
                raise InvalidArgument(
                    "duration needs to be an integer number",
                    function=cls.get_system_reports.__name__,
                )

            cmd.set_attribute("duration", str(duration))

        if start_time:
            cmd.set_attribute("start_time", str(start_time))

        if end_time:
            cmd.set_attribute("end_time", str(end_time))

        if brief is not None:
            cmd.set_attribute("brief", to_bool(brief))

        if slave_id:
            cmd.set_attribute("slave_id", str(slave_id))

        return cmd
