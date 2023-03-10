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


class GmpGetReportsTestMixin:
    def test_get_reports(self):
        self.gmp.get_reports()

        self.connection.send.has_been_called_with("<get_reports/>")

    def test_get_reports_with_filter_string(self):
        self.gmp.get_reports(filter_string="name=foo", ignore_pagination=1)

        self.connection.send.has_been_called_with(
            '<get_reports report_filter="name=foo" ignore_pagination="1"/>'
        )

    def test_get_reports_with_filter_id(self):
        self.gmp.get_reports(filter_id="f1")

        self.connection.send.has_been_called_with(
            '<get_reports report_filt_id="f1"/>'
        )

    def test_get_reports_without_note_details(self):
        self.gmp.get_reports(note_details=False)

        self.connection.send.has_been_called_with(
            '<get_reports note_details="0"/>'
        )

    def test_get_reports_with_note_details(self):
        self.gmp.get_reports(note_details=True, ignore_pagination=False)

        self.connection.send.has_been_called_with(
            '<get_reports note_details="1" ignore_pagination="0"/>'
        )

    def test_get_reports_without_override_details(self):
        self.gmp.get_reports(override_details=False)

        self.connection.send.has_been_called_with(
            '<get_reports override_details="0"/>'
        )

    def test_get_reports_with_override_details(self):
        self.gmp.get_reports(override_details=True)

        self.connection.send.has_been_called_with(
            '<get_reports override_details="1"/>'
        )

    def test_get_reports_with_details(self):
        self.gmp.get_reports(details=True)

        self.connection.send.has_been_called_with('<get_reports details="1"/>')

    def test_get_reports_without_details(self):
        self.gmp.get_reports(details=False)

        self.connection.send.has_been_called_with('<get_reports details="0"/>')
