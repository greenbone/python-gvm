# -*- coding: utf-8 -*-
# Copyright (C) 2020-2021 Greenbone Networks GmbH
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
from .testcmds import *  # pylint: disable=wildcard-import


class Gmpv214CreateNoteTestCase(GmpCreateNoteTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateOverrideTestCase(GmpCreateOverrideTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateTargetTestCase(GmpCreateTargetTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyNoteTestCase(GmpModifyNoteTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyOverrideTestCase(GmpModifyOverrideTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyTargetTestCase(GmpModifyTargetTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyUserTestCase(GmpModifyUserTestCase, Gmpv214TestCase):
    pass


class Gmpv214CreateScannerTestCase(GmpCreateScannerTestCase, Gmpv214TestCase):
    pass


class Gmpv214ModifyScannerTestCase(GmpModifyScannerTestCase, Gmpv214TestCase):
    pass
