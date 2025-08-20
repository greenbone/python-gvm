# SPDX-FileCopyrightText: 2018-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from collections import OrderedDict

from gvm.errors import InvalidArgument, RequiredArgument


class GmpCreateContainerImageTaskTestMixin:
    def test_create_container_image_task(self):
        self.gmp.create_container_image_task(
            name="foo", oci_image_target_id="it1", scanner_id="s1"
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<oci_image_target id="it1"/>'
            b'<scanner id="s1"/>'
            b"</create_task>"
        )

    def test_create_container_image_task_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_image_task(
                name=None, oci_image_target_id="it1", scanner_id="s1"
            )
        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_image_task(
                name="", oci_image_target_id="it1", scanner_id="s1"
            )

    def test_create_container_image_task_missing_oci_image_target_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_image_task(
                name="foo", oci_image_target_id=None, scanner_id="s1"
            )
        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_image_task(
                name="foo", oci_image_target_id="", scanner_id="s1"
            )

    def test_create_container_image_task_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_image_task(
                name="foo", oci_image_target_id="it1", scanner_id=None
            )
        with self.assertRaises(RequiredArgument):
            self.gmp.create_container_image_task(
                name="foo", oci_image_target_id="it1", scanner_id=""
            )

    def test_create_container_image_task_with_comment(self):
        self.gmp.create_container_image_task(
            name="foo",
            oci_image_target_id="it1",
            scanner_id="s1",
            comment="my comment",
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<oci_image_target id="it1"/>'
            b'<scanner id="s1"/>'
            b"<comment>my comment</comment>"
            b"</create_task>"
        )

    def test_create_container_image_task_with_alerts(self):
        self.gmp.create_container_image_task(
            name="foo",
            oci_image_target_id="it1",
            scanner_id="s1",
            alert_ids=["a1", "a2"],
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<oci_image_target id="it1"/>'
            b'<scanner id="s1"/>'
            b'<alert id="a1"/>'
            b'<alert id="a2"/>'
            b"</create_task>"
        )

    def test_create_container_image_task_with_empty_alerts(self):
        self.gmp.create_container_image_task(
            name="foo", oci_image_target_id="it1", scanner_id="s1", alert_ids=[]
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<oci_image_target id="it1"/>'
            b'<scanner id="s1"/>'
            b"</create_task>"
        )

    def test_create_container_image_task_with_schedule(self):
        self.gmp.create_container_image_task(
            name="foo",
            oci_image_target_id="it1",
            scanner_id="s1",
            schedule_id="s1",
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<oci_image_target id="it1"/>'
            b'<scanner id="s1"/>'
            b'<schedule id="s1"/>'
            b"</create_task>"
        )

    def test_create_create_container_image_task_with_schedule_periods(self):
        self.gmp.create_container_image_task(
            name="foo",
            oci_image_target_id="it1",
            scanner_id="s1",
            schedule_id="s1",
            schedule_periods=5,
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<oci_image_target id="it1"/>'
            b'<scanner id="s1"/>'
            b'<schedule id="s1"/>'
            b"<schedule_periods>5</schedule_periods>"
            b"</create_task>"
        )

    def test_create_container_image_task_with_invalid_schedule_periods(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_container_image_task(
                name="foo",
                oci_image_target_id="it1",
                scanner_id="s1",
                schedule_id="s1",
                schedule_periods="invalid",
            )

        with self.assertRaises(InvalidArgument):
            self.gmp.create_container_image_task(
                name="foo",
                oci_image_target_id="it1",
                scanner_id="s1",
                schedule_id="s1",
                schedule_periods=-1,
            )

    def test_create_container_image_task_with_alterable(self):
        self.gmp.create_container_image_task(
            name="foo",
            oci_image_target_id="it1",
            scanner_id="s1",
            alterable=True,
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<oci_image_target id="it1"/>'
            b'<scanner id="s1"/>'
            b"<alterable>1</alterable>"
            b"</create_task>"
        )

    def test_create__container_image_task_with_observers(self):
        self.gmp.create_container_image_task(
            name="foo",
            oci_image_target_id="it1",
            scanner_id="s1",
            observers=["u1", "u2"],
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<oci_image_target id="it1"/>'
            b'<scanner id="s1"/>'
            b"<observers>u1,u2</observers>"
            b"</create_task>"
        )

    def test_create_container_image_task_with_preferences(self):
        self.gmp.create_container_image_task(
            name="foo",
            oci_image_target_id="it1",
            scanner_id="s1",
            preferences=OrderedDict([("pref1", "val1"), ("pref2", "val2")]),
        )

        self.connection.send.has_been_called_with(
            b"<create_task>"
            b"<name>foo</name>"
            b"<usage_type>scan</usage_type>"
            b'<oci_image_target id="it1"/>'
            b'<scanner id="s1"/>'
            b"<preferences>"
            b"<preference><scanner_name>pref1</scanner_name><value>val1</value></preference>"
            b"<preference><scanner_name>pref2</scanner_name><value>val2</value></preference>"
            b"</preferences>"
            b"</create_task>"
        )
