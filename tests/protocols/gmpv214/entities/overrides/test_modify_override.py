# -*- coding: utf-8 -*-
# Copyright (C) 2020-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from decimal import Decimal

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmpv214 import SeverityLevel


class GmpModifyOverrideTestMixin:
    def test_modify_override(self):
        self.gmp.modify_override(override_id="o1", text="foo")

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "</modify_override>"
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
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<active>0</active>"
            "</modify_override>"
        )

        self.gmp.modify_override(override_id="o1", text="foo", days_active=-1)

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<active>-1</active>"
            "</modify_override>"
        )

        self.gmp.modify_override(override_id="o1", text="foo", days_active=600)

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<active>600</active>"
            "</modify_override>"
        )

    def test_modify_override_with_port(self):
        self.gmp.modify_override(override_id="o1", text="foo", port="123/udp")

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<port>123/udp</port>"
            "</modify_override>"
        )

    def test_modify_override_with_hosts(self):
        self.gmp.modify_override(override_id="o1", text="foo", hosts=["foo"])

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<hosts>foo</hosts>"
            "</modify_override>"
        )

        self.gmp.modify_override(
            override_id="o1", text="foo", hosts=["foo", "bar"]
        )

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<hosts>foo,bar</hosts>"
            "</modify_override>"
        )

    def test_modify_override_with_result_id(self):
        self.gmp.modify_override(override_id="o1", text="foo", result_id="r1")

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            '<result id="r1"/>'
            "</modify_override>"
        )

    def test_modify_override_with_task_id(self):
        self.gmp.modify_override(override_id="o1", text="foo", task_id="r1")

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            '<task id="r1"/>'
            "</modify_override>"
        )

    def test_modify_override_with_severity(self):
        self.gmp.modify_override(override_id="o1", text="foo", severity="5.5")

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<severity>5.5</severity>"
            "</modify_override>"
        )

        self.gmp.modify_override(override_id="o1", text="foo", severity=5.5)

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<severity>5.5</severity>"
            "</modify_override>"
        )

        self.gmp.modify_override(
            override_id="o1", text="foo", severity=Decimal(5.5)
        )

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<severity>5.5</severity>"
            "</modify_override>"
        )

    def test_modify_override_with_new_severity(self):
        self.gmp.modify_override(
            override_id="o1", text="foo", new_severity="5.5"
        )

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<new_severity>5.5</new_severity>"
            "</modify_override>"
        )

        self.gmp.modify_override(override_id="o1", text="foo", new_severity=5.5)

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<new_severity>5.5</new_severity>"
            "</modify_override>"
        )

        self.gmp.modify_override(
            override_id="o1", text="foo", new_severity=Decimal(5.5)
        )

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "<new_severity>5.5</new_severity>"
            "</modify_override>"
        )

    def test_modify_override_with_threat(self):
        self.gmp.modify_override(
            override_id="o1", text="foo", threat=SeverityLevel.HIGH
        )

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "</modify_override>"
        )

    def test_modify_override_with_new_threat(self):
        self.gmp.modify_override(
            override_id="o1", text="foo", new_threat=SeverityLevel.HIGH
        )

        self.connection.send.has_been_called_with(
            '<modify_override override_id="o1">'
            "<text>foo</text>"
            "</modify_override>"
        )

    def test_modify_override_with_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_override(override_id="o1", text="foo", port="123")

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_override(
                override_id="o1", text="foo", port="tcp/123"
            )
