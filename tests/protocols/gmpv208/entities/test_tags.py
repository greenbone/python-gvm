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
from .tags import (
    GmpCloneTagTestMixin,
    GmpCreateTagTestMixin,
    GmpDeleteTagTestMixin,
    GmpGetTagsTestMixin,
    GmpGetTagTestMixin,
    GmpModifyTagTestMixin,
)


class Gmpv208DeleteTagTestCase(GmpDeleteTagTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetTagTestCase(GmpGetTagTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetTagsTestCase(GmpGetTagsTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CloneTagTestCase(GmpCloneTagTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateTagTestCase(GmpCreateTagTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyTagTestCase(GmpModifyTagTestMixin, Gmpv208TestCase):
    pass
