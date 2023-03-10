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

from ...gmpv208.entities.permissions import (
    GmpClonePermissionTestMixin,
    GmpCreatePermissionTestMixin,
    GmpDeletePermissionTestMixin,
    GmpGetPermissionsTestMixin,
    GmpGetPermissionTestMixin,
    GmpModifyPermissionTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214DeletePermissionTestCase(
    GmpDeletePermissionTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetPermissionTestCase(GmpGetPermissionTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetPermissionsTestCase(
    GmpGetPermissionsTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ClonePermissionTestCase(
    GmpClonePermissionTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214CreatePermissionTestCase(
    GmpCreatePermissionTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPermissionTestCase(
    GmpModifyPermissionTestMixin, Gmpv214TestCase
):
    pass
