# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import Tags


class TagsTestCase(unittest.TestCase):
    def test_clone_tag(self):
        request = Tags.clone_tag("tag_id")
        self.assertEqual(
            bytes(request),
            b"<create_tag><copy>tag_id</copy></create_tag>",
        )

    def test_clone_tag_missing_tag_id(self):
        with self.assertRaises(RequiredArgument):
            Tags.clone_tag(None)

        with self.assertRaises(RequiredArgument):
            Tags.clone_tag("")

    def test_create_tag(self):
        request = Tags.create_tag("name", "alert")
        self.assertEqual(
            bytes(request),
            b"<create_tag>"
            b"<name>name</name>"
            b"<resources>"
            b"<type>alert</type>"
            b"</resources>"
            b"</create_tag>",
        )

    def test_create_tag_with_resource_filter(self):
        request = Tags.create_tag("name", "alert", resource_filter="filter")
        self.assertEqual(
            bytes(request),
            b"<create_tag>"
            b"<name>name</name>"
            b'<resources filter="filter">'
            b"<type>alert</type>"
            b"</resources>"
            b"</create_tag>",
        )

    def test_create_tag_with_resource_ids(self):
        request = Tags.create_tag("name", "alert", resource_ids=["id1", "id2"])
        self.assertEqual(
            bytes(request),
            b"<create_tag>"
            b"<name>name</name>"
            b"<resources>"
            b'<resource id="id1"/>'
            b'<resource id="id2"/>'
            b"<type>alert</type>"
            b"</resources>"
            b"</create_tag>",
        )

    def test_create_tag_with_value(self):
        request = Tags.create_tag("name", "alert", value="value")
        self.assertEqual(
            bytes(request),
            b"<create_tag>"
            b"<name>name</name>"
            b"<resources>"
            b"<type>alert</type>"
            b"</resources>"
            b"<value>value</value>"
            b"</create_tag>",
        )

    def test_create_tag_with_comment(self):
        request = Tags.create_tag("name", "alert", comment="comment")
        self.assertEqual(
            bytes(request),
            b"<create_tag>"
            b"<name>name</name>"
            b"<resources>"
            b"<type>alert</type>"
            b"</resources>"
            b"<comment>comment</comment>"
            b"</create_tag>",
        )

    def test_create_tag_with_active(self):
        request = Tags.create_tag("name", "alert", active=True)
        self.assertEqual(
            bytes(request),
            b"<create_tag>"
            b"<name>name</name>"
            b"<resources>"
            b"<type>alert</type>"
            b"</resources>"
            b"<active>1</active>"
            b"</create_tag>",
        )

        request = Tags.create_tag("name", "alert", active=False)
        self.assertEqual(
            bytes(request),
            b"<create_tag>"
            b"<name>name</name>"
            b"<resources>"
            b"<type>alert</type>"
            b"</resources>"
            b"<active>0</active>"
            b"</create_tag>",
        )

    def test_create_tag_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Tags.create_tag(None, "alert")

        with self.assertRaises(RequiredArgument):
            Tags.create_tag("", "alert")

    def test_create_tag_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            Tags.create_tag("name", None)

        with self.assertRaises(RequiredArgument):
            Tags.create_tag("name", "")

    def test_create_tag_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            Tags.create_tag("name", "invalid")

    def test_create_tag_invalid_resource_filter_and_resource_ids(self):
        with self.assertRaises(InvalidArgument):
            Tags.create_tag(
                "name",
                "alert",
                resource_filter="filter",
                resource_ids=["id1", "id2"],
            )

    def test_delete_tag(self):
        request = Tags.delete_tag("tag_id")
        self.assertEqual(
            bytes(request),
            b'<delete_tag tag_id="tag_id" ultimate="0"/>',
        )

    def test_delete_tag_with_ultimate(self):
        request = Tags.delete_tag("tag_id", ultimate=True)
        self.assertEqual(
            bytes(request),
            b'<delete_tag tag_id="tag_id" ultimate="1"/>',
        )

        request = Tags.delete_tag("tag_id", ultimate=False)
        self.assertEqual(
            bytes(request),
            b'<delete_tag tag_id="tag_id" ultimate="0"/>',
        )

    def test_get_tags(self):
        request = Tags.get_tags()
        self.assertEqual(
            bytes(request),
            b"<get_tags/>",
        )

    def test_get_tags_with_filter_string(self):
        request = Tags.get_tags(filter_string="filter")
        self.assertEqual(
            bytes(request),
            b'<get_tags filter="filter"/>',
        )

    def test_get_tags_with_filter_id(self):
        request = Tags.get_tags(filter_id="filter")
        self.assertEqual(
            bytes(request),
            b'<get_tags filt_id="filter"/>',
        )

    def test_get_tags_with_trash(self):
        request = Tags.get_tags(trash=True)
        self.assertEqual(
            bytes(request),
            b'<get_tags trash="1"/>',
        )

        request = Tags.get_tags(trash=False)
        self.assertEqual(
            bytes(request),
            b'<get_tags trash="0"/>',
        )

    def test_get_tags_with_names_only(self):
        request = Tags.get_tags(names_only=True)
        self.assertEqual(
            bytes(request),
            b'<get_tags names_only="1"/>',
        )

        request = Tags.get_tags(names_only=False)
        self.assertEqual(
            bytes(request),
            b'<get_tags names_only="0"/>',
        )

    def test_get_tag(self):
        request = Tags.get_tag("tag_id")
        self.assertEqual(
            bytes(request),
            b'<get_tags tag_id="tag_id"/>',
        )

    def test_get_tag_missing_tag_id(self):
        with self.assertRaises(RequiredArgument):
            Tags.get_tag(None)

        with self.assertRaises(RequiredArgument):
            Tags.get_tag("")

    def test_modify_tag(self):
        request = Tags.modify_tag("tag_id", resource_type="alert")
        self.assertEqual(
            bytes(request),
            b'<modify_tag tag_id="tag_id">'
            b"<resources>"
            b"<type>alert</type>"
            b"</resources>"
            b"</modify_tag>",
        )

    def test_modify_tag_with_comment(self):
        request = Tags.modify_tag(
            "tag_id", resource_type="alert", comment="comment"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_tag tag_id="tag_id">'
            b"<comment>comment</comment>"
            b"<resources>"
            b"<type>alert</type>"
            b"</resources>"
            b"</modify_tag>",
        )

    def test_modify_tag_with_name(self):
        request = Tags.modify_tag("tag_id", resource_type="alert", name="name")
        self.assertEqual(
            bytes(request),
            b'<modify_tag tag_id="tag_id">'
            b"<name>name</name>"
            b"<resources>"
            b"<type>alert</type>"
            b"</resources>"
            b"</modify_tag>",
        )

    def test_modify_tag_with_value(self):
        request = Tags.modify_tag(
            "tag_id", resource_type="alert", value="value"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_tag tag_id="tag_id">'
            b"<value>value</value>"
            b"<resources>"
            b"<type>alert</type>"
            b"</resources>"
            b"</modify_tag>",
        )

    def test_modify_tag_with_active(self):
        request = Tags.modify_tag("tag_id", resource_type="alert", active=True)
        self.assertEqual(
            bytes(request),
            b'<modify_tag tag_id="tag_id">'
            b"<active>1</active>"
            b"<resources>"
            b"<type>alert</type>"
            b"</resources>"
            b"</modify_tag>",
        )

        request = Tags.modify_tag("tag_id", resource_type="alert", active=False)
        self.assertEqual(
            bytes(request),
            b'<modify_tag tag_id="tag_id">'
            b"<active>0</active>"
            b"<resources>"
            b"<type>alert</type>"
            b"</resources>"
            b"</modify_tag>",
        )

    def test_modify_tag_with_resource_action(self):
        request = Tags.modify_tag("tag_id", resource_action="add")
        self.assertEqual(
            bytes(request),
            b'<modify_tag tag_id="tag_id">'
            b'<resources action="add"/>'
            b"</modify_tag>",
        )

    def test_modify_tag_with_resource_filter(self):
        request = Tags.modify_tag(
            "tag_id", resource_type="alert", resource_filter="filter"
        )
        self.assertEqual(
            bytes(request),
            b'<modify_tag tag_id="tag_id">'
            b'<resources filter="filter">'
            b"<type>alert</type>"
            b"</resources>"
            b"</modify_tag>",
        )

    def test_modify_tag_with_resource_ids(self):
        request = Tags.modify_tag("tag_id", resource_ids=["id1", "id2"])
        self.assertEqual(
            bytes(request),
            b'<modify_tag tag_id="tag_id">'
            b"<resources>"
            b'<resource id="id1"/>'
            b'<resource id="id2"/>'
            b"</resources>"
            b"</modify_tag>",
        )

    def test_modify_tag_missing_tag_id(self):
        with self.assertRaises(RequiredArgument):
            Tags.modify_tag(None)

        with self.assertRaises(RequiredArgument):
            Tags.modify_tag("")

    def test_modify_tag_with_resource_filter_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            Tags.modify_tag("tag_id", resource_filter="filter")

        with self.assertRaises(RequiredArgument):
            Tags.modify_tag(
                "tag_id", resource_filter="filter", resource_type=None
            )

        with self.assertRaises(RequiredArgument):
            Tags.modify_tag(
                "tag_id", resource_filter="filter", resource_type=""
            )

    def test_modify_tag_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            Tags.modify_tag("tag_id", resource_type="invalid")
