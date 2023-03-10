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

from ...gmpv208.entities.overrides import (
    GmpCloneOverrideTestMixin,
    GmpDeleteOverrideTestMixin,
    GmpGetOverridesTestMixin,
    GmpGetOverrideTestMixin,
)
from ...gmpv214 import Gmpv214TestCase
from .overrides import GmpCreateOverrideTestMixin, GmpModifyOverrideTestMixin


class Gmpv214CloneOverrideTestCase(GmpCloneOverrideTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateOverrideTestCase(
    GmpCreateOverrideTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214DeleteOverrideTestCase(
    GmpDeleteOverrideTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetOverrideTestCase(GmpGetOverrideTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetOverridesTestCase(GmpGetOverridesTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyOverrideTestCase(
    GmpModifyOverrideTestMixin, Gmpv214TestCase
):
    pass
