# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import (
    AlertCondition,
    AlertEvent,
    AlertMethod,
    Alerts,
    ReportFormatType,
)


class AlertsTestCase(unittest.TestCase):
    def test_create_alerts(self):
        request = Alerts.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
        )

        self.assertEqual(
            bytes(request),
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always</condition>"
            b"<event>Task run status changed</event>"
            b"<method>Email</method>"
            b"</create_alert>",
        )

    def test_create_alert_with_filter_id(self):
        request = Alerts.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            filter_id="f1",
        )

        self.assertEqual(
            bytes(request),
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always</condition>"
            b"<event>Task run status changed</event>"
            b"<method>Email</method>"
            b'<filter id="f1"/>'
            b"</create_alert>",
        )

    def test_create_alert_with_comment(self):
        request = Alerts.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            comment="bar",
        )

        self.assertEqual(
            bytes(request),
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always</condition>"
            b"<event>Task run status changed</event>"
            b"<method>Email</method>"
            b"<comment>bar</comment>"
            b"</create_alert>",
        )

    def test_create_alert_with_condition_data(self):
        request = Alerts.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            condition_data={"foo": "bar"},
        )

        self.assertEqual(
            bytes(request),
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always<data>bar<name>foo</name></data></condition>"
            b"<event>Task run status changed</event>"
            b"<method>Email</method>"
            b"</create_alert>",
        )

    def test_create_alert_with_event_data(self):
        request = Alerts.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            event_data={"foo": "bar"},
        )

        self.assertEqual(
            bytes(request),
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always</condition>"
            b"<event>Task run status changed"
            b"<data>bar<name>foo</name></data>"
            b"</event>"
            b"<method>Email</method>"
            b"</create_alert>",
        )

    def test_create_alert_with_method_data(self):
        request = Alerts.create_alert(
            name="foo",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            method_data={"foo": "bar"},
        )

        self.assertEqual(
            bytes(request),
            b"<create_alert>"
            b"<name>foo</name>"
            b"<condition>Always</condition>"
            b"<event>Task run status changed</event>"
            b"<method>Email<data>bar<name>foo</name></data></method>"
            b"</create_alert>",
        )

    def test_create_alert_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Alerts.create_alert(
                "",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

        with self.assertRaises(RequiredArgument):
            Alerts.create_alert(
                None,
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

    def test_create_alert_missing_event(self):
        with self.assertRaises(RequiredArgument):
            Alerts.create_alert(
                "foo",
                condition=AlertCondition.ALWAYS,
                event=None,
                method=AlertMethod.EMAIL,
            )

        with self.assertRaises(RequiredArgument):
            Alerts.create_alert(
                "foo",
                condition=AlertCondition.ALWAYS,
                event="",
                method=AlertMethod.EMAIL,
            )

    def test_create_alert_missing_condition(self):
        with self.assertRaises(RequiredArgument):
            Alerts.create_alert(
                "foo",
                condition=None,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

        with self.assertRaises(RequiredArgument):
            Alerts.create_alert(
                "foo",
                condition="",
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

    def test_create_alert_missing_method(self):
        with self.assertRaises(RequiredArgument):
            Alerts.create_alert(
                "foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=None,
            )

        with self.assertRaises(RequiredArgument):
            Alerts.create_alert(
                "foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method="",
            )

    def test_create_alert_invalid_condition(self):
        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                "foo",
                condition="foo",
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

    def test_create_alert_invalid_event(self):
        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                "foo",
                condition=AlertCondition.ALWAYS,
                event="foo",
                method=AlertMethod.EMAIL,
            )

    def test_create_alert_invalid_method(self):
        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                "foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method="foo",
            )

    def test_create_alert_invalid_condition_for_secinfo(self):
        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.SEVERITY_AT_LEAST,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.EMAIL,
            )

    def test_create_alert_invalid_method_for_secinfo(self):
        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.HTTP_GET,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.ALEMBA_VFIRE,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.SOURCEFIRE_CONNECTOR,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.START_TASK,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.TIPPINGPOINT_SMS,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.VERINICE_CONNECTOR,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.HTTP_GET,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.ALEMBA_VFIRE,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.SOURCEFIRE_CONNECTOR,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.START_TASK,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.TIPPINGPOINT_SMS,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.VERINICE_CONNECTOR,
            )

    def test_create_alert_missing_method_for_ticket_received(self):
        with self.assertRaises(RequiredArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=None,
            )

    def test_create_alert_missing_condition_for_ticket_received(self):
        with self.assertRaises(RequiredArgument):
            Alerts.create_alert(
                name="foo",
                condition=None,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.EMAIL,
            )

    def test_create_alert_invalid_method_for_ticket_received(self):
        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.HTTP_GET,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.SCP,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.SEND,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.SMB,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.SNMP,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.ALEMBA_VFIRE,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.VERINICE_CONNECTOR,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.TIPPINGPOINT_SMS,
            )

        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.SOURCEFIRE_CONNECTOR,
            )

    def test_create_alert_invalid_condition_for_task_run_status_changed(self):
        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.ERROR,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.EMAIL,
            )

    def test_create_alert_invalid_condition_for_ticket_received(self):
        with self.assertRaises(InvalidArgument):
            Alerts.create_alert(
                name="foo",
                condition=AlertCondition.FILTER_COUNT_AT_LEAST,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.EMAIL,
            )

    def test_modify_alert(self):
        request = Alerts.modify_alert(
            alert_id="a1",
        )

        self.assertEqual(bytes(request), b'<modify_alert alert_id="a1"/>')

    def test_modify_alert_missing_alert_id(self):
        with self.assertRaises(RequiredArgument):
            Alerts.modify_alert(alert_id="")

        with self.assertRaises(RequiredArgument):
            Alerts.modify_alert(alert_id=None)

    def test_modify_alert_with_comment(self):
        request = Alerts.modify_alert(
            alert_id="a1",
            comment="foo",
        )

        self.assertEqual(
            bytes(request),
            b'<modify_alert alert_id="a1"><comment>foo</comment></modify_alert>',
        )

    def test_modify_alert_with_name(self):
        request = Alerts.modify_alert(
            alert_id="a1",
            name="foo",
        )

        self.assertEqual(
            bytes(request),
            b'<modify_alert alert_id="a1"><name>foo</name></modify_alert>',
        )

    def test_modify_alert_with_filter_id(self):
        request = Alerts.modify_alert(
            alert_id="a1",
            filter_id="f1",
        )

        self.assertEqual(
            bytes(request),
            b'<modify_alert alert_id="a1"><filter id="f1"/></modify_alert>',
        )

    def test_modify_alert_with_event_data(self):
        request = Alerts.modify_alert(
            alert_id="a1",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            event_data={"foo": "bar"},
        )

        self.assertEqual(
            bytes(request),
            b'<modify_alert alert_id="a1">'
            b"<condition>Always</condition>"
            b"<method>Email</method>"
            b"<event>Task run status changed"
            b"<data>bar<name>foo</name></data>"
            b"</event>"
            b"</modify_alert>",
        )

    def test_modify_alert_with_condition_data(self):
        request = Alerts.modify_alert(
            alert_id="a1",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            condition_data={"foo": "bar"},
        )

        self.assertEqual(
            bytes(request),
            b'<modify_alert alert_id="a1">'
            b"<condition>Always<data>bar<name>foo</name></data></condition>"
            b"<method>Email</method>"
            b"<event>Task run status changed</event>"
            b"</modify_alert>",
        )

    def test_modify_alert_with_method_data(self):
        request = Alerts.modify_alert(
            alert_id="a1",
            condition=AlertCondition.ALWAYS,
            event=AlertEvent.TASK_RUN_STATUS_CHANGED,
            method=AlertMethod.EMAIL,
            method_data={"foo": "bar"},
        )

        self.assertEqual(
            bytes(request),
            b'<modify_alert alert_id="a1">'
            b"<condition>Always</condition>"
            b"<method>Email<data>bar<name>foo</name></data></method>"
            b"<event>Task run status changed</event>"
            b"</modify_alert>",
        )

    def test_modify_alert_invalid_condition(self):
        with self.assertRaises(InvalidArgument):
            Alerts.modify_alert(
                alert_id="a1",
                condition="bar",
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.SCP,
            )

    def test_modify_alert_invalid_event(self):
        with self.assertRaises(InvalidArgument):
            Alerts.modify_alert(
                alert_id="a1",
                condition=AlertCondition.ALWAYS,
                event="lorem",
                method=AlertMethod.SCP,
            )

    def test_modify_alert_invalid_method(self):
        with self.assertRaises(InvalidArgument):
            Alerts.modify_alert(
                alert_id="a1",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method="ipsum",
            )

    def test_modify_alert_with_event_missing_method(self):
        with self.assertRaisesRegex(RequiredArgument, "method is required"):
            Alerts.modify_alert(
                alert_id="a1",
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                condition=AlertCondition.ALWAYS,
            )

        with self.assertRaisesRegex(RequiredArgument, "method is required"):
            Alerts.modify_alert(
                alert_id="a1",
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                condition=AlertCondition.ALWAYS,
            )

        with self.assertRaisesRegex(RequiredArgument, "method is required"):
            Alerts.modify_alert(
                alert_id="a1",
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                condition=AlertCondition.ALWAYS,
            )

    def test_modify_alert_with_event_missing_condition(self):
        with self.assertRaisesRegex(RequiredArgument, "condition is required"):
            Alerts.modify_alert(
                alert_id="a1",
                event=AlertEvent.TASK_RUN_STATUS_CHANGED,
                method=AlertMethod.SCP,
            )

        with self.assertRaisesRegex(RequiredArgument, "condition is required"):
            Alerts.modify_alert(
                alert_id="a1",
                event=AlertEvent.NEW_SECINFO_ARRIVED,
                method=AlertMethod.SCP,
            )

        with self.assertRaisesRegex(RequiredArgument, "condition is required"):
            Alerts.modify_alert(
                alert_id="a1",
                event=AlertEvent.UPDATED_SECINFO_ARRIVED,
                method=AlertMethod.SCP,
            )

    def test_modify_alert_invalid_condition_for_secinfo(self):
        with self.assertRaises(InvalidArgument):
            Alerts.modify_alert(
                alert_id="a1",
                condition="Severity at least",
                event="Updated SecInfo arrived",
                method="Email",
            )

    def test_modify_alert_invalid_method_for_secinfo(self):
        with self.assertRaises(InvalidArgument):
            Alerts.modify_alert(
                alert_id="a1",
                condition="Always",
                event="Updated SecInfo arrived",
                method="HTTP Get",
            )

    def test_modify_missing_method_for_ticket_received(self):
        with self.assertRaises(RequiredArgument):
            Alerts.modify_alert(
                alert_id="a1",
                condition=AlertCondition.ALWAYS,
                event=AlertEvent.TICKET_RECEIVED,
                method=None,
            )

    def test_modify_missing_condition_for_ticket_received(self):
        with self.assertRaises(RequiredArgument):
            Alerts.modify_alert(
                alert_id="a1",
                condition=None,
                event=AlertEvent.TICKET_RECEIVED,
                method=AlertMethod.EMAIL,
            )

    def test_clone_alert(self):
        request = Alerts.clone_alert(alert_id="a1")

        self.assertEqual(
            bytes(request), b"<create_alert><copy>a1</copy></create_alert>"
        )

    def test_clone_alert_missing_alert_id(self):
        with self.assertRaises(RequiredArgument):
            Alerts.clone_alert(alert_id="")

        with self.assertRaises(RequiredArgument):
            Alerts.clone_alert(alert_id=None)

    def test_delete_alert(self):
        request = Alerts.delete_alert(alert_id="a1")

        self.assertEqual(
            bytes(request), b'<delete_alert alert_id="a1" ultimate="0"/>'
        )

    def test_delete_alert_ultimate(self):
        request = Alerts.delete_alert(alert_id="a1", ultimate=True)

        self.assertEqual(
            bytes(request), b'<delete_alert alert_id="a1" ultimate="1"/>'
        )

        request = Alerts.delete_alert(alert_id="a1", ultimate=False)

        self.assertEqual(
            bytes(request), b'<delete_alert alert_id="a1" ultimate="0"/>'
        )

    def test_delete_alert_missing_alert_id(self):
        with self.assertRaises(RequiredArgument):
            Alerts.delete_alert(alert_id="")

        with self.assertRaises(RequiredArgument):
            Alerts.delete_alert(alert_id=None)

    def test_test_alert(self):
        request = Alerts.test_alert(alert_id="a1")

        self.assertEqual(bytes(request), b'<test_alert alert_id="a1"/>')

    def test_test_alert_missing_alert_id(self):
        with self.assertRaises(RequiredArgument):
            Alerts.test_alert(alert_id="")

        with self.assertRaises(RequiredArgument):
            Alerts.test_alert(alert_id=None)

    def test_trigger_alert(self):
        request = Alerts.trigger_alert(alert_id="a1", report_id="r1")

        self.assertEqual(
            bytes(request), b'<get_reports report_id="r1" alert_id="a1"/>'
        )

    def test_trigger_alert_with_filter_string(self):
        request = Alerts.trigger_alert(
            alert_id="a1", report_id="r1", filter_string="name=foo"
        )

        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="r1" alert_id="a1" filter="name=foo"/>',
        )

    def test_trigger_alert_with_filter_id(self):
        request = Alerts.trigger_alert(
            alert_id="a1", report_id="r1", filter_id="f1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="r1" alert_id="a1" filt_id="f1"/>',
        )

    def test_trigger_alert_with_report_format_id(self):
        request = Alerts.trigger_alert(
            alert_id="a1", report_id="r1", report_format_id="bar"
        )

        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="r1" alert_id="a1" format_id="bar"/>',
        )

    def test_trigger_alert_with_report_format_type(self):
        request = Alerts.trigger_alert(
            alert_id="a1",
            report_id="r1",
            report_format_id=ReportFormatType.SVG,
        )

        self.assertEqual(
            bytes(request),
            '<get_reports report_id="r1" alert_id="a1" '
            f'format_id="{ReportFormatType.SVG}"/>'.encode(encoding="utf-8"),
        )

    def test_trigger_alert_with_delta_report_id(self):
        request = Alerts.trigger_alert(
            alert_id="a1", report_id="r1", delta_report_id="d1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_reports report_id="r1" alert_id="a1" delta_report_id="d1"/>',
        )

    def test_trigger_alert_missing_alert_id(self):
        with self.assertRaises(RequiredArgument):
            Alerts.trigger_alert(alert_id="", report_id="r1")

        with self.assertRaises(RequiredArgument):
            Alerts.trigger_alert(alert_id=None, report_id="r1")

    def test_trigger_alert_missing_report_id(self):
        with self.assertRaises(RequiredArgument):
            Alerts.trigger_alert(alert_id="a1", report_id="")

        with self.assertRaises(RequiredArgument):
            Alerts.trigger_alert(alert_id="a1", report_id=None)

    def test_get_alerts(self):
        request = Alerts.get_alerts()

        self.assertEqual(bytes(request), b"<get_alerts/>")

    def test_get_alerts_with_trash(self):
        request = Alerts.get_alerts(trash=True)

        self.assertEqual(bytes(request), b'<get_alerts trash="1"/>')

        request = Alerts.get_alerts(trash=False)

        self.assertEqual(bytes(request), b'<get_alerts trash="0"/>')

    def test_get_alerts_with_filter_string(self):
        request = Alerts.get_alerts(filter_string="foo=bar")

        self.assertEqual(bytes(request), b'<get_alerts filter="foo=bar"/>')

    def test_get_alerts_with_filter_id(self):
        request = Alerts.get_alerts(filter_id="f1")

        self.assertEqual(bytes(request), b'<get_alerts filt_id="f1"/>')

    def test_get_alerts_with_tasks(self):
        request = Alerts.get_alerts(tasks=True)

        self.assertEqual(bytes(request), b'<get_alerts tasks="1"/>')

        request = Alerts.get_alerts(tasks=False)

        self.assertEqual(bytes(request), b'<get_alerts tasks="0"/>')

    def test_get_alert(self):
        request = Alerts.get_alert(alert_id="a1")

        self.assertEqual(bytes(request), b'<get_alerts alert_id="a1"/>')

    def test_get_alert_with_tasks(self):
        request = Alerts.get_alert(alert_id="a1", tasks=True)

        self.assertEqual(
            bytes(request), b'<get_alerts alert_id="a1" tasks="1"/>'
        )

        request = Alerts.get_alert(alert_id="a1", tasks=False)

        self.assertEqual(
            bytes(request), b'<get_alerts alert_id="a1" tasks="0"/>'
        )

    def test_get_alert_invalid_alert_id(self):
        with self.assertRaises(RequiredArgument):
            Alerts.get_alert(alert_id=None)

        with self.assertRaises(RequiredArgument):
            Alerts.get_alert(alert_id="")
