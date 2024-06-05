# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from collections import OrderedDict

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import HostsOrdering


class GmpCreateTaskTestMixin:
    def test_create_task(self):
        self.gmp.create_task(
            name="foo", config_id="c1", target_id="t1", scanner_id="s1"
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"</create_task>"
        )

    def test_create_task_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name=None, config_id="c1", target_id="t1", scanner_id="s1"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name="", config_id="c1", target_id="t1", scanner_id="s1"
            )

    def test_create_task_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name="foo", config_id=None, target_id="t1", scanner_id="s1"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name="foo", config_id="", target_id="t1", scanner_id="s1"
            )

    def test_create_task_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name="foo", config_id="c1", target_id=None, scanner_id="s1"
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name="foo", config_id="c1", target_id="", scanner_id="s1"
            )

    def test_create_task_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name="foo", config_id="c1", target_id="t1", scanner_id=None
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name="foo", config_id="c1", target_id="t1", scanner_id=""
            )

    def test_create_task_with_comment(self):
        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            comment="bar",
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<comment>bar</comment>"
            b"</create_task>"
        )

    def test_create_task_single_alert(self):
        # pylint: disable=invalid-name
        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            alert_ids=["a1"],
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b'<alert id="a1"/>'
            b"</create_task>"
        )

    def test_create_task_multiple_alerts(self):
        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            alert_ids=["a1", "a2", "a3"],
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b'<alert id="a1"/>'
            b'<alert id="a2"/>'
            b'<alert id="a3"/>'
            b"</create_task>"
        )

    def test_create_task_with_empty_alert_ids(self):
        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            alert_ids=[],
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"</create_task>"
        )

    def test_create_task_with_alterable(self):
        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            alterable=True,
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<alterable>1</alterable>"
            b"</create_task>"
        )

        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            alterable=False,
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<alterable>0</alterable>"
            b"</create_task>"
        )

    def test_create_task_with_hosts_ordering(self):
        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            hosts_ordering=HostsOrdering.REVERSE,
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<hosts_ordering>reverse</hosts_ordering>"
            b"</create_task>"
        )

    def test_create_task_invalid_hosts_ordering(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_task(
                name="foo",
                config_id="c1",
                target_id="t1",
                scanner_id="s1",
                hosts_ordering="foo",
            )

    def test_create_task_with_schedule(self):
        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            schedule_id="s1",
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b'<schedule id="s1"/>'
            b"</create_task>"
        )

    def test_create_task_with_schedule_and_schedule_periods(self):
        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            schedule_id="s1",
            schedule_periods=0,
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b'<schedule id="s1"/>'
            b"<schedule_periods>0</schedule_periods>"
            b"</create_task>"
        )

        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            schedule_id="s1",
            schedule_periods=5,
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b'<schedule id="s1"/>'
            b"<schedule_periods>5</schedule_periods>"
            b"</create_task>"
        )

    def test_create_task_with_schedule_and_invalid_schedule_periods(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_task(
                name="foo",
                config_id="c1",
                target_id="t1",
                scanner_id="s1",
                schedule_id="s1",
                schedule_periods="foo",
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_task(
                name="foo",
                config_id="c1",
                target_id="t1",
                scanner_id="s1",
                schedule_id="s1",
                schedule_periods=-1,
            )

    def test_create_task_with_observers(self):
        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            observers=["u1", "u2"],
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="c1"/>'
            b'<target id="t1"/>'
            b'<scanner id="s1"/>'
            b"<observers>u1,u2</observers>"
            b"</create_task>"
        )

    def test_create_task_with_preferences(self):
        self.gmp.create_task(
            name="foo",
            config_id="c1",
            target_id="t1",
            scanner_id="s1",
            preferences=OrderedDict([("foo", "bar"), ("lorem", "ipsum")]),
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
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
            b"</create_task>"
        )

    def test_create_task_don_t_allow_container_task(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_task(
                name="foo",
                config_id="c1",
                target_id="0",
                scanner_id="s1",
                observers="",
            )

        # target_id=0 is considered as False
        with self.assertRaises(RequiredArgument):
            self.gmp.create_task(
                name="foo",
                config_id="c1",
                target_id=0,
                scanner_id="s1",
                observers="",
            )
