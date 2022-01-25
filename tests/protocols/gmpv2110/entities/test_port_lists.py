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

from ...gmpv2110 import Gmpv2110TestCase
from ...gmpv208.entities.port_lists import (
    GmpClonePortListTestMixin,
    GmpCreatePortListTestMixin,
    GmpCreatePortRangeTestMixin,
    GmpDeletePortListTestMixin,
    GmpDeletePortRangeTestMixin,
    GmpGetPortListsTestMixin,
    GmpGetPortListTestMixin,
    GmpModifyPortListTestMixin,
)


class Gmpv2110ClonePortListTestCase(
    GmpClonePortListTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110CreatePortListTestCase(
    GmpCreatePortListTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110CreatePortRangeListTestCase(
    GmpCreatePortRangeTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110DeletePortListTestCase(
    GmpDeletePortListTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110DeletePortRangeTestCase(
    GmpDeletePortRangeTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110GetPortListTestCase(GmpGetPortListTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetPortListsTestCase(GmpGetPortListsTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110ModifyPortListTestCase(
    GmpModifyPortListTestMixin, Gmpv2110TestCase
):
    pass
