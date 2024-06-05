# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import EntityType


class GmpModifyTagTestMixin:
    def test_modify_tag(self):
        self.gmp.modify_tag(tag_id="t1")

        self.connection.send.has_been_called_with(b'<modify_tag tag_id="t1"/>')

    def test_modify_tag_missing_tag_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_tag(tag_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_tag(tag_id="")

    def test_modify_tag_with_comment(self):
        self.gmp.modify_tag(tag_id="t1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1"><comment>foo</comment></modify_tag>'
        )

    def test_modify_tag_with_value(self):
        self.gmp.modify_tag(tag_id="t1", value="foo")

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1"><value>foo</value></modify_tag>'
        )

    def test_modify_tag_with_name(self):
        self.gmp.modify_tag(tag_id="t1", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1"><name>foo</name></modify_tag>'
        )

    def test_modify_tag_with_active(self):
        self.gmp.modify_tag(tag_id="t1", active=True)

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1"><active>1</active></modify_tag>'
        )

        self.gmp.modify_tag(tag_id="t1", active=False)

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1"><active>0</active></modify_tag>'
        )

    def test_modify_tag_with_resource_filter_and_type(self):
        self.gmp.modify_tag(
            tag_id="t1",
            resource_filter="name=foo",
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1">'
            b'<resources filter="name=foo">'
            b"<type>task</type>"
            b"</resources>"
            b"</modify_tag>"
        )

    def test_modify_tag_with_resource_filter_and_type_audit(self):
        self.gmp.modify_tag(
            tag_id="t1",
            resource_filter="name=foo",
            resource_type=EntityType.AUDIT,
        )

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1">'
            b'<resources filter="name=foo">'
            b"<type>task</type>"
            b"</resources>"
            b"</modify_tag>"
        )

    def test_modify_tag_with_resource_filter_and_type_policy(self):
        self.gmp.modify_tag(
            tag_id="t1",
            resource_filter="name=foo",
            resource_type=EntityType.POLICY,
        )

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1">'
            b'<resources filter="name=foo">'
            b"<type>config</type>"
            b"</resources>"
            b"</modify_tag>"
        )

    def test_modify_tag_with_resource_action_filter_and_type(self):
        self.gmp.modify_tag(
            tag_id="t1",
            resource_action="set",
            resource_filter="name=foo",
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1">'
            b'<resources action="set" filter="name=foo">'
            b"<type>task</type>"
            b"</resources>"
            b"</modify_tag>"
        )

    def test_modify_tag_with_resource_ids_and_type(self):
        self.gmp.modify_tag(
            tag_id="t1", resource_ids=["r1"], resource_type=EntityType.TASK
        )

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1">'
            b"<resources>"
            b'<resource id="r1"/>'
            b"<type>task</type>"
            b"</resources>"
            b"</modify_tag>"
        )

    def test_modify_tag_with_resource_action_ids_and_type(self):
        self.gmp.modify_tag(
            tag_id="t1",
            resource_action="set",
            resource_ids=["r1"],
            resource_type=EntityType.TASK,
        )

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1">'
            b'<resources action="set">'
            b'<resource id="r1"/>'
            b"<type>task</type>"
            b"</resources>"
            b"</modify_tag>"
        )

    def test_modify_tag_with_missing_resource_filter_or_ids_andtype(self):
        self.gmp.modify_tag(tag_id="t1", resource_action="add")

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1">'
            b'<resources action="add"/>'
            b"</modify_tag>"
        )

    def test_modify_tag_with_missing_resource_type(self):
        self.gmp.modify_tag(tag_id="t1", resource_ids=["r1"])

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1">'
            b"<resources>"
            b'<resource id="r1"/>'
            b"</resources>"
            b"</modify_tag>"
        )

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_tag(tag_id="t1", resource_filter="name=foo")

    def test_modify_tag_with_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_tag(
                tag_id="t1", resource_type="foo", resource_filter="name=foo"
            )

    def test_modify_tag_with_missing_resource_filter_and_ids(self):
        self.gmp.modify_tag(tag_id="t1", resource_type=EntityType.TASK)

        self.connection.send.has_been_called_with(
            b'<modify_tag tag_id="t1">'
            b"<resources>"
            b"<type>task</type>"
            b"</resources>"
            b"</modify_tag>"
        )
