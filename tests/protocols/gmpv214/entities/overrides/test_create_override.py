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


class GmpCreateOverrideTestMixin:
    def test_create_override(self):
        self.gmp.create_override("foo", nvt_oid="oid1")

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "</create_override>"
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
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", hosts=["h1", "h2"])

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "<hosts>h1,h2</hosts>"
            "</create_override>"
        )

    def test_create_override_with_port(self):
        self.gmp.create_override(nvt_oid="oid1", text="foo", port="123/udp")

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "<port>123/udp</port>"
            "</create_override>"
        )

    def test_create_override_with_result_id(self):
        self.gmp.create_override("foo", nvt_oid="oid1", result_id="r1")

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            '<result id="r1"/>'
            "</create_override>"
        )

    def test_create_override_with_task_id(self):
        self.gmp.create_override("foo", nvt_oid="oid1", task_id="t1")

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            '<task id="t1"/>'
            "</create_override>"
        )

    def test_create_override_with_severity(self):
        self.gmp.create_override("foo", nvt_oid="oid1", severity="5.5")

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "<severity>5.5</severity>"
            "</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", severity=5.5)

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "<severity>5.5</severity>"
            "</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", severity=Decimal(5.5))

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "<severity>5.5</severity>"
            "</create_override>"
        )

    def test_create_override_with_new_severity(self):
        self.gmp.create_override("foo", nvt_oid="oid1", new_severity="5.5")

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "<new_severity>5.5</new_severity>"
            "</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", new_severity=5.5)

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "<new_severity>5.5</new_severity>"
            "</create_override>"
        )

        self.gmp.create_override(
            "foo", nvt_oid="oid1", new_severity=Decimal(5.5)
        )

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "<new_severity>5.5</new_severity>"
            "</create_override>"
        )

    def test_create_override_with_threat(self):
        self.gmp.create_override(
            "foo", nvt_oid="oid1", threat=SeverityLevel.HIGH
        )

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "</create_override>"
        )

    def test_create_override_with_new_threat(self):
        self.gmp.create_override(
            "foo", nvt_oid="oid1", new_threat=SeverityLevel.HIGH
        )

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "</create_override>"
        )

    def test_create_override_with_days_active(self):
        self.gmp.create_override("foo", nvt_oid="oid1", days_active=0)

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "<active>0</active>"
            "</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", days_active=-1)

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "<active>-1</active>"
            "</create_override>"
        )

        self.gmp.create_override("foo", nvt_oid="oid1", days_active=3600)

        self.connection.send.has_been_called_with(
            "<create_override>"
            "<text>foo</text>"
            '<nvt oid="oid1"/>'
            "<active>3600</active>"
            "</create_override>"
        )

    def test_create_override_with_invalid_port(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.create_override(nvt_oid="oid1", text="foo", port="123")

        with self.assertRaises(InvalidArgument):
            self.gmp.create_override(nvt_oid="oid1", text="foo", port="tcp/123")
