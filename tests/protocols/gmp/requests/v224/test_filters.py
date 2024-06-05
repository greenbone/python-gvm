# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import Filters, FilterType


class FilterTestsCase(unittest.TestCase):
    def test_clone_filter(self):
        request = Filters.clone_filter("filter_id")
        self.assertEqual(
            bytes(request),
            b"<create_filter><copy>filter_id</copy></create_filter>",
        )

    def test_clone_filter_missing_filter_id(self):
        with self.assertRaises(RequiredArgument):
            Filters.clone_filter(None)

        with self.assertRaises(RequiredArgument):
            Filters.clone_filter("")

    def test_create_filter(self):
        request = Filters.create_filter("filter_name")
        self.assertEqual(
            bytes(request),
            b"<create_filter><name>filter_name</name></create_filter>",
        )

    def test_create_filter_with_comment(self):
        request = Filters.create_filter("filter_name", comment="comment")
        self.assertEqual(
            bytes(request),
            b"<create_filter>"
            b"<name>filter_name</name>"
            b"<comment>comment</comment>"
            b"</create_filter>",
        )

    def test_create_filter_with_term(self):
        request = Filters.create_filter("filter_name", term="term")
        self.assertEqual(
            bytes(request),
            b"<create_filter>"
            b"<name>filter_name</name>"
            b"<term>term</term>"
            b"</create_filter>",
        )

    def test_create_filter_with_filter_type(self):
        request = Filters.create_filter(
            "filter_name", filter_type=FilterType.ALERT
        )
        self.assertEqual(
            bytes(request),
            b"<create_filter>"
            b"<name>filter_name</name>"
            b"<type>alert</type>"
            b"</create_filter>",
        )

        request = Filters.create_filter(
            "filter_name",
            filter_type="alert",
        )
        self.assertEqual(
            bytes(request),
            b"<create_filter>"
            b"<name>filter_name</name>"
            b"<type>alert</type>"
            b"</create_filter>",
        )

    def test_create_filter_invalid_filter_type(self):
        with self.assertRaises(InvalidArgument):
            Filters.create_filter("filter_name", filter_type="invalid")

    def test_create_filter_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Filters.create_filter(None)

        with self.assertRaises(RequiredArgument):
            Filters.create_filter("")

    def test_delete_filter(self):
        request = Filters.delete_filter("filter_id")
        self.assertEqual(
            bytes(request),
            b'<delete_filter filter_id="filter_id" ultimate="0"/>',
        )

    def test_delete_filter_with_ultimate(self):
        request = Filters.delete_filter("filter_id", ultimate=True)
        self.assertEqual(
            bytes(request),
            b'<delete_filter filter_id="filter_id" ultimate="1"/>',
        )

        request = Filters.delete_filter("filter_id", ultimate=False)
        self.assertEqual(
            bytes(request),
            b'<delete_filter filter_id="filter_id" ultimate="0"/>',
        )

    def test_delete_filter_missing_filter_id(self):
        with self.assertRaises(RequiredArgument):
            Filters.delete_filter(None)

        with self.assertRaises(RequiredArgument):
            Filters.delete_filter("")

    def test_get_filters(self):
        request = Filters.get_filters()
        self.assertEqual(
            bytes(request),
            b"<get_filters/>",
        )

    def test_get_filters_with_filter_string(self):
        request = Filters.get_filters(filter_string="filter_string")
        self.assertEqual(
            bytes(request),
            b'<get_filters filter="filter_string"/>',
        )

    def test_get_filters_with_filter_id(self):
        request = Filters.get_filters(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_filters filt_id="filter_id"/>',
        )

    def test_get_filters_with_trash(self):
        request = Filters.get_filters(trash=True)
        self.assertEqual(
            bytes(request),
            b'<get_filters trash="1"/>',
        )

        request = Filters.get_filters(trash=False)
        self.assertEqual(
            bytes(request),
            b'<get_filters trash="0"/>',
        )

    def test_get_filters_with_alerts(self):
        request = Filters.get_filters(alerts=True)
        self.assertEqual(
            bytes(request),
            b'<get_filters alerts="1"/>',
        )

        request = Filters.get_filters(alerts=False)
        self.assertEqual(
            bytes(request),
            b'<get_filters alerts="0"/>',
        )

    def test_get_filter(self):
        request = Filters.get_filter("filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_filters filter_id="filter_id"/>',
        )

    def test_get_filter_with_alerts(self):
        request = Filters.get_filter("filter_id", alerts=True)
        self.assertEqual(
            bytes(request),
            b'<get_filters filter_id="filter_id" alerts="1"/>',
        )

        request = Filters.get_filter("filter_id", alerts=False)
        self.assertEqual(
            bytes(request),
            b'<get_filters filter_id="filter_id" alerts="0"/>',
        )

    def test_get_filter_missing_filter_id(self):
        with self.assertRaises(RequiredArgument):
            Filters.get_filter(None)

        with self.assertRaises(RequiredArgument):
            Filters.get_filter("")

    def test_modify_filter(self):
        request = Filters.modify_filter("filter_id")
        self.assertEqual(
            bytes(request),
            b'<modify_filter filter_id="filter_id"/>',
        )

    def test_modify_filter_with_comment(self):
        request = Filters.modify_filter("filter_id", comment="comment")
        self.assertEqual(
            bytes(request),
            b'<modify_filter filter_id="filter_id">'
            b"<comment>comment</comment>"
            b"</modify_filter>",
        )

    def test_modify_filter_with_name(self):
        request = Filters.modify_filter("filter_id", name="name")
        self.assertEqual(
            bytes(request),
            b'<modify_filter filter_id="filter_id">'
            b"<name>name</name>"
            b"</modify_filter>",
        )

    def test_modify_filter_with_term(self):
        request = Filters.modify_filter("filter_id", term="term")
        self.assertEqual(
            bytes(request),
            b'<modify_filter filter_id="filter_id">'
            b"<term>term</term>"
            b"</modify_filter>",
        )

    def test_modify_filter_with_type(self):
        request = Filters.modify_filter(
            "filter_id", filter_type=FilterType.ALERT
        )
        self.assertEqual(
            bytes(request),
            b'<modify_filter filter_id="filter_id">'
            b"<type>alert</type>"
            b"</modify_filter>",
        )

        request = Filters.modify_filter("filter_id", filter_type="alert")
        self.assertEqual(
            bytes(request),
            b'<modify_filter filter_id="filter_id">'
            b"<type>alert</type>"
            b"</modify_filter>",
        )

    def test_modify_filter_missing_filter_id(self):
        with self.assertRaises(RequiredArgument):
            Filters.modify_filter(None)

        with self.assertRaises(RequiredArgument):
            Filters.modify_filter("")
