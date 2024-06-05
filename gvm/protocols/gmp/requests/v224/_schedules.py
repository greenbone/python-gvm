# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID


class Schedules:

    @classmethod
    def clone_schedule(cls, schedule_id: EntityID) -> Request:
        """Clone an existing schedule

        Args:
            schedule_id: UUID of an existing schedule to clone from
        """
        if not schedule_id:
            raise RequiredArgument(
                function=cls.clone_schedule.__name__, argument="schedule_id"
            )

        cmd = XmlCommand("create_schedule")
        cmd.add_element("copy", str(schedule_id))
        return cmd

    @classmethod
    def create_schedule(
        cls,
        name: str,
        icalendar: str,
        timezone: str,
        *,
        comment: Optional[str] = None,
    ) -> Request:
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

                Schedules.create_schedule(
                    name="My Schedule",
                    icalendar=cal.to_ical(),
                    timezone='UTC'
                )

        Args:
            name: Name of the new schedule
            icalendar: `iCalendar`_ (RFC 5545) based data.
            timezone: Timezone to use for the icalendar events e.g
                Europe/Berlin. If the datetime values in the icalendar data are
                missing timezone information this timezone gets applied.
                Otherwise the datetime values from the icalendar data are
                displayed in this timezone
            comment: Comment on schedule.

        .. _iCalendar:
            https://tools.ietf.org/html/rfc5545
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_schedule.__name__, argument="name"
            )

        if not icalendar:
            raise RequiredArgument(
                function=cls.create_schedule.__name__, argument="icalendar"
            )

        if not timezone:
            raise RequiredArgument(
                function=cls.create_schedule.__name__, argument="timezone"
            )

        cmd = XmlCommand("create_schedule")

        cmd.add_element("name", name)
        cmd.add_element("icalendar", icalendar)
        cmd.add_element("timezone", timezone)

        if comment:
            cmd.add_element("comment", comment)

        return cmd

    @classmethod
    def delete_schedule(
        cls, schedule_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Deletes an existing schedule

        Args:
            schedule_id: UUID of the schedule to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not schedule_id:
            raise RequiredArgument(
                function=cls.delete_schedule.__name__, argument="schedule_id"
            )

        cmd = XmlCommand("delete_schedule")
        cmd.set_attribute("schedule_id", str(schedule_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @staticmethod
    def get_schedules(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> Request:
        """Request a list of schedules

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan schedules instead
            tasks: Whether to include tasks using the schedules
        """
        cmd = XmlCommand("get_schedules")

        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return cmd

    @classmethod
    def get_schedule(
        cls, schedule_id: EntityID, *, tasks: Optional[bool] = None
    ) -> Request:
        """Request a single schedule

        Args:
            schedule_id: UUID of an existing schedule
            tasks: Whether to include tasks using the schedules
        """
        cmd = XmlCommand("get_schedules")

        if not schedule_id:
            raise RequiredArgument(
                function=cls.get_schedule.__name__, argument="schedule_id"
            )

        cmd.set_attribute("schedule_id", str(schedule_id))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return cmd

    @classmethod
    def modify_schedule(
        cls,
        schedule_id: EntityID,
        *,
        name: Optional[str] = None,
        icalendar: Optional[str] = None,
        timezone: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> Request:
        """Modifies an existing schedule

        Args:
            schedule_id: UUID of the schedule to be modified
            name: Name of the schedule
            icalendar: `iCalendar`_ (RFC 5545) based data.
            timezone: Timezone to use for the icalendar events e.g
                Europe/Berlin. If the datetime values in the icalendar data are
                missing timezone information this timezone gets applied.
                Otherwise the datetime values from the icalendar data are
                displayed in this timezone
            comment: Comment on schedule.

        .. _iCalendar:
            https://tools.ietf.org/html/rfc5545
        """
        if not schedule_id:
            raise RequiredArgument(
                function=cls.modify_schedule.__name__, argument="schedule_id"
            )

        cmd = XmlCommand("modify_schedule")
        cmd.set_attribute("schedule_id", str(schedule_id))

        if name:
            cmd.add_element("name", name)

        if icalendar:
            cmd.add_element("icalendar", icalendar)

        if timezone:
            cmd.add_element("timezone", timezone)

        if comment:
            cmd.add_element("comment", comment)

        return cmd
