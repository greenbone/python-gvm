# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import PortLists, PortRangeType


class PortListsTestCase(unittest.TestCase):
    def test_clone(self) -> None:
        request = PortLists.clone_port_list("a1")

        self.assertEqual(
            bytes(request),
            b"<create_port_list><copy>a1</copy></create_port_list>",
        )

    def test_clone_missing_id(self):
        with self.assertRaises(RequiredArgument):
            PortLists.clone_port_list("")

        with self.assertRaises(RequiredArgument):
            PortLists.clone_port_list(None)

    def test_create_port_list_missing_name(self):
        with self.assertRaises(RequiredArgument):
            PortLists.create_port_list(name=None, port_range="T:1-1234")

        with self.assertRaises(RequiredArgument):
            PortLists.create_port_list(name="", port_range="T:1-1234")

    def test_create_port_list_missing_port_range(self):
        with self.assertRaises(RequiredArgument):
            PortLists.create_port_list(name="foo", port_range=None)

        with self.assertRaises(RequiredArgument):
            PortLists.create_port_list(name="foo", port_range="")

    def test_create_port_list(self):
        request = PortLists.create_port_list(name="foo", port_range="T:1-1234")

        self.assertEqual(
            bytes(request),
            b"<create_port_list>"
            b"<name>foo</name>"
            b"<port_range>T:1-1234</port_range>"
            b"</create_port_list>",
        )

    def test_create_port_list_with_comment(self):
        request = PortLists.create_port_list(
            name="foo", port_range="T:1-1234", comment="lorem"
        )

        self.assertEqual(
            bytes(request),
            b"<create_port_list>"
            b"<name>foo</name>"
            b"<port_range>T:1-1234</port_range>"
            b"<comment>lorem</comment>"
            b"</create_port_list>",
        )

    def test_create_port_range_missing_port_list_id(self):
        with self.assertRaises(RequiredArgument):
            PortLists.create_port_range(
                port_list_id=None,
                start=1,
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

        with self.assertRaises(RequiredArgument):
            PortLists.create_port_range(
                port_list_id="",
                start=1,
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

    def test_create_port_range_missing_start(self):
        with self.assertRaises(RequiredArgument):
            PortLists.create_port_range(
                port_list_id="pl1",
                start=None,
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

        with self.assertRaises(RequiredArgument):
            PortLists.create_port_range(
                port_list_id="pl1",
                start="",
                end=1234,
                port_range_type=PortRangeType.TCP,
            )

    def test_create_port_range_missing_end(self):
        with self.assertRaises(RequiredArgument):
            PortLists.create_port_range(
                port_list_id="pl1",
                start=1,
                end=None,
                port_range_type=PortRangeType.TCP,
            )

        with self.assertRaises(RequiredArgument):
            PortLists.create_port_range(
                port_list_id="pl1",
                start=1,
                end="",
                port_range_type=PortRangeType.TCP,
            )

    def test_create_port_range_missing_port_range_type(self):
        with self.assertRaises(RequiredArgument):
            PortLists.create_port_range(
                port_list_id="pl1", start=1, end=1234, port_range_type=None
            )

        with self.assertRaises(RequiredArgument):
            PortLists.create_port_range(
                port_list_id="pl1", start=1, end=1234, port_range_type=""
            )

    def test_create_port_range_invalid_port_range_type(self):
        with self.assertRaises(InvalidArgument):
            PortLists.create_port_range(
                port_list_id="pl1", start=1, end=1234, port_range_type="blubb"
            )

    def test_create_port_range(self):
        request = PortLists.create_port_range(
            port_list_id="pl1",
            start=1,
            end=1234,
            port_range_type=PortRangeType.TCP,
        )

        self.assertEqual(
            bytes(request),
            b"<create_port_range>"
            b'<port_list id="pl1"/>'
            b"<start>1</start>"
            b"<end>1234</end>"
            b"<type>TCP</type>"
            b"</create_port_range>",
        )

        request = PortLists.create_port_range(
            port_list_id="pl1",
            start=1,
            end=1234,
            port_range_type=PortRangeType.UDP,
        )

        self.assertEqual(
            bytes(request),
            b"<create_port_range>"
            b'<port_list id="pl1"/>'
            b"<start>1</start>"
            b"<end>1234</end>"
            b"<type>UDP</type>"
            b"</create_port_range>",
        )

        request = PortLists.create_port_range(
            port_list_id="pl1",
            start="1",
            end="1234",
            port_range_type=PortRangeType.TCP,
        )

        self.assertEqual(
            bytes(request),
            b"<create_port_range>"
            b'<port_list id="pl1"/>'
            b"<start>1</start>"
            b"<end>1234</end>"
            b"<type>TCP</type>"
            b"</create_port_range>",
        )

    def test_create_port_range_with_comment(self):
        request = PortLists.create_port_range(
            port_list_id="pl1",
            start=1,
            end=1234,
            port_range_type=PortRangeType.TCP,
            comment="lorem",
        )

        self.assertEqual(
            bytes(request),
            b"<create_port_range>"
            b'<port_list id="pl1"/>'
            b"<start>1</start>"
            b"<end>1234</end>"
            b"<type>TCP</type>"
            b"<comment>lorem</comment>"
            b"</create_port_range>",
        )

    def test_delete(self):
        request = PortLists.delete_port_list("a1")

        self.assertEqual(
            bytes(request),
            b'<delete_port_list port_list_id="a1" ultimate="0"/>',
        )

    def test_delete_ultimate(self):
        request = PortLists.delete_port_list("a1", ultimate=True)

        self.assertEqual(
            bytes(request),
            b'<delete_port_list port_list_id="a1" ultimate="1"/>',
        )

    def test_delete_missing_id(self):
        with self.assertRaises(RequiredArgument):
            PortLists.delete_port_list(None)

        with self.assertRaises(RequiredArgument):
            PortLists.delete_port_list("")

    def test_delete_port_range(self):
        request = PortLists.delete_port_range("a1")

        self.assertEqual(
            bytes(request), b'<delete_port_range port_range_id="a1"/>'
        )

    def test_delete_port_range_missing_id(self):
        with self.assertRaises(RequiredArgument):
            PortLists.delete_port_range(None)

        with self.assertRaises(RequiredArgument):
            PortLists.delete_port_range("")

    def test_get_port_lists(self):
        request = PortLists.get_port_lists()

        self.assertEqual(bytes(request), b"<get_port_lists/>")

    def test_get_port_lists_with_filter_string(self):
        request = PortLists.get_port_lists(filter_string="foo=bar")

        self.assertEqual(bytes(request), b'<get_port_lists filter="foo=bar"/>')

    def test_get_port_lists_with_filter_id(self):
        request = PortLists.get_port_lists(filter_id="f1")

        self.assertEqual(bytes(request), b'<get_port_lists filt_id="f1"/>')

    def test_get_port_lists_with_trash(self):
        request = PortLists.get_port_lists(trash=True)

        self.assertEqual(bytes(request), b'<get_port_lists trash="1"/>')

        request = PortLists.get_port_lists(trash=False)

        self.assertEqual(bytes(request), b'<get_port_lists trash="0"/>')

    def test_get_port_lists_with_details(self):
        request = PortLists.get_port_lists(details=True)

        self.assertEqual(bytes(request), b'<get_port_lists details="1"/>')

        request = PortLists.get_port_lists(details=False)

        self.assertEqual(bytes(request), b'<get_port_lists details="0"/>')

    def test_get_port_lists_with_targets(self):
        request = PortLists.get_port_lists(targets=True)

        self.assertEqual(bytes(request), b'<get_port_lists targets="1"/>')

        request = PortLists.get_port_lists(targets=False)

        self.assertEqual(bytes(request), b'<get_port_lists targets="0"/>')

    def test_get_port_list(self):
        request = PortLists.get_port_list(port_list_id="port_list_id")

        self.assertEqual(
            bytes(request),
            b'<get_port_lists port_list_id="port_list_id" details="1"/>',
        )

    def test_get_port_list_missing_port_list_id(self):
        with self.assertRaises(RequiredArgument):
            PortLists.get_port_list(port_list_id=None)

        with self.assertRaises(RequiredArgument):
            PortLists.get_port_list(port_list_id="")

        with self.assertRaises(RequiredArgument):
            PortLists.get_port_list("")

    def test_modify_port_list(self):
        request = PortLists.modify_port_list(port_list_id="p1")

        self.assertEqual(
            bytes(request), b'<modify_port_list port_list_id="p1"/>'
        )

    def test_modify_port_list_missing_port_list_id(self):
        with self.assertRaises(RequiredArgument):
            PortLists.modify_port_list(port_list_id=None)

        with self.assertRaises(RequiredArgument):
            PortLists.modify_port_list(port_list_id="")

        with self.assertRaises(RequiredArgument):
            PortLists.modify_port_list("")

    def test_modify_port_list_with_comment(self):
        request = PortLists.modify_port_list(port_list_id="p1", comment="foo")

        self.assertEqual(
            bytes(request),
            b'<modify_port_list port_list_id="p1">'
            b"<comment>foo</comment>"
            b"</modify_port_list>",
        )

    def test_modify_port_list_with_name(self):
        request = PortLists.modify_port_list(port_list_id="p1", name="foo")

        self.assertEqual(
            bytes(request),
            b'<modify_port_list port_list_id="p1">'
            b"<name>foo</name>"
            b"</modify_port_list>",
        )
