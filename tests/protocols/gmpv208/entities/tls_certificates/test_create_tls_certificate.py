# -*- coding: utf-8 -*-
# Copyright (C) 2018-2022 Greenbone AG
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

from gvm.errors import RequiredArgument


class GmpCreateTLSCertificateTestMixin:
    def test_create_tls_certificate(self):
        self.gmp.create_tls_certificate("foo", "c1", comment="bar", trust=True)

        self.connection.send.has_been_called_with(
            "<create_tls_certificate>"
            "<comment>bar</comment>"
            "<name>foo</name>"
            "<certificate>c1</certificate>"
            "<trust>1</trust>"
            "</create_tls_certificate>"
        )

        self.gmp.create_tls_certificate("foo", "c1", trust=False)

        self.connection.send.has_been_called_with(
            "<create_tls_certificate>"
            "<name>foo</name>"
            "<certificate>c1</certificate>"
            "</create_tls_certificate>"
        )

    def test_missing_certificate(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_tls_certificate(name="foo", certificate="")

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tls_certificate(name="foo", certificate=None)

    def test_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_tls_certificate(name=None, certificate="c1")

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tls_certificate(name="", certificate="c1")
