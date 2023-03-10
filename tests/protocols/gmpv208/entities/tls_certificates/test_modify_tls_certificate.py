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


class GmpModifyTLSCertificateTestMixin:
    def test_modify_tls_certificate(self):
        self.gmp.modify_tls_certificate("c1")

        self.connection.send.has_been_called_with(
            '<modify_tls_certificate tls_certificate_id="c1"/>'
        )

    def test_modify_tls_certificate_with_name(self):
        self.gmp.modify_tls_certificate("c1", name="foo")

        self.connection.send.has_been_called_with(
            '<modify_tls_certificate tls_certificate_id="c1">'
            "<name>foo</name>"
            "</modify_tls_certificate>"
        )

    def test_modify_tls_certificate_with_comment(self):
        self.gmp.modify_tls_certificate("c1", comment="foo")

        self.connection.send.has_been_called_with(
            '<modify_tls_certificate tls_certificate_id="c1">'
            "<comment>foo</comment>"
            "</modify_tls_certificate>"
        )

    def test_modify_tls_certificate_with_trust(self):
        self.gmp.modify_tls_certificate("c1", trust=True)

        self.connection.send.has_been_called_with(
            '<modify_tls_certificate tls_certificate_id="c1">'
            "<trust>1</trust>"
            "</modify_tls_certificate>"
        )

        self.gmp.modify_tls_certificate("c1", trust=False)

        self.connection.send.has_been_called_with(
            '<modify_tls_certificate tls_certificate_id="c1"/>'
        )

    def test_missing_tls_certificate_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_tls_certificate(name="foo", tls_certificate_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_tls_certificate(name="foo", tls_certificate_id=None)
