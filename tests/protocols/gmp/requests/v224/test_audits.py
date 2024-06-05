# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import Audits, HostsOrdering


class AuditsTestCase(unittest.TestCase):
    def test_create_audit(self):
        request = Audits.create_audit(
            name="foo", policy_id="c1", target_id="t1", scanner_id="s1"
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"</create_task>",
        )

    def test_create_audit_with_comment(self):
        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            comment="bar",
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<comment>bar</comment>"
            b"</create_task>",
        )

    def test_create_audit_with_single_alert(self):
        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            alert_ids=["a1"],
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b'<alert id="a1"/>'
            b"</create_task>",
        )

    def test_create_audit_with_multiple_alerts(self):
        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            alert_ids=["a1", "a2"],
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b'<alert id="a1"/>'
            b'<alert id="a2"/>'
            b"</create_task>",
        )

    def test_create_audit_with_empty_alert_ids(self):
        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            alert_ids=[],
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"</create_task>",
        )

    def test_create_audit_with_alterable(self):
        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            alterable=True,
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<alterable>1</alterable>"
            b"</create_task>",
        )

        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            alterable=False,
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<alterable>0</alterable>"
            b"</create_task>",
        )

    def test_create_audit_with_hosts_ordering(self):
        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            hosts_ordering=HostsOrdering.RANDOM,
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<hosts_ordering>random</hosts_ordering>"
            b"</create_task>",
        )

        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            hosts_ordering="random",
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<hosts_ordering>random</hosts_ordering>"
            b"</create_task>",
        )

    def test_create_audit_with_schedule_id(self):
        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            schedule_id="s1",
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b'<schedule id="s1"/>'
            b"</create_task>",
        )

    def test_create_audit_with_schedule_and_schedule_periods(self):
        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            schedule_id="s1",
            schedule_periods=0,
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b'<schedule id="s1"/>'
            b"<schedule_periods>0</schedule_periods>"
            b"</create_task>",
        )

        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            schedule_id="s1",
            schedule_periods=5,
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b'<schedule id="s1"/>'
            b"<schedule_periods>5</schedule_periods>"
            b"</create_task>",
        )

    def test_create_audit_with_observers(self):
        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            observers=["u1", "u2"],
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<observers>u1,u2</observers>"
            b"</create_task>",
        )

    def test_create_audit_with_preferences(self):
        request = Audits.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            preferences={"foo": "bar", "lorem": "ipsum"},
        )

        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>audit</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<preferences>"
            b"<preference>"
            b"<scanner_name>foo</scanner_name>"
            b"<value>bar</value>"
            b"</preference>"
            b"<preference>"
            b"<scanner_name>lorem</scanner_name>"
            b"<value>ipsum</value>"
            b"</preference>"
            b"</preferences>"
            b"</create_task>",
        )

    def test_create_audit_don_t_allow_container_task(self):
        with self.assertRaises(InvalidArgument):
            Audits.create_audit(
                name="foo",
                policy_id="c1",
                target_id="0",
                scanner_id="s1",
                observers="",
            )

        # target_id=0 is considered as False
        with self.assertRaises(RequiredArgument):
            Audits.create_audit(
                name="foo",
                policy_id="c1",
                target_id=0,
                scanner_id="s1",
                observers="",
            )

    def test_create_audit_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Audits.create_audit(
                "", policy_id="c1", target_id="t1", scanner_id="s1"
            )

        with self.assertRaises(RequiredArgument):
            Audits.create_audit(
                None, policy_id="c1", target_id="t1", scanner_id="s1"
            )

    def test_create_audit_missing_policy_id(self):
        with self.assertRaises(RequiredArgument):
            Audits.create_audit(
                "foo", policy_id="", target_id="t1", scanner_id="s1"
            )

        with self.assertRaises(RequiredArgument):
            Audits.create_audit(
                "foo", policy_id=None, target_id="t1", scanner_id="s1"
            )

    def test_create_audit_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            Audits.create_audit(
                "foo", policy_id="c1", target_id="", scanner_id="s1"
            )

        with self.assertRaises(RequiredArgument):
            Audits.create_audit(
                "foo", policy_id="c1", target_id=None, scanner_id="s1"
            )

    def test_create_audit_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            Audits.create_audit(
                "foo", policy_id="c1", target_id="t1", scanner_id=""
            )

        with self.assertRaises(RequiredArgument):
            Audits.create_audit(
                "foo", policy_id="c1", target_id="t1", scanner_id=None
            )

    def test_create_audit_invalid_hosts_ordering(self):
        with self.assertRaises(InvalidArgument):
            Audits.create_audit(
                "foo",
                policy_id="c1",
                target_id="t1",
                scanner_id="s1",
                hosts_ordering="invalid",
            )

    def test_create_audit_with_schedule_and_invalid_schedule_periods(self):
        with self.assertRaises(InvalidArgument):
            Audits.create_audit(
                name="foo",
                policy_id="c1",
                target_id="t1",
                scanner_id="s1",
                schedule_id="s1",
                schedule_periods=-1,
            )

        with self.assertRaises(InvalidArgument):
            Audits.create_audit(
                name="foo",
                policy_id="c1",
                target_id="t1",
                scanner_id="s1",
                schedule_id="s1",
                schedule_periods="invalid",
            )

    def test_modify_audit(self):
        request = Audits.modify_audit("t1")

        self.assertEqual(bytes(request), b'<modify_task task_id="t1"/>')

    def test_modify_audit_missing_audit_id(self):
        with self.assertRaises(RequiredArgument):
            Audits.modify_audit(None)

        with self.assertRaises(RequiredArgument):
            Audits.modify_audit("")

    def test_modify_audit_with_name(self):
        request = Audits.modify_audit(audit_id="t1", name="foo")

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1"><name>foo</name></modify_task>',
        )

    def test_modify_audit_with_policy_id(self):
        request = Audits.modify_audit(audit_id="t1", policy_id="c1")

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1"><config id="c1"/></modify_task>',
        )

    def test_modify_audit_with_target_id(self):
        request = Audits.modify_audit(audit_id="t1", target_id="t1")

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1"><target id="t1"/></modify_task>',
        )

    def test_modify_audit_with_scanner_id(self):
        request = Audits.modify_audit(audit_id="t1", scanner_id="s1")

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1"><scanner id="s1"/></modify_task>',
        )

    def test_modify_audit_with_schedule_id(self):
        request = Audits.modify_audit(audit_id="t1", schedule_id="s1")

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1"><schedule id="s1"/></modify_task>',
        )

    def test_modify_audit_with_comment(self):
        request = Audits.modify_audit(audit_id="t1", comment="bar")

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1">'
            b"<comment>bar</comment>"
            b"</modify_task>",
        )

    def test_modify_audit_with_alerts_ids(self):
        request = Audits.modify_audit(audit_id="t1", alert_ids=["a1", "a2"])

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1">'
            b'<alert id="a1"/>'
            b'<alert id="a2"/>'
            b"</modify_task>",
        )

    def test_modify_audit_with_empty_alert_ids(self):
        request = Audits.modify_audit(audit_id="t1", alert_ids=[])

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1"><alert id="0"/></modify_task>',
        )

    def test_modify_audit_with_alterable(self):
        request = Audits.modify_audit(audit_id="t1", alterable=True)

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1"><alterable>1</alterable></modify_task>',
        )

        request = Audits.modify_audit(audit_id="t1", alterable=False)

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1"><alterable>0</alterable></modify_task>',
        )

    def test_modify_audit_with_hosts_ordering(self):
        request = Audits.modify_audit(
            audit_id="t1", hosts_ordering=HostsOrdering.RANDOM
        )
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1">'
            b"<hosts_ordering>random</hosts_ordering>"
            b"</modify_task>",
        )

        request = Audits.modify_audit(audit_id="t1", hosts_ordering="random")

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1">'
            b"<hosts_ordering>random</hosts_ordering>"
            b"</modify_task>",
        )

    def test_modify_audit_with_schedule_periods(self):
        request = Audits.modify_audit(audit_id="t1", schedule_periods=0)

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1">'
            b"<schedule_periods>0</schedule_periods>"
            b"</modify_task>",
        )

        request = Audits.modify_audit(audit_id="t1", schedule_periods=5)

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1">'
            b"<schedule_periods>5</schedule_periods>"
            b"</modify_task>",
        )

    def test_modify_audit_with_observers(self):
        request = Audits.modify_audit(audit_id="t1", observers=["u1", "u2"])

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1">'
            b"<observers>u1,u2</observers>"
            b"</modify_task>",
        )

    def test_modify_audit_with_preferences(self):
        request = Audits.modify_audit(
            audit_id="t1", preferences={"foo": "bar", "lorem": "ipsum"}
        )

        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="t1">'
            b"<preferences>"
            b"<preference>"
            b"<scanner_name>foo</scanner_name>"
            b"<value>bar</value>"
            b"</preference>"
            b"<preference>"
            b"<scanner_name>lorem</scanner_name>"
            b"<value>ipsum</value>"
            b"</preference>"
            b"</preferences>"
            b"</modify_task>",
        )

    def test_modify_audit_invalid_hosts_ordering(self):
        with self.assertRaises(InvalidArgument):
            Audits.modify_audit(audit_id="t1", hosts_ordering="foo")

    def test_modify_audit_invalid_schedule_periods(self):
        with self.assertRaises(InvalidArgument):
            Audits.modify_audit(audit_id="t1", schedule_periods="foo")

        with self.assertRaises(InvalidArgument):
            Audits.modify_audit(audit_id="t1", schedule_periods=-1)

    def test_clone_audit(self):
        request = Audits.clone_audit("t1")

        self.assertEqual(
            bytes(request),
            b"<create_task><copy>t1</copy></create_task>",
        )

    def test_clone_audit_missing_audit_id(self):
        with self.assertRaises(RequiredArgument):
            Audits.clone_audit(None)

        with self.assertRaises(RequiredArgument):
            Audits.clone_audit("")

    def test_delete_audit(self):
        request = Audits.delete_audit("t1")

        self.assertEqual(
            bytes(request),
            b'<delete_task task_id="t1" ultimate="0"/>',
        )

    def test_delete_audit_with_ultimate(self):
        request = Audits.delete_audit("t1", ultimate=True)

        self.assertEqual(
            bytes(request),
            b'<delete_task task_id="t1" ultimate="1"/>',
        )

        request = Audits.delete_audit("t1", ultimate=False)

        self.assertEqual(
            bytes(request),
            b'<delete_task task_id="t1" ultimate="0"/>',
        )

    def test_delete_audit_missing_audit_id(self):
        with self.assertRaises(RequiredArgument):
            Audits.delete_audit(None)

        with self.assertRaises(RequiredArgument):
            Audits.delete_audit("")

    def test_get_audits(self):
        request = Audits.get_audits()

        self.assertEqual(bytes(request), b'<get_tasks usage_type="audit"/>')

    def test_get_audits_with_filter_string(self):
        request = Audits.get_audits(filter_string="name=foo")

        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="audit" filter="name=foo"/>',
        )

    def test_get_audits_with_filter_id(self):
        request = Audits.get_audits(filter_id="f1")

        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="audit" filt_id="f1"/>',
        )

    def test_get_audits_with_trash(self):
        request = Audits.get_audits(trash=True)

        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="audit" trash="1"/>',
        )

        request = Audits.get_audits(trash=False)

        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="audit" trash="0"/>',
        )

    def test_get_audits_with_details(self):
        request = Audits.get_audits(details=True)

        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="audit" details="1"/>',
        )

        request = Audits.get_audits(details=False)

        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="audit" details="0"/>',
        )

    def test_get_audits_with_schedules_only(self):
        request = Audits.get_audits(schedules_only=True)

        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="audit" schedules_only="1"/>',
        )

        request = Audits.get_audits(schedules_only=False)

        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="audit" schedules_only="0"/>',
        )

    def test_get_audit(self):
        request = Audits.get_audit("t1")

        self.assertEqual(
            bytes(request),
            b'<get_tasks task_id="t1" usage_type="audit" details="1"/>',
        )

    def test_get_audit_missing_audit_id(self):
        with self.assertRaises(RequiredArgument):
            Audits.get_audit(None)

        with self.assertRaises(RequiredArgument):
            Audits.get_audit("")

    def test_start_audit(self):
        request = Audits.start_audit("t1")

        self.assertEqual(
            bytes(request),
            b'<start_task task_id="t1"/>',
        )

    def test_start_audit_missing_audit_id(self):
        with self.assertRaises(RequiredArgument):
            Audits.start_audit(None)

        with self.assertRaises(RequiredArgument):
            Audits.start_audit("")

    def test_stop_audit(self):
        request = Audits.stop_audit("t1")

        self.assertEqual(
            bytes(request),
            b'<stop_task task_id="t1"/>',
        )

    def test_stop_audit_missing_audit_id(self):
        with self.assertRaises(RequiredArgument):
            Audits.stop_audit(None)

        with self.assertRaises(RequiredArgument):
            Audits.stop_audit("")

    def test_resume_audit(self):
        request = Audits.resume_audit("t1")

        self.assertEqual(
            bytes(request),
            b'<resume_task task_id="t1"/>',
        )

    def test_resume_audit_missing_audit_id(self):
        with self.assertRaises(RequiredArgument):
            Audits.resume_audit(None)

        with self.assertRaises(RequiredArgument):
            Audits.resume_audit("")
