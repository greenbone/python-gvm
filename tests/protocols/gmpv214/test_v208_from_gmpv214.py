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


class Gmpv214AuthenticateTestCase(GmpAuthenticateTestCase, Gmpv214TestCase):
    pass


class Gmpv214HelpTestCase(GmpHelpTestCase, Gmpv214TestCase):
    pass


class Gmpv214DescribeAuthCommandTestCase(
    GmpDescribeAuthCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214EmptyTrashcanCommandTestCase(
    GmpEmptyTrashcanCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214GetSystemReportsTestCase(
    GmpGetSystemReportsTestCase, Gmpv214TestCase
):
    pass


class Gmpv214GetVersionCommandTestCase(
    GmpGetVersionCommandTestCase, Gmpv214TestCase
):
    pass


class Gmpv214ModifyAuthTestCase(GmpModifyAuthTestCase, Gmpv214TestCase):
    pass


class Gmpv214RestoreTestCase(GmpRestoreTestCase, Gmpv214TestCase):
    pass


class Gmpv214v7WithStatementTestCase(GmpWithStatementTestCase, Gmpv214TestCase):
    pass
