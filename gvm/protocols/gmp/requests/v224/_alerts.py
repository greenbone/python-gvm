# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Union

from gvm._enum import Enum
from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.utils import to_bool
from gvm.xml import XmlCommand

from .._entity_id import EntityID
from ._report_formats import ReportFormatType


class AlertEvent(Enum):
    """Enum for alert event types"""

    TASK_RUN_STATUS_CHANGED = "Task run status changed"
    UPDATED_SECINFO_ARRIVED = "Updated SecInfo arrived"
    NEW_SECINFO_ARRIVED = "New SecInfo arrived"
    TICKET_RECEIVED = "Ticket received"
    ASSIGNED_TICKET_CHANGED = "Assigned ticket changed"
    OWNED_TICKET_CHANGED = "Owned ticket changed"


class AlertCondition(Enum):
    """Enum for alert condition types"""

    ALWAYS = "Always"
    ERROR = "Error"
    SEVERITY_AT_LEAST = "Severity at least"
    SEVERITY_CHANGED = "Severity changed"
    FILTER_COUNT_CHANGED = "Filter count changed"
    FILTER_COUNT_AT_LEAST = "Filter count at least"


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


def _check_event(
    event: AlertEvent,
    condition: Optional[AlertCondition],
    method: Optional[AlertMethod],
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


class Alerts:
    @classmethod
    def create_alert(
        cls,
        name: str,
        condition: AlertCondition,
        event: AlertEvent,
        method: AlertMethod,
        *,
        method_data: Optional[dict[str, str]] = None,
        event_data: Optional[dict[str, str]] = None,
        condition_data: Optional[dict[str, str]] = None,
        filter_id: Optional[EntityID] = None,
        comment: Optional[str] = None,
    ) -> Request:
        """Create a new alert

        Args:
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
        """
        if not name:
            raise RequiredArgument(
                function=cls.create_alert.__name__, argument="name"
            )

        if not condition:
            raise RequiredArgument(
                function=cls.create_alert.__name__, argument="condition"
            )

        if not event:
            raise RequiredArgument(
                function=cls.create_alert.__name__, argument="event"
            )

        if not method:
            raise RequiredArgument(
                function=cls.create_alert.__name__, argument="method"
            )

        if not isinstance(condition, AlertCondition):
            condition = AlertCondition(condition)
        if not isinstance(event, AlertEvent):
            event = AlertEvent(event)
        if not isinstance(method, AlertMethod):
            method = AlertMethod(method)

        _check_event(event, condition, method)

        cmd = XmlCommand("create_alert")
        cmd.add_element("name", name)

        conditions = cmd.add_element("condition", condition.value)

        if condition_data is not None:
            for key, value in condition_data.items():
                xml_data = conditions.add_element("data", value)
                xml_data.add_element("name", key)

        events = cmd.add_element("event", event.value)

        if event_data is not None:
            for key, value in event_data.items():
                xml_data = events.add_element("data", value)
                xml_data.add_element("name", key)

        methods = cmd.add_element("method", method.value)

        if method_data is not None:
            for key, value in method_data.items():
                xml_data = methods.add_element("data", value)
                xml_data.add_element("name", key)

        if filter_id:
            cmd.add_element("filter", attrs={"id": filter_id})

        if comment:
            cmd.add_element("comment", comment)

        return cmd

    @classmethod
    def modify_alert(
        cls,
        alert_id: EntityID,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        event: Optional[Union[AlertEvent, str]] = None,
        event_data: Optional[dict] = None,
        condition: Optional[Union[AlertCondition, str]] = None,
        condition_data: Optional[dict[str, str]] = None,
        method: Optional[Union[AlertMethod, str]] = None,
        method_data: Optional[dict[str, str]] = None,
    ) -> Request:
        """Modify an existing alert.

        Args:
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
        """
        if not alert_id:
            raise RequiredArgument(
                function=cls.modify_alert.__name__, argument="alert_id"
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
                condition = AlertCondition(condition)

            conditions = cmd.add_element("condition", condition.value)

            if condition_data is not None:
                for key, value in condition_data.items():
                    xml_data = conditions.add_element("data", value)
                    xml_data.add_element("name", key)

        if method:
            if not isinstance(method, AlertMethod):
                method = AlertMethod(method)

            methods = cmd.add_element("method", method.value)

            if method_data is not None:
                for key, value in method_data.items():
                    xml_data = methods.add_element("data", value)
                    xml_data.add_element("name", key)

        if event:
            if not isinstance(event, AlertEvent):
                event = AlertEvent(event)

            _check_event(event, condition, method)  # type: ignore

            events = cmd.add_element("event", event.value)

            if event_data is not None:
                for key, value in event_data.items():
                    xml_data = events.add_element("data", value)
                    xml_data.add_element("name", key)

        return cmd

    @classmethod
    def clone_alert(cls, alert_id: EntityID) -> Request:
        """Clone an existing alert

        Args:
            alert_id: UUID of the alert to clone from
        """
        if not alert_id:
            raise RequiredArgument(
                function=cls.clone_alert.__name__, argument="alert_id"
            )

        cmd = XmlCommand("create_alert")
        cmd.add_element("copy", str(alert_id))
        return cmd

    @classmethod
    def delete_alert(
        cls, alert_id: EntityID, *, ultimate: Optional[bool] = False
    ) -> Request:
        """Delete an existing alert

        Args:
            alert_id: UUID of the alert to delete
            ultimate: Whether to remove entirely or to the trashcan.
        """
        if not alert_id:
            raise RequiredArgument(
                function=cls.delete_alert.__name__, argument="alert_id"
            )

        cmd = XmlCommand("delete_alert")
        cmd.set_attribute("alert_id", str(alert_id))
        cmd.set_attribute("ultimate", to_bool(ultimate))
        return cmd

    @classmethod
    def test_alert(cls, alert_id: EntityID) -> Request:
        """Run an alert

        Invoke a test run of an alert

        Args:
            alert_id: UUID of the alert to be tested
        """
        if not alert_id:
            raise RequiredArgument(
                function=cls.test_alert.__name__, argument="alert_id"
            )

        cmd = XmlCommand("test_alert")
        cmd.set_attribute("alert_id", str(alert_id))
        return cmd

    @classmethod
    def trigger_alert(
        cls,
        alert_id: EntityID,
        report_id: EntityID,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        report_format_id: Optional[Union[EntityID, ReportFormatType]] = None,
        delta_report_id: Optional[EntityID] = None,
    ) -> Request:
        """Run an alert by ignoring its event and conditions

        The alert is triggered to run immediately with the provided filtered
        report by ignoring the even and condition settings.

        Args:
            alert_id: UUID of the alert to be run
            report_id: UUID of the report to be provided to the alert
            filter: Filter term to use to filter results in the report
            filter_id: UUID of filter to use to filter results in the report
            report_format_id: UUID of report format to use                              or ReportFormatType (enum)
            delta_report_id: UUID of an existing report to compare report to.
        """
        if not alert_id:
            raise RequiredArgument(
                function=cls.trigger_alert.__name__,
                argument="alert_id argument",
            )

        if not report_id:
            raise RequiredArgument(
                function=cls.trigger_alert.__name__,
                argument="report_id argument",
            )

        cmd = XmlCommand("get_reports")
        cmd.set_attribute("report_id", str(report_id))
        cmd.set_attribute("alert_id", str(alert_id))
        cmd.add_filter(filter_string, filter_id)

        if report_format_id:
            cmd.set_attribute("format_id", str(report_format_id))

        if delta_report_id:
            cmd.set_attribute("delta_report_id", str(delta_report_id))

        return cmd

    @staticmethod
    def get_alerts(
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> Request:
        """Request a list of alerts

        Args:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: True to request the alerts in the trashcan
            tasks: Whether to include the tasks using the alerts
        """
        cmd = XmlCommand("get_alerts")
        cmd.add_filter(filter_string, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return cmd

    @classmethod
    def get_alert(
        cls, alert_id: EntityID, *, tasks: Optional[bool] = None
    ) -> Request:
        """Request a single alert

        Arguments:
            alert_id: UUID of an existing alert
            tasks: Whether to include the tasks using the alert
        """
        cmd = XmlCommand("get_alerts")

        if not alert_id:
            raise RequiredArgument(
                function=cls.get_alert.__name__, argument="alert_id"
            )

        cmd.set_attribute("alert_id", str(alert_id))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return cmd
