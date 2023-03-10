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
from .reports import (
    GmpDeleteReportTestMixin,
    GmpGetReportsTestMixin,
    GmpGetReportTestMixin,
    GmpImportReportTestMixin,
)


class Gmpv208DeleteReportTestCase(GmpDeleteReportTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetReportTestCase(GmpGetReportTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetReportsTestCase(GmpGetReportsTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ImportReportTestCase(GmpImportReportTestMixin, Gmpv208TestCase):
    pass
