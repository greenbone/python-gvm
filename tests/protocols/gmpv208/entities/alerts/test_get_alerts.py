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


class GmpGetAlertsTestMixin:
    def test_get_alerts(self):
        self.gmp.get_alerts()

        self.connection.send.has_been_called_with("<get_alerts/>")

    def test_get_alerts_with_trash(self):
        self.gmp.get_alerts(trash=True)

        self.connection.send.has_been_called_with('<get_alerts trash="1"/>')

        self.gmp.get_alerts(trash=False)

        self.connection.send.has_been_called_with('<get_alerts trash="0"/>')

    def test_get_alerts_with_filter_string(self):
        self.gmp.get_alerts(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            '<get_alerts filter="foo=bar"/>'
        )

    def test_get_alerts_with_filter_id(self):
        self.gmp.get_alerts(filter_id="f1")

        self.connection.send.has_been_called_with('<get_alerts filt_id="f1"/>')

    def test_get_alerts_with_tasks(self):
        self.gmp.get_alerts(tasks=True)

        self.connection.send.has_been_called_with('<get_alerts tasks="1"/>')

        self.gmp.get_alerts(tasks=False)

        self.connection.send.has_been_called_with('<get_alerts tasks="0"/>')
