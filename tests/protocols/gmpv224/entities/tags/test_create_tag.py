# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import EntityType


class GmpCreateTagTestMixin:
    def test_create_tag_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name=None, resource_ids=["foo"], resource_type=EntityType.TASK
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name="", resource_ids=["foo"], resource_type=EntityType.TASK
            )

    def test_create_tag_missing_resource_filter_and_ids(self):
        self.gmp.create_tag(
            name="foo",
            resource_filter=None,
            resource_ids=None,
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b"<resources>"
            b"<type>task</type>"
            b"</resources>"
            b"</create_tag>"
        )

        self.gmp.create_tag(
            name="foo",
            resource_filter=None,
            resource_ids=[],
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b"<resources>"
            b"<type>task</type>"
            b"</resources>"
            b"</create_tag>"
        )

        self.gmp.create_tag(name="foo", resource_type=EntityType.TASK)

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b"<resources>"
            b"<type>task</type>"
            b"</resources>"
            b"</create_tag>"
        )

    def test_create_tag_both_resource_filter_and_ids(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_tag(
                name="foo",
                resource_filter="name=foo",
                resource_ids=["foo"],
                resource_type=EntityType.TASK,
            )

    def test_create_tag_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_tag(
                name="foo",
                resource_type="Foo",
                resource_filter=None,
                resource_ids=["foo"],
            )

    def test_create_tag_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name="foo",
                resource_type=None,
                resource_filter=None,
                resource_ids=["foo"],
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name="foo",
                resource_type=None,
                resource_filter="name=foo",
                resource_ids=None,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name="foo", resource_type="", resource_ids=["foo"]
            )

    def test_create_tag_with_resource_filter(self):
        self.gmp.create_tag(
            name="foo",
            resource_filter="name=foo",
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b'<resources filter="name=foo">'
            b"<type>task</type>"
            b"</resources>"
            b"</create_tag>"
        )

    def test_create_tag_with_resource_filter_audit(self):
        self.gmp.create_tag(
            name="foo",
            resource_filter="name=foo",
            resource_type=EntityType.AUDIT,
        )

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b'<resources filter="name=foo">'
            b"<type>task</type>"
            b"</resources>"
            b"</create_tag>"
        )

    def test_create_tag_with_resource_filter_policy(self):
        self.gmp.create_tag(
            name="foo",
            resource_filter="name=foo",
            resource_type=EntityType.POLICY,
        )

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b'<resources filter="name=foo">'
            b"<type>config</type>"
            b"</resources>"
            b"</create_tag>"
        )

    def test_create_tag_with_resource_ids(self):
        self.gmp.create_tag(
            name="foo", resource_ids=["foo"], resource_type=EntityType.TASK
        )

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b"<resources>"
            b'<resource id="foo"/>'
            b"<type>task</type>"
            b"</resources>"
            b"</create_tag>"
        )

        self.gmp.create_tag(
            name="foo",
            resource_ids=["foo", "bar"],
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b"<resources>"
            b'<resource id="foo"/>'
            b'<resource id="bar"/>'
            b"<type>task</type>"
            b"</resources>"
            b"</create_tag>"
        )

    def test_create_tag_with_comment(self):
        self.gmp.create_tag(
            name="foo",
            resource_ids=["foo"],
            resource_type=EntityType.TASK,
            comment="bar",
        )

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b"<resources>"
            b'<resource id="foo"/>'
            b"<type>task</type>"
            b"</resources>"
            b"<comment>bar</comment>"
            b"</create_tag>"
        )

    def test_create_tag_with_value(self):
        self.gmp.create_tag(
            name="foo",
            resource_ids=["foo"],
            resource_type=EntityType.TASK,
            value="bar",
        )

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b"<resources>"
            b'<resource id="foo"/>'
            b"<type>task</type>"
            b"</resources>"
            b"<value>bar</value>"
            b"</create_tag>"
        )

    def test_create_tag_with_active(self):
        self.gmp.create_tag(
            name="foo",
            resource_ids=["foo"],
            resource_type=EntityType.TASK,
            active=True,
        )

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b"<resources>"
            b'<resource id="foo"/>'
            b"<type>task</type>"
            b"</resources>"
            b"<active>1</active>"
            b"</create_tag>"
        )

        self.gmp.create_tag(
            name="foo",
            resource_ids=["foo"],
            resource_type=EntityType.TASK,
            active=False,
        )

        self.connection.send.has_been_called_with(
            b"<create_tag>"
            b"<name>foo</name>"
            b"<resources>"
            b'<resource id="foo"/>'
            b"<type>task</type>"
            b"</resources>"
            b"<active>0</active>"
            b"</create_tag>"
        )
