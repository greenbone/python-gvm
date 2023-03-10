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


class GmpGetCveListTestMixin:
    def test_get_cpes(self):
        self.gmp.get_cves()

        self.connection.send.has_been_called_with('<get_info type="CVE"/>')

    def test_get_cves_with_filter_string(self):
        self.gmp.get_cves(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            '<get_info type="CVE" filter="foo=bar"/>'
        )

    def test_get_cves_with_filter_id(self):
        self.gmp.get_cves(filter_id="f1")

        self.connection.send.has_been_called_with(
            '<get_info type="CVE" filt_id="f1"/>'
        )

    def test_get_cves_with_name(self):
        self.gmp.get_cves(name="foo")

        self.connection.send.has_been_called_with(
            '<get_info type="CVE" name="foo"/>'
        )

    def test_get_cves_with_details(self):
        self.gmp.get_cves(details=True)

        self.connection.send.has_been_called_with(
            '<get_info type="CVE" details="1"/>'
        )

        self.gmp.get_cves(details=False)

        self.connection.send.has_been_called_with(
            '<get_info type="CVE" details="0"/>'
        )
