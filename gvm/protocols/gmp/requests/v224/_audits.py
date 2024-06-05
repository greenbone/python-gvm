# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from numbers import Integral
from typing import Optional, Union

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool, to_comma_list
from gvm.xml import XmlCommand

from .._entity_id import EntityID
from ._hosts import HostsOrdering


class Audits:
    @classmethod
    def create_audit(
        cls,
        name: str,
        policy_id: EntityID,
        target_id: EntityID,
        scanner_id: EntityID,
        *,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[Union[HostsOrdering, str]] = None,
        schedule_id: Optional[str] = None,
        alert_ids: Optional[list[EntityID]] = None,
        comment: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        observers: Optional[list[EntityID]] = None,
        preferences: Optional[dict[str, str]] = None,
    ) -> Request:
        """Create a new audit

        Args:
            name: Name of the new audit
            policy_id: UUID of policy to use by the audit
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: Comment for the audit
            alterable: Whether the task should be alterable
            alert_ids: List of UUIDs for alerts to be applied to the audit
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the audit should be run.
            schedule_periods: A limit to the number of times the audit will be
                scheduled, or 0 for no limit
            observers: List of names or ids of users which should be allowed to
                observe this audit
            preferences: Name/Value pairs of scanner preferences.
        """

        if not name:
            raise RequiredArgument(
                function=cls.create_audit.__name__, argument="name"
            )
        if not policy_id:
            raise RequiredArgument(
                function=cls.create_audit.__name__, argument="policy_id"
            )

        if not target_id:
            raise RequiredArgument(
                function=cls.create_audit.__name__, argument="target_id"
            )

        if not scanner_id:
            raise RequiredArgument(
                function=cls.create_audit.__name__, argument="scanner_id"
            )

        # don't allow to create a container task with create_task
        if target_id == "0":
            raise InvalidArgument(
                function=cls.create_audit.__name__, argument="target_id"
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("name", name)
        cmd.add_element("usage_type", "audit")
        cmd.add_element("config", attrs={"id": str(policy_id)})
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
    def modify_audit(
        cls,
        audit_id: EntityID,
        *,
        name: Optional[str] = None,
        policy_id: Optional[EntityID] = None,
        target_id: Optional[EntityID] = None,
        scanner_id: Optional[EntityID] = None,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[Union[str, HostsOrdering]] = None,
        schedule_id: Optional[EntityID] = None,
        schedule_periods: Optional[int] = None,
        comment: Optional[str] = None,
        alert_ids: Optional[list[EntityID]] = None,
        observers: Optional[list[EntityID]] = None,
        preferences: Optional[dict[str, str]] = None,
    ) -> Request:
        """Modifies an existing audit.

        Args:
            audit_id: UUID of audit to modify.
            name: The name of the audit.
            policy_id: UUID of policy to use by the audit
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: The comment on the audit.
            alert_ids: List of UUIDs for alerts to be applied to the audit
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the audit should be run.
            schedule_periods: A limit to the number of times the audit will be
                scheduled, or 0 for no limit.
            observers: List of names or ids of users which should be allowed to
                observe this audit
            preferences: Name/Value pairs of scanner preferences.
        """
        if not audit_id:
            raise RequiredArgument(
                function=cls.modify_audit.__name__, argument="task_id argument"
            )

        cmd = XmlCommand("modify_task")
        cmd.set_attribute("task_id", str(audit_id))

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if policy_id:
            cmd.add_element("config", attrs={"id": str(policy_id)})

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
    def clone_audit(cls, audit_id: EntityID) -> Request:
        """Clone an existing audit

        Args:
            audit_id: UUID of the audit to clone
        """
        if not audit_id:
            raise RequiredArgument(
                function=cls.clone_audit.__name__, argument="task_id"
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("copy", str(audit_id))
        return cmd

    @classmethod
    def delete_audit(
        cls, audit_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Delete an existing audit

        Args:
            audit_id: UUID of the audit to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not audit_id:
            raise RequiredArgument(
                function=cls.delete_audit.__name__, argument="task_id"
            )

        cmd = XmlCommand("delete_task")
        cmd.set_attribute("task_id", str(audit_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))
        return cmd

    @staticmethod
    def get_audits(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        schedules_only: Optional[bool] = None,
    ) -> Request:
        """Request a list of audits

        Args:
            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan audits instead
            details: Whether to include full audit details
            schedules_only: Whether to only include id, name and schedule
                details
        """
        cmd = XmlCommand("get_tasks")
        cmd.set_attribute("usage_type", "audit")
        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if schedules_only is not None:
            cmd.set_attribute("schedules_only", to_bool(schedules_only))

        return cmd

    @classmethod
    def get_audit(cls, audit_id: EntityID) -> Request:
        """Request a single audit

        Args:
            audit_id: UUID of an existing audit
        """
        if not audit_id:
            raise RequiredArgument(
                function=cls.get_audit.__name__, argument="audit_id"
            )

        cmd = XmlCommand("get_tasks")
        cmd.set_attribute("task_id", str(audit_id))
        cmd.set_attribute("usage_type", "audit")

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return cmd

    @classmethod
    def resume_audit(cls, audit_id: EntityID) -> Request:
        """Resume an existing stopped audit

        Args:
            audit_id: UUID of the audit to be resumed
        """
        if not audit_id:
            raise RequiredArgument(
                function=cls.resume_audit.__name__, argument="audit_id"
            )

        cmd = XmlCommand("resume_task")
        cmd.set_attribute("task_id", str(audit_id))
        return cmd

    @classmethod
    def start_audit(cls, audit_id: EntityID) -> Request:
        """Start an existing audit

        Args:
            audit_id: UUID of the audit to be started
        """
        if not audit_id:
            raise RequiredArgument(
                function=cls.start_audit.__name__, argument="audit_id"
            )

        cmd = XmlCommand("start_task")
        cmd.set_attribute("task_id", str(audit_id))
        return cmd

    @classmethod
    def stop_audit(cls, audit_id: EntityID) -> Request:
        """Stop an existing running audit

        Args:
            audit_id: UUID of the audit to be stopped
        """
        if not audit_id:
            raise RequiredArgument(
                function=cls.stop_audit.__name__, argument="audit_id"
            )

        cmd = XmlCommand("stop_task")
        cmd.set_attribute("task_id", str(audit_id))
        return cmd
