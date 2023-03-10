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

from ...gmpv208.entities.users import (
    GmpCloneUserTestMixin,
    GmpCreateUserTestMixin,
    GmpDeleteUserTestMixin,
    GmpGetUsersTestMixin,
    GmpGetUserTestMixin,
)
from ...gmpv214 import Gmpv214TestCase
from .users import GmpModifyUserTestMixin


class Gmpv214CloneUserTestCase(GmpCloneUserTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateUserTestCase(GmpCreateUserTestMixin, Gmpv214TestCase):
    pass


class Gmpv214DeleteUserTestCase(GmpDeleteUserTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetUserTestCase(GmpGetUserTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetUsersTestCase(GmpGetUsersTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyUserTestCase(GmpModifyUserTestMixin, Gmpv214TestCase):
    pass
