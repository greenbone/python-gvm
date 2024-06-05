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


class GmpCreateAlertTestMixin:
    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name="",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name=None,
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

    def test_missing_condition(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name="foo", condition="", event="bar", method="lorem"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name="foo", condition=None, event="bar", method="lorem"
            )

    def test_missing_event(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name="foo", condition="bar", event="", method="lorem"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name="foo", condition="bar", event=None, method="lorem"
            )

    def test_missing_method(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name="foo", condition="bar", event="lorem", method=""
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name="foo", condition="bar", event="lorem", method=None
            )

    def test_invalid_condition(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition="bar",
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

    def test_invalid_event(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event="lorem",
                method=AlertMethod.EMAIL,
            )

    def test_invalid_method(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method="ipsum",
            )

    def test_invalid_condition_for_secinfo(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.SEVERITY_AT_LEAST,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.EMAIL,
            )

    def test_invalid_method_for_secinfo(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.HTTP_GET,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.ALEMBA_VFIRE,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.SOURCEFIRE_CONNECTOR,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.START_TASK,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.TIPPINGPOINT_SMS,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.VERINICE_CONNECTOR,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.HTTP_GET,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.ALEMBA_VFIRE,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.SOURCEFIRE_CONNECTOR,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.START_TASK,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.TIPPINGPOINT_SMS,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.VERINICE_CONNECTOR,
            )

    def test_missing_method_for_ticket_received(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=None,
            )

    def test_missing_condition_for_ticket_received(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_alert(
                name="foo",
                condition=None,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.EMAIL,
            )

    def test_invalid_method_for_ticket_received(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.HTTP_GET,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.SCP,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.SEND,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.SMB,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.SNMP,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.ALEMBA_VFIRE,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.VERINICE_CONNECTOR,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.TIPPINGPOINT_SMS,
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.SOURCEFIRE_CONNECTOR,
            )

    def test_invalid_condition_for_task_run_status_changed(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.ERROR,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

    def test_invalid_condition_for_ticket_received(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_alert(
                name="foo",
                condition=AlertCondition.FILTER_COUNT_AT_LEAST,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.EMAIL,
            )

    def test_create_alert(self):
        self.gmp.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
        )

        self.connection.send.has_been_called_with(
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always</condition>"
            b"<event>Task run status changed</event>"
            b"<method>Email</method>"
            b"</create_alert>"
        )

    def test_create_alert_with_filter_id(self):
        self.gmp.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            filter_id="f1",
        )

        self.connection.send.has_been_called_with(
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always</condition>"
            b"<event>Task run status changed</event>"
            b"<method>Email</method>"
            b'<filter id="f1"/>'
            b"</create_alert>"
        )

    def test_create_alert_with_comment(self):
        self.gmp.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            comment="hello",
        )

        self.connection.send.has_been_called_with(
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always</condition>"
            b"<event>Task run status changed</event>"
            b"<method>Email</method>"
            b"<comment>hello</comment>"
            b"</create_alert>"
        )

    def test_create_alert_with_condition_data(self):
        self.gmp.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            condition_data={"foo": "bar"},
        )

        self.connection.send.has_been_called_with(
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always<data>bar<name>foo</name></data></condition>"
            b"<event>Task run status changed</event>"
            b"<method>Email</method>"
            b"</create_alert>"
        )

    def test_create_alert_with_event_data(self):
        self.gmp.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            event_data={"foo": "bar"},
        )

        self.connection.send.has_been_called_with(
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always</condition>"
            b"<event>Task run status changed"
            b"<data>bar<name>foo</name></data>"
            b"</event>"
            b"<method>Email</method>"
            b"</create_alert>"
        )

    def test_create_alert_with_method_data(self):
        self.gmp.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            method_data={"foo": "bar"},
        )

        self.connection.send.has_been_called_with(
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always</condition>"
            b"<event>Task run status changed</event>"
            b"<method>Email<data>bar<name>foo</name></data></method>"
            b"</create_alert>"
        )
