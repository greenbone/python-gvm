# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from collections import OrderedDict

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import HostsOrdering


class GmpModifyAuditTestMixin:
    def test_modify_task(self):
        self.gmp.modify_audit("t1")

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1"/>'
        )

    def test_modify_audit_missing_task_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_audit(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_audit("")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_audit(audit_id="")

    def test_modify_audit_with_name(self):
        self.gmp.modify_audit(audit_id="t1", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1"><name>foo</name></modify_task>'
        )

    def test_modify_audit_with_policy_id(self):
        self.gmp.modify_audit(audit_id="t1", policy_id="c1")

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1"><config id="c1"/></modify_task>'
        )

    def test_modify_audit_with_target_id(self):
        self.gmp.modify_audit(audit_id="t1", target_id="t1")

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1"><target id="t1"/></modify_task>'
        )

    def test_modify_audit_with_scanner_id(self):
        self.gmp.modify_audit(audit_id="t1", scanner_id="s1")

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1"><scanner id="s1"/></modify_task>'
        )

    def test_modify_audit_with_schedule_id(self):
        self.gmp.modify_audit(audit_id="t1", schedule_id="s1")

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1"><schedule id="s1"/></modify_task>'
        )

    def test_modify_audit_with_comment(self):
        self.gmp.modify_audit(audit_id="t1", comment="bar")

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1">'
            b"<comment>bar</comment>"
            b"</modify_task>"
        )

    def test_modify_audit_with_alerts_ids(self):
        self.gmp.modify_audit(audit_id="t1", alert_ids=["a1", "a2", "a3"])

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1">'
            b'<alert id="a1"/>'
            b'<alert id="a2"/>'
            b'<alert id="a3"/>'
            b"</modify_task>"
        )

    def test_modify_audit_with_empty_alert_ids(self):
        self.gmp.modify_audit(audit_id="t1", alert_ids=[])

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1"><alert id="0"/></modify_task>'
        )

    def test_modify_audit_with_alterable(self):
        self.gmp.modify_audit(audit_id="t1", alterable=True)

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1">'
            b"<alterable>1</alterable>"
            b"</modify_task>"
        )

        self.gmp.modify_audit(audit_id="t1", alterable=False)

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1">'
            b"<alterable>0</alterable>"
            b"</modify_task>"
        )

    def test_modify_audit_with_hosts_ordering(self):
        self.gmp.modify_audit(
            audit_id="t1", hosts_ordering=HostsOrdering.REVERSE
        )

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1">'
            b"<hosts_ordering>reverse</hosts_ordering>"
            b"</modify_task>"
        )

    def test_modify_audit_invalid_hosts_ordering(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_audit(audit_id="t1", hosts_ordering="foo")

    def test_modify_audit_with_schedule(self):
        self.gmp.modify_audit(audit_id="t1", schedule_id="s1")

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1"><schedule id="s1"/></modify_task>'
        )

    def test_modify_audit_with_schedule_periods(self):
        self.gmp.modify_audit(audit_id="t1", schedule_periods=0)

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1">'
            b"<schedule_periods>0</schedule_periods>"
            b"</modify_task>"
        )

        self.gmp.modify_audit(audit_id="t1", schedule_periods=5)

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1">'
            b"<schedule_periods>5</schedule_periods>"
            b"</modify_task>"
        )

    def test_modify_audit_invalid_schedule_periods(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_audit(audit_id="t1", schedule_periods="foo")

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_audit(audit_id="t1", schedule_periods=-1)

    def test_modify_audit_with_observers(self):
        self.gmp.modify_audit(audit_id="t1", observers=["u1", "u2"])

        self.connection.send.has_been_called_with(
            b'<modify_task task_id="t1">'
            b"<observers>u1,u2</observers>"
            b"</modify_task>"
        )

    def test_modify_audit_with_preferences(self):
        self.gmp.modify_audit(
            audit_id="t1",
            preferences=OrderedDict([("foo", "bar"), ("lorem", "ipsum")]),
        )

        self.connection.send.has_been_called_with(
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
            b"</modify_task>"
        )
