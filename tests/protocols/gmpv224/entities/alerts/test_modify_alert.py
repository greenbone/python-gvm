# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import (
    AlertCondition,
    AlertEvent,
    AlertMethod,
)


class GmpModifyAlertTestMixin:
    def test_modify_alert(self):
        self.gmp.modify_alert(alert_id="a1")

        self.connection.send.has_been_called_with(
            b'<modify_alert alert_id="a1"/>'
        )

    def test_modify_alert_without_alert_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_alert(alert_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_alert(alert_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_alert("")

    def test_modify_alert_with_comment(self):
        self.gmp.modify_alert(alert_id="a1", comment="lorem")

        self.connection.send.has_been_called_with(
            b'<modify_alert alert_id="a1">'
            b"<comment>lorem</comment>"
            b"</modify_alert>"
        )

    def test_modify_alert_with_name(self):
        self.gmp.modify_alert(alert_id="a1", name="lorem")

        self.connection.send.has_been_called_with(
            b'<modify_alert alert_id="a1">'
            b"<name>lorem</name>"
            b"</modify_alert>"
        )

    def test_modify_alert_with_filter_id(self):
        self.gmp.modify_alert(alert_id="a1", filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<modify_alert alert_id="a1"><filter id="f1"/></modify_alert>'
        )

    def test_modify_alert_invalid_condition(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_alert(
                alert_id="a1",
                condition="bar",
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.SCP,
            )

    def test_modify_alert_invalid_event(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_alert(
                alert_id="a1",
                condition=AlertCondition.ALWAYS,
                event="lorem",
                method=AlertMethod.SCP,
            )

    def test_modify_alert_invalid_method(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_alert(
                alert_id="a1",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method="ipsum",
            )

    def test_modify_alert_with_event_missing_method(self):
        with self.assertRaisesRegex(RequiredArgument, "method is required"):
            self.gmp.modify_alert(
                alert_id="a1",
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                condition=AlertCondition.ALWAYS,
            )

        with self.assertRaisesRegex(RequiredArgument, "method is required"):
            self.gmp.modify_alert(
                alert_id="a1",
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                condition=AlertCondition.ALWAYS,
            )

        with self.assertRaisesRegex(RequiredArgument, "method is required"):
            self.gmp.modify_alert(
                alert_id="a1",
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                condition=AlertCondition.ALWAYS,
            )

    def test_modify_alert_with_event_missing_condition(self):
        with self.assertRaisesRegex(RequiredArgument, "condition is required"):
            self.gmp.modify_alert(
                alert_id="a1",
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.SCP,
            )

        with self.assertRaisesRegex(RequiredArgument, "condition is required"):
            self.gmp.modify_alert(
                alert_id="a1",
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.SCP,
            )

        with self.assertRaisesRegex(RequiredArgument, "condition is required"):
            self.gmp.modify_alert(
                alert_id="a1",
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.SCP,
            )

    def test_modify_alert_invalid_condition_for_secinfo(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_alert(
                alert_id="a1",
                condition="Severity at least",
                event="Updated SecInfo arrived",
                method="Email",
            )

    def test_modify_alert_invalid_method_for_secinfo(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_alert(
                alert_id="a1",
                condition="Always",
                event="Updated SecInfo arrived",
                method="HTTP Get",
            )

    def test_modify_alert_with_event_data(self):
        self.gmp.modify_alert(
            alert_id="a1",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            event_data={"foo": "bar"},
        )

        self.connection.send.has_been_called_with(
            b'<modify_alert alert_id="a1">'
            b"<condition>Always</condition>"
            b"<method>Email</method>"
            b"<event>Task run status changed"
            b"<data>bar<name>foo</name></data>"
            b"</event>"
            b"</modify_alert>"
        )

    def test_modify_alert_with_condition_data(self):
        self.gmp.modify_alert(
            alert_id="a1",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            condition_data={"foo": "bar"},
        )

        self.connection.send.has_been_called_with(
            b'<modify_alert alert_id="a1">'
            b"<condition>Always<data>bar<name>foo</name></data></condition>"
            b"<method>Email</method>"
            b"<event>Task run status changed</event>"
            b"</modify_alert>"
        )

    def test_modify_alert_with_method_data(self):
        self.gmp.modify_alert(
            alert_id="a1",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            method_data={"foo": "bar"},
        )

        self.connection.send.has_been_called_with(
            b'<modify_alert alert_id="a1">'
            b"<condition>Always</condition>"
            b"<method>Email<data>bar<name>foo</name></data></method>"
            b"<event>Task run status changed</event>"
            b"</modify_alert>"
        )

    def test_modify_missing_method_for_ticket_received(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_alert(
                alert_id="a1",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=None,
            )

    def test_modify_missing_condition_for_ticket_received(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_alert(
                alert_id="a1",
                condition=None,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.EMAIL,
            )
