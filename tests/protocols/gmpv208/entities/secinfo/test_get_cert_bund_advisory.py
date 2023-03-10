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


class GmpGetCertBundTestMixin:
    def test_get_cert_bund_advisory(self):
        self.gmp.get_cert_bund_advisory(cert_id="i1")

        self.connection.send.has_been_called_with(
            '<get_info info_id="i1" type="CERT_BUND_ADV" details="1"/>'
        )

        self.gmp.get_cert_bund_advisory("i1")

        self.connection.send.has_been_called_with(
            '<get_info info_id="i1" type="CERT_BUND_ADV" details="1"/>'
        )

    def test_get_cert_bund_advisory_missing_cert_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_cert_bund_advisory(cert_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_cert_bund_advisory("")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_cert_bund_advisory(cert_id=None)
