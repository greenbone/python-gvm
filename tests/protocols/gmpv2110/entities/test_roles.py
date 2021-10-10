# -*- coding: utf-8 -*-
# Copyright (C) 2021 Greenbone Networks GmbH
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
from ...gmpv208.entities.roles import (
    GmpCloneRoleTestMixin,
    GmpCreateRoleTestMixin,
    GmpDeleteRoleTestMixin,
    GmpGetRoleTestMixin,
    GmpGetRolesTestMixin,
    GmpModifyRoleTestMixin,
)


class Gmpv2110DeleteRoleTestCase(GmpDeleteRoleTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetRoleTestCase(GmpGetRoleTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetRolesTestCase(GmpGetRolesTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110CloneRoleTestCase(GmpCloneRoleTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110CreateRoleTestCase(GmpCreateRoleTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110ModifyRoleTestCase(GmpModifyRoleTestMixin, Gmpv2110TestCase):
    pass
