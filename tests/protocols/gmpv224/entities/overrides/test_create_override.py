# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from decimal import Decimal

from gvm.errors import InvalidArgument, RequiredArgument


class GmpCreateOverrideTestMixin:
    def test_create_override(self):
        self.gmp.create_override("foo", nvt_oid="oid1")

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"</create_override>"
        )

    def test_create_override_missing_text(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_override(None, "od1")

        with self.assertRaises(RequiredArgument):
            self.gmp.create_override("", "oid1")

    def test_create_override_missing_nvt_oid(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_override("foo", None)

        with self.assertRaises(RequiredArgument):
            self.gmp.create_override("foo", "")

    def test_create_override_with_hosts(self):
        self.gmp.create_override("foo", nvt_oid="oid1", hosts=[])

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", hosts=["h1", "h2"])

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<hosts>h1,h2</hosts>"
            b"</create_override>"
        )

    def test_create_override_with_port(self):
        self.gmp.create_override("foo", nvt_oid="oid1", port="666/udp")

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<port>666/udp</port>"
            b"</create_override>"
        )

    def test_create_override_with_result_id(self):
        self.gmp.create_override("foo", nvt_oid="oid1", result_id="r1")

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b'<result id="r1"/>'
            b"</create_override>"
        )

    def test_create_override_with_task_id(self):
        self.gmp.create_override("foo", nvt_oid="oid1", task_id="t1")

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b'<task id="t1"/>'
            b"</create_override>"
        )

    def test_create_override_with_severity(self):
        self.gmp.create_override("foo", nvt_oid="oid1", severity="5.5")

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<severity>5.5</severity>"
            b"</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", severity=5.5)

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<severity>5.5</severity>"
            b"</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", severity=Decimal(5.5))

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<severity>5.5</severity>"
            b"</create_override>"
        )

    def test_create_override_with_new_severity(self):
        self.gmp.create_override("foo", nvt_oid="oid1", new_severity="5.5")

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<new_severity>5.5</new_severity>"
            b"</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", new_severity=5.5)

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<new_severity>5.5</new_severity>"
            b"</create_override>"
        )

        self.gmp.create_override(
            "foo", nvt_oid="oid1", new_severity=Decimal(5.5)
        )

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<new_severity>5.5</new_severity>"
            b"</create_override>"
        )

    def test_create_override_with_days_active(self):
        self.gmp.create_override("foo", nvt_oid="oid1", days_active=0)

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<active>0</active>"
            b"</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", days_active=-1)

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<active>-1</active>"
            b"</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", days_active=3600)

        self.connection.send.has_been_called_with(
            b"<create_override>"
            b"<text>foo</text>"
            b'<nvt oid="oid1"/>'
            b"<active>3600</active>"
            b"</create_override>"
        )

    def test_create_override_with_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_override(text="foo", nvt_oid="oid1", port="123")

        with self.assertRaises(InvalidArgument):
            self.gmp.create_override(text="foo", nvt_oid="oid1", port="tcp/123")
