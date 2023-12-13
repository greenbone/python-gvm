# -*- coding: utf-8 -*-
# Copyright (C) 2023 Greenbone AG
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

from ...gmpv208.entities.report_formats import (
    GmpCloneReportFormatTestMixin,
    GmpDeleteReportFormatTestMixin,
    GmpGetReportFormatsTestMixin,
    GmpGetReportFormatTestMixin,
    GmpImportReportFormatTestMixin,
    GmpModifyReportFormatTestMixin,
    GmpVerifyReportFormatTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteReportFormatTestCase(
    GmpDeleteReportFormatTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetReportFormatTestCase(
    GmpGetReportFormatTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetReportFormatsTestCase(
    GmpGetReportFormatsTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225CloneReportFormatTestCase(
    GmpCloneReportFormatTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ImportReportFormatTestCase(
    GmpImportReportFormatTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyReportFormatTestCase(
    GmpModifyReportFormatTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225VerifyReportFormatTestCase(
    GmpVerifyReportFormatTestMixin, Gmpv225TestCase
):
    pass
