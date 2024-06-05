# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from decimal import Decimal

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import Overrides


class OverridesTestCase(unittest.TestCase):
    def test_create_override(self):
        request = Overrides.create_override("foo", nvt_oid="oid1")

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"</create_override>",
        )

    def test_create_override_missing_text(self):
        with self.assertRaises(RequiredArgument):
            Overrides.create_override(None, "od1")

        with self.assertRaises(RequiredArgument):
            Overrides.create_override("", "oid1")

    def test_create_override_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            Overrides.create_override("foo", None)

        with self.assertRaises(RequiredArgument):
            Overrides.create_override("foo", "")

    def test_create_override_with_hosts(self):
        request = Overrides.create_override("foo", nvt_oid="oid1", hosts=[])

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"</create_override>",
        )

        request = Overrides.create_override(
            "foo", nvt_oid="oid1", hosts=["h1", "h2"]
        )

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<hosts>h1,h2</hosts>"
            b"</create_override>",
        )

    def test_create_override_with_port(self):
        request = Overrides.create_override(
            "foo", nvt_oid="oid1", port="666/udp"
        )

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<port>666/udp</port>"
            b"</create_override>",
        )

    def test_create_override_with_result_id(self):
        request = Overrides.create_override(
            "foo", nvt_oid="oid1", result_id="r1"
        )

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b'<result id="r1"/>'
            b"</create_override>",
        )

    def test_create_override_with_task_id(self):
        request = Overrides.create_override("foo", nvt_oid="oid1", task_id="t1")

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b'<task id="t1"/>'
            b"</create_override>",
        )

    def test_create_override_with_severity(self):
        request = Overrides.create_override(
            "foo", nvt_oid="oid1", severity="5.5"
        )

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<severity>5.5</severity>"
            b"</create_override>",
        )

        request = Overrides.create_override("foo", nvt_oid="oid1", severity=5.5)

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<severity>5.5</severity>"
            b"</create_override>",
        )

        request = Overrides.create_override(
            "foo", nvt_oid="oid1", severity=Decimal(5.5)
        )

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<severity>5.5</severity>"
            b"</create_override>",
        )

    def test_create_override_with_new_severity(self):
        request = Overrides.create_override(
            "foo", nvt_oid="oid1", new_severity="5.5"
        )

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<new_severity>5.5</new_severity>"
            b"</create_override>",
        )

        request = Overrides.create_override(
            "foo", nvt_oid="oid1", new_severity=5.5
        )

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<new_severity>5.5</new_severity>"
            b"</create_override>",
        )

        request = Overrides.create_override(
            "foo", nvt_oid="oid1", new_severity=Decimal(5.5)
        )

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<new_severity>5.5</new_severity>"
            b"</create_override>",
        )

    def test_create_override_with_days_active(self):
        request = Overrides.create_override(
            "foo", nvt_oid="oid1", days_active=0
        )

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<active>0</active>"
            b"</create_override>",
        )

        request = Overrides.create_override(
            "foo", nvt_oid="oid1", days_active=5
        )

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<active>5</active>"
            b"</create_override>",
        )

        request = Overrides.create_override(
            "foo", nvt_oid="oid1", days_active=-1
        )

        self.assertEqual(
            bytes(request),
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<active>-1</active>"
            b"</create_override>",
        )

    def test_create_override_with_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            Overrides.create_override("foo", nvt_oid="oid1", port="invalid")

        with self.assertRaises(InvalidArgument):
            Overrides.create_override("foo", nvt_oid="oid1", port="123")

        with self.assertRaises(InvalidArgument):
            Overrides.create_override(
                text="foo", nvt_oid="oid1", port="tcp/123"
            )

    def test_modify_override(self):
        request = Overrides.modify_override("o1", "foo")

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"</modify_override>",
        )

    def test_modify_override_missing_override_id(self):
        with self.assertRaises(RequiredArgument):
            Overrides.modify_override(None, "foo")

        with self.assertRaises(RequiredArgument):
            Overrides.modify_override("", "foo")

    def test_modify_override_missing_text(self):
        with self.assertRaises(RequiredArgument):
            Overrides.modify_override("o1", None)

        with self.assertRaises(RequiredArgument):
            Overrides.modify_override("o1", "")

    def test_modify_override_with_days_active(self):
        request = Overrides.modify_override("o1", "foo", days_active=0)

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<active>0</active>"
            b"</modify_override>",
        )

        request = Overrides.modify_override("o1", "foo", days_active=5)

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<active>5</active>"
            b"</modify_override>",
        )

        request = Overrides.modify_override("o1", "foo", days_active=-1)

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<active>-1</active>"
            b"</modify_override>",
        )

    def test_modify_override_with_port(self):
        request = Overrides.modify_override("o1", "foo", port="666/udp")

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<port>666/udp</port>"
            b"</modify_override>",
        )

    def test_modify_override_with_hosts(self):
        request = Overrides.modify_override("o1", "foo", hosts=["h1"])

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<hosts>h1</hosts>"
            b"</modify_override>",
        )

        request = Overrides.modify_override("o1", "foo", hosts=["h1", "h2"])

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<hosts>h1,h2</hosts>"
            b"</modify_override>",
        )

    def test_modify_override_with_result_id(self):
        request = Overrides.modify_override("o1", "foo", result_id="r1")

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b'<result id="r1"/>'
            b"</modify_override>",
        )

    def test_modify_override_with_task_id(self):
        request = Overrides.modify_override("o1", "foo", task_id="t1")

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b'<task id="t1"/>'
            b"</modify_override>",
        )

    def test_modify_override_with_severity(self):
        request = Overrides.modify_override("o1", "foo", severity="5.5")

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_override>",
        )

        request = Overrides.modify_override("o1", "foo", severity=5.5)

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_override>",
        )

        request = Overrides.modify_override("o1", "foo", severity=Decimal(5.5))

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_override>",
        )

    def test_modify_override_with_new_severity(self):
        request = Overrides.modify_override("o1", "foo", new_severity="5.5")

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<new_severity>5.5</new_severity>"
            b"</modify_override>",
        )

        request = Overrides.modify_override("o1", "foo", new_severity=5.5)

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<new_severity>5.5</new_severity>"
            b"</modify_override>",
        )

        request = Overrides.modify_override(
            "o1", "foo", new_severity=Decimal(5.5)
        )

        self.assertEqual(
            bytes(request),
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<new_severity>5.5</new_severity>"
            b"</modify_override>",
        )

    def test_modify_override_with_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            Overrides.modify_override("o1", "foo", port="invalid")

        with self.assertRaises(InvalidArgument):
            Overrides.modify_override("o1", "foo", port="123")

        with self.assertRaises(InvalidArgument):
            Overrides.modify_override("o1", "foo", port="tcp/123")

    def test_clone_override(self):
        request = Overrides.clone_override("o1")

        self.assertEqual(
            bytes(request),
            b"<create_override><copy>o1</copy></create_override>",
        )

    def test_clone_override_missing_override_id(self):
        with self.assertRaises(RequiredArgument):
            Overrides.clone_override(None)

        with self.assertRaises(RequiredArgument):
            Overrides.clone_override("")

    def test_delete_override(self):
        request = Overrides.delete_override("o1")

        self.assertEqual(
            bytes(request),
            b'<delete_override override_id="o1" ultimate="0"/>',
        )

    def test_delete_override_ultimate(self):
        request = Overrides.delete_override("o1", ultimate=True)

        self.assertEqual(
            bytes(request),
            b'<delete_override override_id="o1" ultimate="1"/>',
        )

        request = Overrides.delete_override("o1", ultimate=False)

        self.assertEqual(
            bytes(request),
            b'<delete_override override_id="o1" ultimate="0"/>',
        )

    def test_delete_override_missing_override_id(self):
        with self.assertRaises(RequiredArgument):
            Overrides.delete_override(None)

        with self.assertRaises(RequiredArgument):
            Overrides.delete_override("")

    def test_get_overrides(self):
        request = Overrides.get_overrides()

        self.assertEqual(
            bytes(request),
            b"<get_overrides/>",
        )

    def test_get_overrides_with_filter_string(self):
        request = Overrides.get_overrides(filter_string="foo=bar")

        self.assertEqual(bytes(request), b'<get_overrides filter="foo=bar"/>')

    def test_get_overrides_with_filter_id(self):
        request = Overrides.get_overrides(filter_id="f1")

        self.assertEqual(bytes(request), b'<get_overrides filt_id="f1"/>')

    def test_get_overrides_with_details(self):
        request = Overrides.get_overrides(details=True)

        self.assertEqual(bytes(request), b'<get_overrides details="1"/>')

        request = Overrides.get_overrides(details=False)

        self.assertEqual(bytes(request), b'<get_overrides details="0"/>')

    def test_get_overrides_with_result(self):
        request = Overrides.get_overrides(result=True)

        self.assertEqual(bytes(request), b'<get_overrides result="1"/>')

        request = Overrides.get_overrides(result=False)

        self.assertEqual(bytes(request), b'<get_overrides result="0"/>')

    def test_get_override(self):
        request = Overrides.get_override("o1")

        self.assertEqual(
            bytes(request),
            b'<get_overrides override_id="o1" details="1"/>',
        )

    def test_get_override_missing_override_id(self):
        with self.assertRaises(RequiredArgument):
            Overrides.get_override(None)

        with self.assertRaises(RequiredArgument):
            Overrides.get_override("")
