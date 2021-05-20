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

from . import Gmpv208TestCase
from .testcmds import *  # pylint: disable=unused-wildcard-import, wildcard-import


class Gmpv208AuthenticateTestCase(GmpAuthenticateTestCase, Gmpv208TestCase):
    pass


class Gmpv208HelpTestCase(GmpHelpTestCase, Gmpv208TestCase):
    pass


class Gmpv208DescribeAuthCommandTestCase(
    GmpDescribeAuthCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208EmptyTrashcanCommandTestCase(
    GmpEmptyTrashcanCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetSystemReportsTestCase(
    GmpGetSystemReportsTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetVersionCommandTestCase(
    GmpGetVersionCommandTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyAuthTestCase(GmpModifyAuthTestCase, Gmpv208TestCase):
    pass


class Gmpv208RestoreTestCase(GmpRestoreTestCase, Gmpv208TestCase):
    pass


class Gmpv208v7WithStatementTestCase(GmpWithStatementTestCase, Gmpv208TestCase):
    pass
