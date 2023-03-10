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

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument

# if I use latest, I get circular import :/
from gvm.protocols.gmpv208.entities.report_formats import ReportFormatType
from gvm.utils import add_filter, to_bool
from gvm.xml import XmlCommand


class AlertEvent(Enum):
    """Enum for alert event types"""

    TASK_RUN_STATUS_CHANGED = "Task run status changed"
    UPDATED_SECINFO_ARRIVED = "Updated SecInfo arrived"
    NEW_SECINFO_ARRIVED = "New SecInfo arrived"
    TICKET_RECEIVED = "Ticket received"
    ASSIGNED_TICKET_CHANGED = "Assigned ticket changed"
    OWNED_TICKET_CHANGED = "Owned ticket changed"

    @classmethod
    def from_string(
        cls,
        alert_event: Optional[str],
    ) -> Optional["AlertEvent"]:
        """Convert an alert event string into a AlertEvent instance"""
        if not alert_event:
            return None

        try:
            return cls[alert_event.replace(" ", "_").upper()]
        except KeyError:
            raise InvalidArgument(
                argument="alert_event",
                function=cls.from_string.__name__,
            ) from None


class AlertCondition(Enum):
    """Enum for alert condition types"""

    ALWAYS = "Always"
    ERROR = "Error"
    SEVERITY_AT_LEAST = "Severity at least"
    SEVERITY_CHANGED = "Severity changed"
    FILTER_COUNT_CHANGED = "Filter count changed"
    FILTER_COUNT_AT_LEAST = "Filter count at least"

    @classmethod
    def from_string(
        cls, alert_condition: Optional[str]
    ) -> Optional["AlertCondition"]:
        """Convert an alert condition string into a AlertCondition instance"""
        if not alert_condition:
            return None

        try:
            return cls[alert_condition.replace(" ", "_").upper()]
        except KeyError:
            raise InvalidArgument(
                argument="alert_condition",
                function=cls.from_string.__name__,
            ) from None


class AlertMethod(Enum):
    """Enum for alert method type"""

    SCP = "SCP"
    SEND = "Send"
    SMB = "SMB"
    SNMP = "SNMP"
    SYSLOG = "Syslog"
    EMAIL = "Email"
    START_TASK = "Start Task"
    HTTP_GET = "HTTP Get"
    SOURCEFIRE_CONNECTOR = "Sourcefire Connector"
    VERINICE_CONNECTOR = "verinice Connector"
    TIPPINGPOINT_SMS = "TippingPoint SMS"
    ALEMBA_VFIRE = "Alemba vFire"

    @classmethod
    def from_string(
        cls,
        alert_method: Optional[str],
    ) -> Optional["AlertMethod"]:
        """Convert an alert method string into a AlertCondition instance"""
        if not alert_method:
            return None

        try:
            return cls[alert_method.replace(" ", "_").upper()]
        except KeyError:
            raise InvalidArgument(
                argument="alert_method",
                function=cls.from_string.__name__,
            ) from None


def _check_event(
    event: AlertEvent, condition: AlertCondition, method: AlertMethod
):
    if event == AlertEvent.TASK_RUN_STATUS_CHANGED:
        if not condition:
            raise RequiredArgument(
                f"condition is required for event {event.name}"
            )

        if not method:
            raise RequiredArgument(f"method is required for event {event.name}")

        if condition not in (
            AlertCondition.ALWAYS,
            AlertCondition.FILTER_COUNT_CHANGED,
            AlertCondition.FILTER_COUNT_AT_LEAST,
            AlertCondition.SEVERITY_AT_LEAST,
            AlertCondition.SEVERITY_CHANGED,
        ):
            raise InvalidArgument(
                f"Invalid condition {condition.name} for event {event.name}"
            )
    elif event in (
        AlertEvent.NEW_SECINFO_ARRIVED,
        AlertEvent.UPDATED_SECINFO_ARRIVED,
    ):
        if not condition:
            raise RequiredArgument(
                f"condition is required for event {event.name}"
            )

        if not method:
            raise RequiredArgument(f"method is required for event {event.name}")

        if condition != AlertCondition.ALWAYS:
            raise InvalidArgument(
                f"Invalid condition {condition.name} for event {event.name}"
            )
        if method not in (
            AlertMethod.SCP,
            AlertMethod.SEND,
            AlertMethod.SMB,
            AlertMethod.SNMP,
            AlertMethod.SYSLOG,
            AlertMethod.EMAIL,
        ):
            raise InvalidArgument(
                f"Invalid method {method.name} for event {event.name}"
            )
    elif event in (
        AlertEvent.TICKET_RECEIVED,
        AlertEvent.OWNED_TICKET_CHANGED,
        AlertEvent.ASSIGNED_TICKET_CHANGED,
    ):
        if not condition:
            raise RequiredArgument(
                f"condition is required for event {event.name}"
            )

        if not method:
            raise RequiredArgument(f"method is required for event {event.name}")
        if condition != AlertCondition.ALWAYS:
            raise InvalidArgument(
                f"Invalid condition {condition.name} for event {event.name}"
            )
        if method not in (
            AlertMethod.EMAIL,
            AlertMethod.START_TASK,
            AlertMethod.SYSLOG,
        ):
            raise InvalidArgument(
                f"Invalid method {method.name} for event {event.name}"
            )


class AlertsMixin:
    def clone_alert(self, alert_id: str) -> Any:
        """Clone an existing alert

        Arguments:
            alert_id: UUID of an existing alert to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not alert_id:
            raise RequiredArgument(
                function=self.clone_alert.__name__, argument="alert_id"
            )

        cmd = XmlCommand("create_alert")
        cmd.add_element("copy", alert_id)
        return self._send_xml_command(cmd)

    def create_alert(
        self,
        name: str,
        condition: AlertCondition,
        event: AlertEvent,
        method: AlertMethod,
        *,
        method_data: Optional[dict] = None,
        event_data: Optional[dict] = None,
        condition_data: Optional[dict] = None,
        filter_id: Optional[int] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Create a new alert

        Arguments:
            name: Name of the new Alert
            condition: The condition that must be satisfied for the alert
                to occur; if the event is either 'Updated SecInfo arrived' or
                'New SecInfo arrived', condition must be 'Always'. Otherwise,
                condition can also be on of 'Severity at least', 'Filter count
                changed' or 'Filter count at least'.
            event: The event that must happen for the alert to occur, one
                of 'Task run status changed', 'Updated SecInfo arrived' or 'New
                SecInfo arrived'
            method: The method by which the user is alerted, one of 'SCP',
                'Send', 'SMB', 'SNMP', 'Syslog' or 'Email'; if the event is
                neither 'Updated SecInfo arrived' nor 'New SecInfo arrived',
                method can also be one of 'Start Task', 'HTTP Get', 'Sourcefire
                Connector' or 'verinice Connector'.
            condition_data: Data that defines the condition
            event_data: Data that defines the event
            method_data: Data that defines the method
            filter_id: Filter to apply when executing alert
            comment: Comment for the alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument="name"
            )

        if not condition:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument="condition"
            )

        if not event:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument="event"
            )

        if not method:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument="method"
            )

        if not isinstance(condition, AlertCondition):
            raise InvalidArgumentType(
                function=self.create_alert.__name__,
                argument="condition",
                arg_type=AlertCondition.__name__,
            )

        if not isinstance(event, AlertEvent):
            raise InvalidArgumentType(
                function=self.create_alert.__name__,
                argument="even",
                arg_type=AlertEvent.__name__,
            )

        if not isinstance(method, AlertMethod):
            raise InvalidArgumentType(
                function=self.create_alert.__name__,
                argument="method",
                arg_type=AlertMethod.__name__,
            )

        _check_event(event, condition, method)

        cmd = XmlCommand("create_alert")
        cmd.add_element("name", name)

        conditions = cmd.add_element("condition", condition.value)

        if condition_data is not None:
            for key, value in condition_data.items():
                _data = conditions.add_element("data", value)
                _data.add_element("name", key)

        events = cmd.add_element("event", event.value)

        if event_data is not None:
            for key, value in event_data.items():
                _data = events.add_element("data", value)
                _data.add_element("name", key)

        methods = cmd.add_element("method", method.value)

        if method_data is not None:
            for key, value in method_data.items():
                _data = methods.add_element("data", value)
                _data.add_element("name", key)

        if filter_id:
            cmd.add_element("filter", attrs={"id": filter_id})

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def delete_alert(
        self, alert_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing alert

        Arguments:
            alert_id: UUID of the alert to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not alert_id:
            raise RequiredArgument(
                function=self.delete_alert.__name__, argument="alert_id"
            )

        cmd = XmlCommand("delete_alert")
        cmd.set_attribute("alert_id", alert_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_alerts(
        self,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> Any:
        """Request a list of alerts

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: True to request the alerts in the trashcan
            tasks: Whether to include the tasks using the alerts
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_alerts")

        add_filter(cmd, filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_alert(self, alert_id: str, *, tasks: Optional[bool] = None) -> Any:
        """Request a single alert

        Arguments:
            alert_id: UUID of an existing alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_alerts")

        if not alert_id:
            raise RequiredArgument(
                function=self.get_alert.__name__, argument="alert_id"
            )

        cmd.set_attribute("alert_id", alert_id)

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return self._send_xml_command(cmd)

    def modify_alert(
        self,
        alert_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        filter_id: Optional[str] = None,
        event: Optional[AlertEvent] = None,
        event_data: Optional[dict] = None,
        condition: Optional[AlertCondition] = None,
        condition_data: Optional[dict] = None,
        method: Optional[AlertMethod] = None,
        method_data: Optional[dict] = None,
    ) -> Any:
        """Modifies an existing alert.

        Arguments:
            alert_id: UUID of the alert to be modified.
            name: Name of the Alert.
            condition: The condition that must be satisfied for the alert to
                occur. If the event is either 'Updated SecInfo
                arrived' or 'New SecInfo arrived', condition must be 'Always'.
                Otherwise, condition can also be on of 'Severity at least',
                'Filter count changed' or 'Filter count at least'.
            condition_data: Data that defines the condition
            event: The event that must happen for the alert to occur, one of
                'Task run status changed', 'Updated SecInfo arrived' or
                'New SecInfo arrived'
            event_data: Data that defines the event
            method: The method by which the user is alerted, one of 'SCP',
                'Send', 'SMB', 'SNMP', 'Syslog' or 'Email';
                if the event is neither 'Updated SecInfo arrived' nor
                'New SecInfo arrived', method can also be one of 'Start Task',
                'HTTP Get', 'Sourcefire Connector' or 'verinice Connector'.
            method_data: Data that defines the method
            filter_id: Filter to apply when executing alert
            comment: Comment for the alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        if not alert_id:
            raise RequiredArgument(
                function=self.modify_alert.__name__, argument="alert_id"
            )

        cmd = XmlCommand("modify_alert")
        cmd.set_attribute("alert_id", str(alert_id))

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if filter_id:
            cmd.add_element("filter", attrs={"id": filter_id})

        if condition:
            if not isinstance(condition, AlertCondition):
                raise InvalidArgumentType(
                    function=self.modify_alert.__name__,
                    argument="condition",
                    arg_type=AlertCondition.__name__,
                )

            conditions = cmd.add_element("condition", condition.value)

            if condition_data is not None:
                for key, value in condition_data.items():
                    _data = conditions.add_element("data", value)
                    _data.add_element("name", key)

        if method:
            if not isinstance(method, AlertMethod):
                raise InvalidArgumentType(
                    function=self.modify_alert.__name__,
                    argument="method",
                    arg_type=AlertMethod.__name__,
                )

            methods = cmd.add_element("method", method.value)

            if method_data is not None:
                for key, value in method_data.items():
                    _data = methods.add_element("data", value)
                    _data.add_element("name", key)

        if event:
            if not isinstance(event, AlertEvent):
                raise InvalidArgumentType(
                    function=self.modify_alert.__name__,
                    argument="event",
                    arg_type=AlertEvent.__name__,
                )

            _check_event(event, condition, method)

            events = cmd.add_element("event", event.value)

            if event_data is not None:
                for key, value in event_data.items():
                    _data = events.add_element("data", value)
                    _data.add_element("name", key)

        return self._send_xml_command(cmd)

    def test_alert(self, alert_id: str) -> Any:
        """Run an alert

        Invoke a test run of an alert

        Arguments:
            alert_id: UUID of the alert to be tested

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not alert_id:
            raise InvalidArgument("test_alert requires an alert_id argument")

        cmd = XmlCommand("test_alert")
        cmd.set_attribute("alert_id", alert_id)

        return self._send_xml_command(cmd)

    def trigger_alert(
        self,
        alert_id: str,
        report_id: str,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[str] = None,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        delta_report_id: Optional[str] = None,
    ) -> Any:
        """Run an alert by ignoring its event and conditions

        The alert is triggered to run immediately with the provided filtered
        report by ignoring the even and condition settings.

        Arguments:
            alert_id: UUID of the alert to be run
            report_id: UUID of the report to be provided to the alert
            filter: Filter term to use to filter results in the report
            filter_id: UUID of filter to use to filter results in the report
            report_format_id: UUID of report format to use
                              or ReportFormatType (enum)
            delta_report_id: UUID of an existing report to compare report to.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not alert_id:
            raise RequiredArgument(
                function=self.trigger_alert.__name__,
                argument="alert_id argument",
            )

        if not report_id:
            raise RequiredArgument(
                function=self.trigger_alert.__name__,
                argument="report_id argument",
            )

        cmd = XmlCommand("get_reports")
        cmd.set_attribute("report_id", report_id)
        cmd.set_attribute("alert_id", alert_id)

        add_filter(cmd, filter_string, filter_id)

        if report_format_id:
            if isinstance(report_format_id, ReportFormatType):
                report_format_id = report_format_id.value

            cmd.set_attribute("format_id", report_format_id)

        if delta_report_id:
            cmd.set_attribute("delta_report_id", delta_report_id)

        return self._send_xml_command(cmd)
