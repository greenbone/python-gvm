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


class GmpGetHostsTestMixin:
    def test_get_hosts(self):
        self.gmp.get_hosts()

        self.connection.send.has_been_called_with('<get_assets type="host"/>')

    def test_get_hosts_details(self):
        self.gmp.get_hosts(details=True)

        self.connection.send.has_been_called_with(
            '<get_assets type="host" details="1"/>'
        )

        self.gmp.get_hosts(details=False)

        self.connection.send.has_been_called_with(
            '<get_assets type="host" details="0"/>'
        )

    def test_get_hosts_with_filter_string(self):
        self.gmp.get_hosts(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            '<get_assets type="host" filter="foo=bar"/>'
        )

    def test_get_hosts_with_filter_id(self):
        self.gmp.get_hosts(filter_id="f1")

        self.connection.send.has_been_called_with(
            '<get_assets type="host" filt_id="f1"/>'
        )
