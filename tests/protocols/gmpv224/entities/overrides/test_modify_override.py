# SPDX-FileCopyrightText: 2020-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from decimal import Decimal

from gvm.errors import InvalidArgument, RequiredArgument


class GmpModifyOverrideTestMixin:
    def test_modify_override(self):
        self.gmp.modify_override(override_id="o1", text="foo")

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"</modify_override>"
        )

    def test_modify_override_missing_override_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_override(override_id=None, text="foo")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_override(override_id="", text="foo")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_override("", text="foo")

    def test_modify_override_missing_text(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_override(override_id="o1", text="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_override(override_id="o1", text=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_override("o1", "")

    def test_modify_override_with_days_active(self):
        self.gmp.modify_override(override_id="o1", text="foo", days_active=0)

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<active>0</active>"
            b"</modify_override>"
        )

        self.gmp.modify_override(override_id="o1", text="foo", days_active=-1)

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<active>-1</active>"
            b"</modify_override>"
        )

        self.gmp.modify_override(override_id="o1", text="foo", days_active=600)

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<active>600</active>"
            b"</modify_override>"
        )

    def test_modify_override_with_port(self):
        self.gmp.modify_override(override_id="o1", text="foo", port="123/udp")

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<port>123/udp</port>"
            b"</modify_override>"
        )

    def test_modify_override_with_hosts(self):
        self.gmp.modify_override(override_id="o1", text="foo", hosts=["foo"])

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<hosts>foo</hosts>"
            b"</modify_override>"
        )

        self.gmp.modify_override(
            override_id="o1", text="foo", hosts=["foo", "bar"]
        )

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<hosts>foo,bar</hosts>"
            b"</modify_override>"
        )

    def test_modify_override_with_result_id(self):
        self.gmp.modify_override(override_id="o1", text="foo", result_id="r1")

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b'<result id="r1"/>'
            b"</modify_override>"
        )

    def test_modify_override_with_task_id(self):
        self.gmp.modify_override(override_id="o1", text="foo", task_id="r1")

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b'<task id="r1"/>'
            b"</modify_override>"
        )

    def test_modify_override_with_severity(self):
        self.gmp.modify_override(override_id="o1", text="foo", severity="5.5")

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_override>"
        )

        self.gmp.modify_override(override_id="o1", text="foo", severity=5.5)

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_override>"
        )

        self.gmp.modify_override(
            override_id="o1", text="foo", severity=Decimal(5.5)
        )

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<severity>5.5</severity>"
            b"</modify_override>"
        )

    def test_modify_override_with_new_severity(self):
        self.gmp.modify_override(
            override_id="o1", text="foo", new_severity="5.5"
        )

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<new_severity>5.5</new_severity>"
            b"</modify_override>"
        )

        self.gmp.modify_override(override_id="o1", text="foo", new_severity=5.5)

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<new_severity>5.5</new_severity>"
            b"</modify_override>"
        )

        self.gmp.modify_override(
            override_id="o1", text="foo", new_severity=Decimal(5.5)
        )

        self.connection.send.has_been_called_with(
            b'<modify_override override_id="o1">'
            b"<text>foo</text>"
            b"<new_severity>5.5</new_severity>"
            b"</modify_override>"
        )

    def test_modify_override_with_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_override(override_id="o1", text="foo", port="123")
