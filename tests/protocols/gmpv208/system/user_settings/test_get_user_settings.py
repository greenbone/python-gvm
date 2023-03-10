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


class GmpGetUserSettingsTestMixin:
    def test_get_settings(self):
        self.gmp.get_user_settings()

        self.connection.send.has_been_called_with("<get_settings/>")

    def test_get_settings_with_filter_string(self):
        self.gmp.get_user_settings(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            '<get_settings filter="foo=bar"/>'
        )
