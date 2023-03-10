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

from typing import Any, Optional

from gvm.errors import RequiredArgument
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class SchedulesMixin:
    def clone_schedule(self, schedule_id: str) -> Any:
        """Clone an existing schedule

        Arguments:
            schedule_id: UUID of an existing schedule to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not schedule_id:
            raise RequiredArgument(
                function=self.clone_schedule.__name__, argument="schedule_id"
            )

        cmd = XmlCommand("create_schedule")
        cmd.add_element("copy", schedule_id)
        return self._send_xml_command(cmd)

    def create_schedule(
        self,
        name: str,
        icalendar: str,
        timezone: str,
        *,
        comment: Optional[str] = None,
    ) -> Any:
        """Create a new schedule based in `iCalendar`_ data.

        Example:
            Requires https://pypi.org/project/icalendar/

            .. code-block:: python

                import pytz

                from datetime import datetime

                from icalendar import Calendar, Event

                cal = Calendar()

                cal.add('prodid', '-//Foo Bar//')
                cal.add('version', '2.0')

                event = Event()
                event.add('dtstamp', datetime.now(tz=pytz.UTC))
                event.add('dtstart', datetime(2020, 1, 1, tzinfo=pytz.utc))

                cal.add_component(event)

                gmp.create_schedule(
                    name="My Schedule",
                    icalendar=cal.to_ical(),
                    timezone='UTC'
                )
        Arguments:
            name: Name of the new schedule
            icalendar: `iCalendar`_ (RFC 5545) based data.
            timezone: Timezone to use for the icalender events e.g
                Europe/Berlin. If the datetime values in the icalendar data are
                missing timezone information this timezone gets applied.
                Otherwise the datetime values from the icalendar data are
                displayed in this timezone
            comment: Comment on schedule.

        Returns:
            The response. See :py:meth:`send_command` for details.

        .. _iCalendar:
            https://tools.ietf.org/html/rfc5545
        """
        if not name:
            raise RequiredArgument(
                function=self.create_schedule.__name__, argument="name"
            )
        if not icalendar:
            raise RequiredArgument(
                function=self.create_schedule.__name__, argument="icalendar"
            )
        if not timezone:
            raise RequiredArgument(
                function=self.create_schedule.__name__, argument="timezone"
            )

        cmd = XmlCommand("create_schedule")

        cmd.add_element("name", name)
        cmd.add_element("icalendar", icalendar)
        cmd.add_element("timezone", timezone)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def delete_schedule(
        self, schedule_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing schedule

        Arguments:
            schedule_id: UUID of the schedule to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not schedule_id:
            raise RequiredArgument(
                function=self.delete_schedule.__name__, argument="schedule_id"
            )

        cmd = XmlCommand("delete_schedule")
        cmd.set_attribute("schedule_id", schedule_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_schedules(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> Any:
        """Request a list of schedules

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan schedules instead
            tasks: Whether to include tasks using the schedules

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_schedules")

        add_filter(cmd, filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_schedule(
        self, schedule_id: str, *, tasks: Optional[bool] = None
    ) -> Any:
        """Request a single schedule

        Arguments:
            schedule_id: UUID of an existing schedule
            tasks: Whether to include tasks using the schedules

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_schedules")

        if not schedule_id:
            raise RequiredArgument(
                function=self.get_schedule.__name__, argument="schedule_id"
            )

        cmd.set_attribute("schedule_id", schedule_id)

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return self._send_xml_command(cmd)

    def modify_schedule(
        self,
        schedule_id: str,
        *,
        name: Optional[str] = None,
        icalendar: Optional[str] = None,
        timezone: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Modifies an existing schedule

        Arguments:
            schedule_id: UUID of the schedule to be modified
            name: Name of the schedule
            icalendar: `iCalendar`_ (RFC 5545) based data.
            timezone: Timezone to use for the icalender events e.g
                Europe/Berlin. If the datetime values in the icalendar data are
                missing timezone information this timezone gets applied.
                Otherwise the datetime values from the icalendar data are
                displayed in this timezone
            comment: Comment on schedule.

        Returns:
            The response. See :py:meth:`send_command` for details.

        .. _iCalendar:
            https://tools.ietf.org/html/rfc5545
        """
        if not schedule_id:
            raise RequiredArgument(
                function=self.modify_schedule.__name__, argument="schedule_id"
            )

        cmd = XmlCommand("modify_schedule")
        cmd.set_attribute("schedule_id", schedule_id)

        if name:
            cmd.add_element("name", name)

        if icalendar:
            cmd.add_element("icalendar", icalendar)

        if timezone:
            cmd.add_element("timezone", timezone)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)
