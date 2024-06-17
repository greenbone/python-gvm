# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import HostsOrdering, Tasks


class TasksTestCase(unittest.TestCase):
    def test_clone_task(self):
        request = Tasks().clone_task("task_id")
        self.assertEqual(
            bytes(request),
            b"<create_task><copy>task_id</copy></create_task>",
        )

    def test_clone_task_invalid(self):
        with self.assertRaises(RequiredArgument):
            Tasks().clone_task(None)

        with self.assertRaises(RequiredArgument):
            Tasks().clone_task("")

    def test_create_container_task(self):
        request = Tasks().create_container_task("name")
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b'<target id="0"/>'
            b"</create_task>",
        )

    def test_create_container_task_with_comment(self):
        request = Tasks().create_container_task("name", comment="comment")
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b'<target id="0"/>'
            b"<comment>comment</comment>"
            b"</create_task>",
        )

    def test_create_task(self):
        request = Tasks().create_task(
            "name",
            target_id="target_id",
            config_id="config_id",
            scanner_id="scanner_id",
        )
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="config_id"/>'
            b'<target id="target_id"/>'
            b'<scanner id="scanner_id"/>'
            b"</create_task>",
        )

    def test_create_task_with_comment(self):
        request = Tasks().create_task(
            "name",
            target_id="target_id",
            config_id="config_id",
            scanner_id="scanner_id",
            comment="comment",
        )
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="config_id"/>'
            b'<target id="target_id"/>'
            b'<scanner id="scanner_id"/>'
            b"<comment>comment</comment>"
            b"</create_task>",
        )

    def test_create_task_with_alterable(self):
        request = Tasks().create_task(
            "name",
            target_id="target_id",
            config_id="config_id",
            scanner_id="scanner_id",
            alterable=True,
        )
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="config_id"/>'
            b'<target id="target_id"/>'
            b'<scanner id="scanner_id"/>'
            b"<alterable>1</alterable>"
            b"</create_task>",
        )

        request = Tasks().create_task(
            "name",
            target_id="target_id",
            config_id="config_id",
            scanner_id="scanner_id",
            alterable=False,
        )
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="config_id"/>'
            b'<target id="target_id"/>'
            b'<scanner id="scanner_id"/>'
            b"<alterable>0</alterable>"
            b"</create_task>",
        )

    def test_create_task_with_hosts_ordering(self):
        request = Tasks().create_task(
            "name",
            target_id="target_id",
            config_id="config_id",
            scanner_id="scanner_id",
            hosts_ordering="random",
        )
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="config_id"/>'
            b'<target id="target_id"/>'
            b'<scanner id="scanner_id"/>'
            b"<hosts_ordering>random</hosts_ordering>"
            b"</create_task>",
        )

        request = Tasks().create_task(
            "name",
            target_id="target_id",
            config_id="config_id",
            scanner_id="scanner_id",
            hosts_ordering=HostsOrdering.RANDOM,
        )
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="config_id"/>'
            b'<target id="target_id"/>'
            b'<scanner id="scanner_id"/>'
            b"<hosts_ordering>random</hosts_ordering>"
            b"</create_task>",
        )

    def test_create_task_with_alert_ids(self):
        request = Tasks().create_task(
            "name",
            target_id="target_id",
            config_id="config_id",
            scanner_id="scanner_id",
            alert_ids=["alert_id1", "alert_id2"],
        )
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="config_id"/>'
            b'<target id="target_id"/>'
            b'<scanner id="scanner_id"/>'
            b'<alert id="alert_id1"/>'
            b'<alert id="alert_id2"/>'
            b"</create_task>",
        )

    def test_create_task_with_schedule_id(self):
        request = Tasks().create_task(
            "name",
            target_id="target_id",
            config_id="config_id",
            scanner_id="scanner_id",
            schedule_id="schedule_id",
        )
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="config_id"/>'
            b'<target id="target_id"/>'
            b'<scanner id="scanner_id"/>'
            b'<schedule id="schedule_id"/>'
            b"</create_task>",
        )

    def test_create_task_with_scanner_id_and_schedule_periods(self):
        request = Tasks().create_task(
            "name",
            target_id="target_id",
            config_id="config_id",
            scanner_id="scanner_id",
            schedule_id="schedule_id",
            schedule_periods=5,
        )
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="config_id"/>'
            b'<target id="target_id"/>'
            b'<scanner id="scanner_id"/>'
            b'<schedule id="schedule_id"/>'
            b"<schedule_periods>5</schedule_periods>"
            b"</create_task>",
        )

    def test_create_task_with_scanner_id_and_invalid_schedule_periods(self):
        with self.assertRaises(InvalidArgument):
            Tasks().create_task(
                "name",
                target_id="target_id",
                config_id="config_id",
                scanner_id="scanner_id",
                schedule_id="schedule_id",
                schedule_periods=-1,
            )
        with self.assertRaises(InvalidArgument):
            Tasks().create_task(
                "name",
                target_id="target_id",
                config_id="config_id",
                scanner_id="scanner_id",
                schedule_id="schedule_id",
                schedule_periods="invalid",
            )

    def test_create_task_with_observers(self):
        request = Tasks().create_task(
            "name",
            target_id="target_id",
            config_id="config_id",
            scanner_id="scanner_id",
            observers=["observer_id1", "observer_id2"],
        )
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="config_id"/>'
            b'<target id="target_id"/>'
            b'<scanner id="scanner_id"/>'
            b"<observers>observer_id1,observer_id2</observers>"
            b"</create_task>",
        )

    def test_create_task_with_preferences(self):
        request = Tasks().create_task(
            "name",
            target_id="target_id",
            config_id="config_id",
            scanner_id="scanner_id",
            preferences={"key1": "value1", "key2": "value2"},
        )
        self.assertEqual(
            bytes(request),
            b"<create_task>"
            b"<name>name</name>"
            b"<usage_type>scan</usage_type>"
            b'<config id="config_id"/>'
            b'<target id="target_id"/>'
            b'<scanner id="scanner_id"/>'
            b"<preferences>"
            b"<preference>"
            b"<scanner_name>key1</scanner_name>"
            b"<value>value1</value>"
            b"</preference>"
            b"<preference>"
            b"<scanner_name>key2</scanner_name>"
            b"<value>value2</value>"
            b"</preference>"
            b"</preferences>"
            b"</create_task>",
        )

    def test_create_task_invalid_hosts_ordering(self):
        with self.assertRaises(InvalidArgument):
            Tasks().create_task(
                "name",
                target_id="target_id",
                config_id="config_id",
                scanner_id="scanner_id",
                hosts_ordering="invalid",
            )

    def test_create_task_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Tasks().create_task(
                "",
                target_id="target_id",
                config_id="config_id",
                scanner_id="scanner_id",
            )
        with self.assertRaises(RequiredArgument):
            Tasks().create_task(
                None,
                target_id="target_id",
                config_id="config_id",
                scanner_id="scanner_id",
            )

    def test_create_task_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            Tasks().create_task(
                "name",
                target_id="",
                config_id="config_id",
                scanner_id="scanner_id",
            )
        with self.assertRaises(RequiredArgument):
            Tasks().create_task(
                "name",
                target_id=None,
                config_id="config_id",
                scanner_id="scanner_id",
            )

    def test_create_task_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            Tasks().create_task(
                "name",
                target_id="target_id",
                config_id="",
                scanner_id="scanner_id",
            )
        with self.assertRaises(RequiredArgument):
            Tasks().create_task(
                "name",
                target_id="target_id",
                config_id=None,
                scanner_id="scanner_id",
            )

    def test_create_task_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            Tasks().create_task(
                "name",
                target_id="target_id",
                config_id="config_id",
                scanner_id="",
            )
        with self.assertRaises(RequiredArgument):
            Tasks().create_task(
                "name",
                target_id="target_id",
                config_id="config_id",
                scanner_id=None,
            )

    def test_delete_task(self):
        request = Tasks().delete_task("task_id")
        self.assertEqual(
            bytes(request),
            b'<delete_task task_id="task_id" ultimate="0"/>',
        )

    def test_delete_task_with_ultimate(self):
        request = Tasks().delete_task("task_id", ultimate=True)
        self.assertEqual(
            bytes(request),
            b'<delete_task task_id="task_id" ultimate="1"/>',
        )

        request = Tasks().delete_task("task_id", ultimate=False)
        self.assertEqual(
            bytes(request),
            b'<delete_task task_id="task_id" ultimate="0"/>',
        )

    def test_delete_task_missing_task_id(self):
        with self.assertRaises(RequiredArgument):
            Tasks().delete_task("")

        with self.assertRaises(RequiredArgument):
            Tasks().delete_task(None)

    def test_get_tasks(self):
        request = Tasks().get_tasks()
        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="scan"/>',
        )

    def test_get_tasks_with_filter_string(self):
        request = Tasks().get_tasks(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="scan" filter="filter_string"/>',
        )

    def test_get_tasks_with_filter_id(self):
        request = Tasks().get_tasks(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="scan" filt_id="filter_id"/>',
        )

    def test_get_tasks_with_trash(self):
        request = Tasks().get_tasks(trash=True)
        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="scan" trash="1"/>',
        )

        request = Tasks().get_tasks(trash=False)
        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="scan" trash="0"/>',
        )

    def test_get_tasks_with_details(self):
        request = Tasks().get_tasks(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="scan" details="1"/>',
        )

        request = Tasks().get_tasks(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="scan" details="0"/>',
        )

    def test_get_tasks_with_schedules_only(self):
        request = Tasks().get_tasks(schedules_only=True)
        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="scan" schedules_only="1"/>',
        )

        request = Tasks().get_tasks(schedules_only=False)
        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="scan" schedules_only="0"/>',
        )

    def test_get_tasks_with_ignore_pagination(self):
        request = Tasks().get_tasks(ignore_pagination=True)
        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="scan" ignore_pagination="1"/>',
        )

        request = Tasks().get_tasks(ignore_pagination=False)
        self.assertEqual(
            bytes(request),
            b'<get_tasks usage_type="scan" ignore_pagination="0"/>',
        )

    def test_get_task(self):
        request = Tasks().get_task("task_id")
        self.assertEqual(
            bytes(request),
            b'<get_tasks task_id="task_id" usage_type="scan" details="1"/>',
        )

    def test_get_task_missing_task_id(self):
        with self.assertRaises(RequiredArgument):
            Tasks().get_task("")

        with self.assertRaises(RequiredArgument):
            Tasks().get_task(None)

    def test_modify_task(self):
        request = Tasks().modify_task("task_id")
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id"/>',
        )

    def test_modify_task_with_name(self):
        request = Tasks().modify_task("task_id", name="name")
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b"<name>name</name>"
            b"</modify_task>",
        )

    def test_modify_task_with_config_id(self):
        request = Tasks().modify_task("task_id", config_id="config_id")
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b'<config id="config_id"/>'
            b"</modify_task>",
        )

    def test_modify_task_with_comment(self):
        request = Tasks().modify_task("task_id", comment="comment")
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b"<comment>comment</comment>"
            b"</modify_task>",
        )

    def test_modify_task_with_target_id(self):
        request = Tasks().modify_task("task_id", target_id="target_id")
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b'<target id="target_id"/>'
            b"</modify_task>",
        )

    def test_modify_task_with_alterable(self):
        request = Tasks().modify_task("task_id", alterable=True)
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b"<alterable>1</alterable>"
            b"</modify_task>",
        )

        request = Tasks().modify_task("task_id", alterable=False)
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b"<alterable>0</alterable>"
            b"</modify_task>",
        )

    def test_modify_task_with_hosts_ordering(self):
        request = Tasks().modify_task("task_id", hosts_ordering="random")
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b"<hosts_ordering>random</hosts_ordering>"
            b"</modify_task>",
        )

        request = Tasks().modify_task(
            "task_id", hosts_ordering=HostsOrdering.RANDOM
        )
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b"<hosts_ordering>random</hosts_ordering>"
            b"</modify_task>",
        )

    def test_modify_task_with_scanner_id(self):
        request = Tasks().modify_task("task_id", scanner_id="scanner_id")
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b'<scanner id="scanner_id"/>'
            b"</modify_task>",
        )

    def test_modify_task_with_schedule_id(self):
        request = Tasks().modify_task("task_id", schedule_id="schedule_id")
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b'<schedule id="schedule_id"/>'
            b"</modify_task>",
        )

    def test_modify_task_with_schedule_periods(self):
        request = Tasks().modify_task("task_id", schedule_periods=5)
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b"<schedule_periods>5</schedule_periods>"
            b"</modify_task>",
        )

    def test_modify_task_with_alert_ids(self):
        request = Tasks().modify_task(
            "task_id", alert_ids=["alert_id1", "alert_id2"]
        )
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b'<alert id="alert_id1"/>'
            b'<alert id="alert_id2"/>'
            b"</modify_task>",
        )

        request = Tasks().modify_task("task_id", alert_ids=[])
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b'<alert id="0"/>'
            b"</modify_task>",
        )

    def test_modify_task_with_observers(self):
        request = Tasks().modify_task(
            "task_id", observers=["observer_id1", "observer_id2"]
        )
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b"<observers>observer_id1,observer_id2</observers>"
            b"</modify_task>",
        )
        request = Tasks().modify_task("task_id", observers=[])
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b"<observers></observers>"
            b"</modify_task>",
        )

    def test_modify_task_with_preferences(self):
        request = Tasks().modify_task(
            "task_id", preferences={"key1": "value1", "key2": "value2"}
        )
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b"<preferences>"
            b"<preference>"
            b"<scanner_name>key1</scanner_name>"
            b"<value>value1</value>"
            b"</preference>"
            b"<preference>"
            b"<scanner_name>key2</scanner_name>"
            b"<value>value2</value>"
            b"</preference>"
            b"</preferences>"
            b"</modify_task>",
        )

        request = Tasks().modify_task("task_id", preferences={})
        self.assertEqual(
            bytes(request),
            b'<modify_task task_id="task_id">'
            b"<preferences/>"
            b"</modify_task>",
        )

    def test_modify_task_missing_task_id(self):
        with self.assertRaises(RequiredArgument):
            Tasks().modify_task("")

        with self.assertRaises(RequiredArgument):
            Tasks().modify_task(None)

    def test_modify_task_invalid_schedule_periods(self):
        with self.assertRaises(InvalidArgument):
            Tasks().modify_task("task_id", schedule_periods=-1)
        with self.assertRaises(InvalidArgument):
            Tasks().modify_task("task_id", schedule_periods="invalid")

    def test_modify_task_invalid_hosts_ordering(self):
        with self.assertRaises(InvalidArgument):
            Tasks().modify_task("task_id", hosts_ordering="invalid")

    def test_move_task(self):
        request = Tasks().move_task("task_id")
        self.assertEqual(
            bytes(request),
            b'<move_task task_id="task_id"/>',
        )

    def test_move_task_with_slave_id(self):
        request = Tasks().move_task("task_id", slave_id="slave_id")
        self.assertEqual(
            bytes(request),
            b'<move_task task_id="task_id" slave_id="slave_id"/>',
        )

    def test_move_task_missing_task_id(self):
        with self.assertRaises(RequiredArgument):
            Tasks().move_task("")

        with self.assertRaises(RequiredArgument):
            Tasks().move_task(None)

    def test_start_task(self):
        request = Tasks().start_task("task_id")
        self.assertEqual(
            bytes(request),
            b'<start_task task_id="task_id"/>',
        )

    def test_start_task_missing_task_id(self):
        with self.assertRaises(RequiredArgument):
            Tasks().start_task("")

        with self.assertRaises(RequiredArgument):
            Tasks().start_task(None)

    def test_resume_task(self):
        request = Tasks().resume_task("task_id")
        self.assertEqual(
            bytes(request),
            b'<resume_task task_id="task_id"/>',
        )

    def test_resume_task_missing_task_id(self):
        with self.assertRaises(RequiredArgument):
            Tasks().resume_task("")

        with self.assertRaises(RequiredArgument):
            Tasks().resume_task(None)

    def test_stop_task(self):
        request = Tasks().stop_task("task_id")
        self.assertEqual(
            bytes(request),
            b'<stop_task task_id="task_id"/>',
        )

    def test_stop_task_missing_task_id(self):
        with self.assertRaises(RequiredArgument):
            Tasks().stop_task("")

        with self.assertRaises(RequiredArgument):
            Tasks().stop_task(None)
