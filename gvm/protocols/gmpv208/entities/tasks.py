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


from collections.abc import Mapping
from numbers import Integral
from typing import Any, List, Optional

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv208.entities.hosts import HostsOrdering
from gvm.utils import add_filter, is_list_like, to_bool, to_comma_list
from gvm.xml import XmlCommand


class TasksMixin:
    def clone_task(self, task_id: str) -> Any:
        """Clone an existing task

        Arguments:
            task_id: UUID of existing task to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.clone_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("copy", task_id)
        return self._send_xml_command(cmd)

    def create_container_task(
        self, name: str, *, comment: Optional[str] = None
    ) -> Any:
        """Create a new container task

        A container task is a "meta" task to import and view reports from other
        systems.

        Arguments:
            name: Name of the task
            comment: Comment for the task

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_container_task.__name__, argument="name"
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("name", name)
        cmd.add_element("target", attrs={"id": "0"})

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def create_task(
        self,
        name: str,
        config_id: str,
        target_id: str,
        scanner_id: str,
        *,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[str] = None,
        alert_ids: Optional[List[str]] = None,
        comment: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        observers: Optional[List[str]] = None,
        preferences: Optional[dict] = None,
    ) -> Any:
        """Create a new scan task

        Arguments:
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

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_task.__name__, argument="name"
            )

        if not config_id:
            raise RequiredArgument(
                function=self.create_task.__name__, argument="config_id"
            )

        if not target_id:
            raise RequiredArgument(
                function=self.create_task.__name__, argument="target_id"
            )

        if not scanner_id:
            raise RequiredArgument(
                function=self.create_task.__name__, argument="scanner_id"
            )

        # don't allow to create a container task with create_task
        if target_id == "0":
            raise InvalidArgument(
                function=self.create_task.__name__, argument="target_id"
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("name", name)
        cmd.add_element("usage_type", "scan")
        cmd.add_element("config", attrs={"id": config_id})
        cmd.add_element("target", attrs={"id": target_id})
        cmd.add_element("scanner", attrs={"id": scanner_id})

        if comment:
            cmd.add_element("comment", comment)

        if alterable is not None:
            cmd.add_element("alterable", to_bool(alterable))

        if hosts_ordering:
            if not isinstance(hosts_ordering, HostsOrdering):
                raise InvalidArgumentType(
                    function=self.create_task.__name__,
                    argument="hosts_ordering",
                    arg_type=HostsOrdering.__name__,
                )
            cmd.add_element("hosts_ordering", hosts_ordering.value)

        if alert_ids is not None:
            if not is_list_like(alert_ids):
                raise InvalidArgumentType(
                    function=self.modify_task.__name__,
                    argument="alert_ids",
                    arg_type="list",
                )

            if not len(alert_ids) == 0:
                for alert in alert_ids:
                    cmd.add_element("alert", attrs={"id": str(alert)})

        if schedule_id:
            cmd.add_element("schedule", attrs={"id": schedule_id})

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

        if observers is not None:
            if not is_list_like(observers):
                raise InvalidArgumentType(
                    function=self.create_task.__name__,
                    argument="observers",
                    arg_type="list",
                )

            # gvmd splits by comma and space
            # gvmd tries to lookup each value as user name and afterwards as
            # user id. So both user name and user id are possible
            cmd.add_element("observers", to_comma_list(observers))

        if preferences is not None:
            if not isinstance(preferences, Mapping):
                raise InvalidArgumentType(
                    function=self.create_task.__name__,
                    argument="preferences",
                    arg_type=Mapping.__name__,
                )

            _xmlprefs = cmd.add_element("preferences")
            for pref_name, pref_value in preferences.items():
                _xmlpref = _xmlprefs.add_element("preference")
                _xmlpref.add_element("scanner_name", pref_name)
                _xmlpref.add_element("value", str(pref_value))

        return self._send_xml_command(cmd)

    def delete_task(
        self, task_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing task

        Arguments:
            task_id: UUID of the task to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.delete_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("delete_task")
        cmd.set_attribute("task_id", task_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_tasks(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        schedules_only: Optional[bool] = None,
    ) -> Any:
        """Request a list of tasks

        Arguments:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan tasks instead
            details: Whether to include full task details
            schedules_only: Whether to only include id, name and schedule
                details

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tasks")
        cmd.set_attribute("usage_type", "scan")

        add_filter(cmd, filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if schedules_only is not None:
            cmd.set_attribute("schedules_only", to_bool(schedules_only))

        return self._send_xml_command(cmd)

    def get_task(self, task_id: str) -> Any:
        """Request a single task

        Arguments:
            task_id: UUID of an existing task

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.get_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("get_tasks")
        cmd.set_attribute("task_id", task_id)
        cmd.set_attribute("usage_type", "scan")

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def modify_task(
        self,
        task_id: str,
        *,
        name: Optional[str] = None,
        config_id: Optional[str] = None,
        target_id: Optional[str] = None,
        scanner_id: Optional[str] = None,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        comment: Optional[str] = None,
        alert_ids: Optional[List[str]] = None,
        observers: Optional[List[str]] = None,
        preferences: Optional[dict] = None,
    ) -> Any:
        """Modifies an existing task.

        Arguments:
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

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.modify_task.__name__, argument="task_id argument"
            )

        cmd = XmlCommand("modify_task")
        cmd.set_attribute("task_id", task_id)

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if config_id:
            cmd.add_element("config", attrs={"id": config_id})

        if target_id:
            cmd.add_element("target", attrs={"id": target_id})

        if alterable is not None:
            cmd.add_element("alterable", to_bool(alterable))

        if hosts_ordering:
            if not isinstance(hosts_ordering, HostsOrdering):
                raise InvalidArgumentType(
                    function=self.modify_task.__name__,
                    argument="hosts_ordering",
                    arg_type=HostsOrdering.__name__,
                )
            cmd.add_element("hosts_ordering", hosts_ordering.value)

        if scanner_id:
            cmd.add_element("scanner", attrs={"id": scanner_id})

        if schedule_id:
            cmd.add_element("schedule", attrs={"id": schedule_id})

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
            if not is_list_like(alert_ids):
                raise InvalidArgumentType(
                    function=self.modify_task.__name__,
                    argument="alert_ids",
                    arg_type="list",
                )

            if len(alert_ids) == 0:
                cmd.add_element("alert", attrs={"id": "0"})
            else:
                for alert in alert_ids:
                    cmd.add_element("alert", attrs={"id": str(alert)})

        if observers is not None:
            if not is_list_like(observers):
                raise InvalidArgumentType(
                    function=self.modify_task.__name__,
                    argument="observers",
                    arg_type="list",
                )

            cmd.add_element("observers", to_comma_list(observers))

        if preferences is not None:
            if not isinstance(preferences, Mapping):
                raise InvalidArgumentType(
                    function=self.modify_task.__name__,
                    argument="preferences",
                    arg_type=Mapping.__name__,
                )

            _xmlprefs = cmd.add_element("preferences")
            for pref_name, pref_value in preferences.items():
                _xmlpref = _xmlprefs.add_element("preference")
                _xmlpref.add_element("scanner_name", pref_name)
                _xmlpref.add_element("value", str(pref_value))

        return self._send_xml_command(cmd)

    def move_task(self, task_id: str, *, slave_id: Optional[str] = None) -> Any:
        """Move an existing task to another GMP slave scanner or the master

        Arguments:
            task_id: UUID of the task to be moved
            slave_id: UUID of slave to reassign the task to, empty for master.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.move_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("move_task")
        cmd.set_attribute("task_id", task_id)

        if slave_id is not None:
            cmd.set_attribute("slave_id", slave_id)

        return self._send_xml_command(cmd)

    def start_task(self, task_id: str) -> Any:
        """Start an existing task

        Arguments:
            task_id: UUID of the task to be started

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.start_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("start_task")
        cmd.set_attribute("task_id", task_id)

        return self._send_xml_command(cmd)

    def resume_task(self, task_id: str) -> Any:
        """Resume an existing stopped task

        Arguments:
            task_id: UUID of the task to be resumed

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.resume_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("resume_task")
        cmd.set_attribute("task_id", task_id)

        return self._send_xml_command(cmd)

    def stop_task(self, task_id: str) -> Any:
        """Stop an existing running task

        Arguments:
            task_id: UUID of the task to be stopped

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not task_id:
            raise RequiredArgument(
                function=self.stop_task.__name__, argument="task_id"
            )

        cmd = XmlCommand("stop_task")
        cmd.set_attribute("task_id", task_id)

        return self._send_xml_command(cmd)
