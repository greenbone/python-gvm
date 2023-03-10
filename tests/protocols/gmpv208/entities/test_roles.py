# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
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

from ...gmpv208 import Gmpv208TestCase
from .roles import (
    GmpCloneRoleTestMixin,
    GmpCreateRoleTestMixin,
    GmpDeleteRoleTestMixin,
    GmpGetRolesTestMixin,
    GmpGetRoleTestMixin,
    GmpModifyRoleTestMixin,
)


class Gmpv208DeleteRoleTestCase(GmpDeleteRoleTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetRoleTestCase(GmpGetRoleTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetRolesTestCase(GmpGetRolesTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CloneRoleTestCase(GmpCloneRoleTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateRoleTestCase(GmpCreateRoleTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyRoleTestCase(GmpModifyRoleTestMixin, Gmpv208TestCase):
    pass
