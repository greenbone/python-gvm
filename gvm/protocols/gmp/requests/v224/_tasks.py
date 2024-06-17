# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from numbers import Integral
from typing import Mapping, Optional, Sequence

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import SupportsStr, to_bool, to_comma_list
from gvm.xml import XmlCommand

from .._entity_id import EntityID
from ._hosts import HostsOrdering


class Tasks:

    @classmethod
    def clone_task(cls, task_id: EntityID) -> Request:
        """Clone an existing task

        Args:
            task_id: UUID of existing task to clone from
        """
        if not task_id:
            raise RequiredArgument(
                function=cls.clone_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("copy", str(task_id))
        return cmd

    @classmethod
    def create_container_task(
        cls, name: str, *, comment: Optional[str] = None
    ) -> Request:
        """Create a new container task

        A container task is a "meta" task to import and view reports from other
        systems.

        Args:
            name: Name of the task
            comment: Comment for the task
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_container_task.__name__, argument="name"
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("name", name)
        cmd.add_element("target", attrs={"id": "0"})

        if comment:
            cmd.add_element("comment", comment)

        return cmd

    @classmethod
    def create_task(
        cls,
        name: str,
        config_id: EntityID,
        target_id: EntityID,
        scanner_id: EntityID,
        *,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[EntityID] = None,
        alert_ids: Optional[Sequence[EntityID]] = None,
        comment: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        observers: Optional[Sequence[str]] = None,
        preferences: Optional[Mapping[str, SupportsStr]] = None,
    ) -> Request:
        """Create a new scan task

        Args:
            name: Name of the new task
            config_id: UUID of config to use by the task
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: Comment for the task
            alterable: Whether the task should be alterable
            alert_ids: List of UUIDs for alerts to be applied to the task
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the task should be run.
            schedule_periods: A limit to the number of times the task will be
                scheduled, or 0 for no limit
            observers: List of names or ids of users which should be allowed to
                observe this task
            preferences: Name/Value pairs of scanner preferences.
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_task.__name__, argument="name"
            )

        if not config_id:
            raise RequiredArgument(
                function=cls.create_task.__name__, argument="config_id"
            )

        if not target_id:
            raise RequiredArgument(
                function=cls.create_task.__name__, argument="target_id"
            )

        if not scanner_id:
            raise RequiredArgument(
                function=cls.create_task.__name__, argument="scanner_id"
            )

        # don't allow to create a container task with create_task
        if target_id == "0":
            raise InvalidArgument(
                function=cls.create_task.__name__, argument="target_id"
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("name", name)
        cmd.add_element("usage_type", "scan")
        cmd.add_element("config", attrs={"id": str(config_id)})
        cmd.add_element("target", attrs={"id": str(target_id)})
        cmd.add_element("scanner", attrs={"id": str(scanner_id)})

        if comment:
            cmd.add_element("comment", comment)

        if alterable is not None:
            cmd.add_element("alterable", to_bool(alterable))

        if hosts_ordering:
            if not isinstance(hosts_ordering, HostsOrdering):
                hosts_ordering = HostsOrdering(hosts_ordering)
            cmd.add_element("hosts_ordering", hosts_ordering.value)

        if alert_ids:
            for alert in alert_ids:
                cmd.add_element("alert", attrs={"id": str(alert)})

        if schedule_id:
            cmd.add_element("schedule", attrs={"id": str(schedule_id)})

            if schedule_periods is not None:
                if (
                    not isinstance(schedule_periods, Integral)
                    or schedule_periods < 0
                ):
                    raise InvalidArgument(
                        "schedule_periods must be an integer greater or equal "
                        "than 0"
                    )
                cmd.add_element("schedule_periods", str(schedule_periods))

        if observers:
            # gvmd splits by comma and space
            # gvmd tries to lookup each value as user name and afterwards as
            # user id. So both user name and user id are possible
            cmd.add_element("observers", to_comma_list(observers))

        if preferences is not None:
            xml_prefs = cmd.add_element("preferences")
            for pref_name, pref_value in preferences.items():
                xml_pref = xml_prefs.add_element("preference")
                xml_pref.add_element("scanner_name", pref_name)
                xml_pref.add_element("value", str(pref_value))

        return cmd

    @classmethod
    def delete_task(
        cls, task_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Deletes an existing task

        Args:
            task_id: UUID of the task to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not task_id:
            raise RequiredArgument(
                function=cls.delete_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("delete_task")
        cmd.set_attribute("task_id", str(task_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return cmd

    @staticmethod
    def get_tasks(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        schedules_only: Optional[bool] = None,
        ignore_pagination: Optional[bool] = None,
    ) -> Request:
        """Request a list of tasks

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan tasks instead
            details: Whether to include full task details
            schedules_only: Whether to only include id, name and schedule
                details
            ignore_pagination: Whether to ignore pagination settings (filter
                terms "first" and "rows"). Default is False.
        """
        cmd = XmlCommand("get_tasks")
        cmd.set_attribute("usage_type", "scan")

        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if schedules_only is not None:
            cmd.set_attribute("schedules_only", to_bool(schedules_only))

        if ignore_pagination is not None:
            cmd.set_attribute("ignore_pagination", to_bool(ignore_pagination))

        return cmd

    @classmethod
    def get_task(cls, task_id: EntityID) -> Request:
        """Request a single task

        Args:
            task_id: UUID of an existing task
        """
        if not task_id:
            raise RequiredArgument(
                function=cls.get_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("get_tasks")
        cmd.set_attribute("task_id", str(task_id))
        cmd.set_attribute("usage_type", "scan")

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return cmd

    @classmethod
    def modify_task(
        cls,
        task_id: EntityID,
        *,
        name: Optional[str] = None,
        config_id: Optional[EntityID] = None,
        target_id: Optional[EntityID] = None,
        scanner_id: Optional[EntityID] = None,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[EntityID] = None,
        schedule_periods: Optional[int] = None,
        comment: Optional[str] = None,
        alert_ids: Optional[Sequence[EntityID]] = None,
        observers: Optional[Sequence[str]] = None,
        preferences: Optional[Mapping[str, SupportsStr]] = None,
    ) -> Request:
        """Modifies an existing task.

        Args:
            task_id: UUID of task to modify.
            name: The name of the task.
            config_id: UUID of scan config to use by the task
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: The comment on the task.
            alert_ids: List of UUIDs for alerts to be applied to the task
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the task should be run.
            schedule_periods: A limit to the number of times the task will be
                scheduled, or 0 for no limit.
            observers: List of names or ids of users which should be allowed to
                observe this task
            preferences: Name/Value pairs of scanner preferences.
        """
        if not task_id:
            raise RequiredArgument(
                function=cls.modify_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("modify_task")
        cmd.set_attribute("task_id", str(task_id))

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if config_id:
            cmd.add_element("config", attrs={"id": str(config_id)})

        if target_id:
            cmd.add_element("target", attrs={"id": str(target_id)})

        if alterable is not None:
            cmd.add_element("alterable", to_bool(alterable))

        if hosts_ordering:
            if not isinstance(hosts_ordering, HostsOrdering):
                hosts_ordering = HostsOrdering(hosts_ordering)
            cmd.add_element("hosts_ordering", hosts_ordering.value)

        if scanner_id:
            cmd.add_element("scanner", attrs={"id": str(scanner_id)})

        if schedule_id:
            cmd.add_element("schedule", attrs={"id": str(schedule_id)})

        if schedule_periods is not None:
            if (
                not isinstance(schedule_periods, Integral)
                or schedule_periods < 0
            ):
                raise InvalidArgument(
                    "schedule_periods must be an integer greater or equal "
                    "than 0"
                )
            cmd.add_element("schedule_periods", str(schedule_periods))

        if alert_ids is not None:
            if len(alert_ids) == 0:
                cmd.add_element("alert", attrs={"id": "0"})
            else:
                for alert in alert_ids:
                    cmd.add_element("alert", attrs={"id": str(alert)})

        if observers is not None:
            cmd.add_element("observers", to_comma_list(observers))

        if preferences is not None:
            xml_prefs = cmd.add_element("preferences")
            for pref_name, pref_value in preferences.items():
                xml_pref = xml_prefs.add_element("preference")
                xml_pref.add_element("scanner_name", pref_name)
                xml_pref.add_element("value", str(pref_value))

        return cmd

    @classmethod
    def move_task(
        cls, task_id: EntityID, *, slave_id: Optional[EntityID] = None
    ) -> Request:
        """Move an existing task to another GMP slave scanner or the master

        Args:
            task_id: UUID of the task to be moved
            slave_id: UUID of the sensor to reassign the task to, empty for master.
        """
        if not task_id:
            raise RequiredArgument(
                function=cls.move_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("move_task")
        cmd.set_attribute("task_id", str(task_id))

        if slave_id is not None:
            cmd.set_attribute("slave_id", str(slave_id))

        return cmd

    @classmethod
    def start_task(cls, task_id: EntityID) -> Request:
        """Start an existing task

        Args:
            task_id: UUID of the task to be started
        """
        if not task_id:
            raise RequiredArgument(
                function=cls.start_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("start_task")
        cmd.set_attribute("task_id", str(task_id))
        return cmd

    @classmethod
    def resume_task(cls, task_id: EntityID) -> Request:
        """Resume an existing stopped task

        Args:
            task_id: UUID of the task to be resumed
        """
        if not task_id:
            raise RequiredArgument(
                function=cls.resume_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("resume_task")
        cmd.set_attribute("task_id", str(task_id))
        return cmd

    @classmethod
    def stop_task(cls, task_id: EntityID) -> Request:
        """Stop an existing running task

        Args:
            task_id: UUID of the task to be stopped
        """
        if not task_id:
            raise RequiredArgument(
                function=cls.stop_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("stop_task")
        cmd.set_attribute("task_id", str(task_id))
        return cmd
