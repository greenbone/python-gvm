# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Greenbone Networks GmbH
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

from . import Gmpv214TestCase
from ..gmpv208.testcmds import *  # pylint: disable=unused-wildcard-import,wildcard-import


class Gmpv214CloneAgentTestCase(GmpCloneAgentTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateFilterTestCase(GmpCreateFilterTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreatePermissionTestCase(
    GmpCreatePermissionTestCase, Gmpv214TestCase
):
    pass


class Gmpv214CreateTagTestCase(GmpCreateTagTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetAggregatesTestCase(GmpGetAggregatesTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetInfoTestCase(GmpGetInfoTestCase, Gmpv214TestCase):
    pass


class Gmpv214GetInfoListTestCase(GmpGetInfoListTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyFilterTestCase(GmpModifyFilterTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyPermissionTestCase(
    GmpModifyPermissionTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyReportFormatTestCase(
    GmpModifyReportFormatTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyTagTestCase(GmpModifyTagTestCase, Gmpv214TestCase):
    pass
