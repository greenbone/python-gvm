# -*- coding: utf-8 -*-
# Copyright (C) 2018-2022 Greenbone AG
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

from collections import OrderedDict

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv208 import HostsOrdering


class GmpCreateAuditTestMixin:
    def test_create_audit(self):
        self.gmp.create_audit(
            name="foo", policy_id="c1", target_id="t1", scanner_id="s1"
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            "</create_task>"
        )

    def test_create_audit_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_audit(
                name=None, policy_id="c1", target_id="t1", scanner_id="s1"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_audit(
                name="", policy_id="c1", target_id="t1", scanner_id="s1"
            )

    def test_create_audit_missing_policy_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_audit(
                name="foo", policy_id=None, target_id="t1", scanner_id="s1"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_audit(
                name="foo", policy_id="", target_id="t1", scanner_id="s1"
            )

    def test_create_audit_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_audit(
                name="foo", policy_id="c1", target_id=None, scanner_id="s1"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_audit(
                name="foo", policy_id="c1", target_id="", scanner_id="s1"
            )

    def test_create_audit_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_audit(
                name="foo", policy_id="c1", target_id="t1", scanner_id=None
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_audit(
                name="foo", policy_id="c1", target_id="t1", scanner_id=""
            )

    def test_create_audit_with_comment(self):
        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            comment="bar",
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            "<comment>bar</comment>"
            "</create_task>"
        )

    def test_create_audit_single_alert(self):
        # pylint: disable=invalid-name
        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            alert_ids=["a1"],
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<alert id="a1"/>'
            "</create_task>"
        )

    def test_create_audit_multiple_alerts(self):
        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            alert_ids=["a1", "a2", "a3"],
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<alert id="a1"/>'
            '<alert id="a2"/>'
            '<alert id="a3"/>'
            "</create_task>"
        )

    def test_create_audit_invalid_alerts(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_audit(
                name="foo",
                policy_id="c1",
                target_id="t1",
                scanner_id="s1",
                alert_ids="invalid",
            )

    def test_create_audit_with_empty_alert_ids(self):
        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            alert_ids=[],
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            "</create_task>"
        )

    def test_create_audit_with_alterable(self):
        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            alterable=True,
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            "<alterable>1</alterable>"
            "</create_task>"
        )

        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            alterable=False,
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            "<alterable>0</alterable>"
            "</create_task>"
        )

    def test_create_audit_with_hosts_ordering(self):
        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            hosts_ordering=HostsOrdering.REVERSE,
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            "<hosts_ordering>reverse</hosts_ordering>"
            "</create_task>"
        )

    def test_create_audit_invalid_hosts_ordering(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_audit(
                name="foo",
                policy_id="c1",
                target_id="t1",
                scanner_id="s1",
                hosts_ordering="foo",
            )

    def test_create_audit_with_schedule(self):
        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            schedule_id="s1",
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<schedule id="s1"/>'
            "</create_task>"
        )

    def test_create_audit_with_schedule_and_schedule_periods(self):
        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            schedule_id="s1",
            schedule_periods=0,
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<schedule id="s1"/>'
            "<schedule_periods>0</schedule_periods>"
            "</create_task>"
        )

        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            schedule_id="s1",
            schedule_periods=5,
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            '<schedule id="s1"/>'
            "<schedule_periods>5</schedule_periods>"
            "</create_task>"
        )

    def test_create_audit_with_schedule_and_invalid_schedule_periods(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_audit(
                name="foo",
                policy_id="c1",
                target_id="t1",
                scanner_id="s1",
                schedule_id="s1",
                schedule_periods="foo",
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_audit(
                name="foo",
                policy_id="c1",
                target_id="t1",
                scanner_id="s1",
                schedule_id="s1",
                schedule_periods=-1,
            )

    def test_create_audit_with_observers(self):
        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            observers=["u1", "u2"],
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            "<observers>u1,u2</observers>"
            "</create_task>"
        )

    def test_create_audit_invalid_observers(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_audit(
                name="foo",
                policy_id="c1",
                target_id="t1",
                scanner_id="s1",
                observers="",
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_audit(
                name="foo",
                policy_id="c1",
                target_id="t1",
                scanner_id="s1",
                observers="foo",
            )

    def test_create_audit_with_preferences(self):
        self.gmp.create_audit(
            name="foo",
            policy_id="c1",
            target_id="t1",
            scanner_id="s1",
            preferences=OrderedDict([("foo", "bar"), ("lorem", "ipsum")]),
        )

        self.connection.send.has_been_called_with(
            "<create_task>"
            "<name>foo</name>"
            "<usage_type>audit</usage_type>"
            '<config id="c1"/>'
            '<target id="t1"/>'
            '<scanner id="s1"/>'
            "<preferences>"
            "<preference>"
            "<scanner_name>foo</scanner_name>"
            "<value>bar</value>"
            "</preference>"
            "<preference>"
            "<scanner_name>lorem</scanner_name>"
            "<value>ipsum</value>"
            "</preference>"
            "</preferences>"
            "</create_task>"
        )

    def test_create_audit_invalid_preferences(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_audit(
                name="foo",
                policy_id="c1",
                target_id="t1",
                scanner_id="s1",
                preferences="",
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_audit(
                name="foo",
                policy_id="c1",
                target_id="t1",
                scanner_id="s1",
                preferences=["foo", "bar"],
            )

    def test_create_audit_don_t_allow_container_task(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_audit(
                name="foo",
                policy_id="c1",
                target_id="0",
                scanner_id="s1",
                observers="",
            )

        # target_id=0 is considered as False
        with self.assertRaises(RequiredArgument):
            self.gmp.create_audit(
                name="foo",
                policy_id="c1",
                target_id=0,
                scanner_id="s1",
                observers="",
            )
