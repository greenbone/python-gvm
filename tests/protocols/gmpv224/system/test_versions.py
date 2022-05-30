# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone Networks GmbH
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

from ...gmpv224 import Gmpv224TestCase
from ...gmpv208.system.versions import GmpGetVersionTestCase
from .versions import GmpGetProtocolVersionTestCase


class Gmpv224GetVersionCommandTestCase(GmpGetVersionTestCase, Gmpv224TestCase):
    pass


class Gmpv224GmpGetProtocolVersionTestCase(
    GmpGetProtocolVersionTestCase, Gmpv224TestCase
):
    pass