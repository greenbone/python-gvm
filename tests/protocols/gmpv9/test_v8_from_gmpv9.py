# -*- coding: utf-8 -*-
# Copyright (C) 2019 Greenbone Networks GmbH
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

from . import Gmpv9TestCase
from ..gmpv8.testcmds import *  # pylint: disable=unused-wildcard-import,wildcard-import


class Gmpv9CloneTicketTestCase(GmpCloneTicketTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateCredentialTestCase(GmpCreateCredentialTestCase, Gmpv9TestCase):

    pass


class Gmpv9CreateScheduleTestCase(GmpCreateScheduleTestCase, Gmpv9TestCase):
    pass


class Gmpv9CreateTargetCommandTestCase(
    GmpCreateTargetCommandTestCase, Gmpv9TestCase
):
    pass


class Gmpv9CreateTicketTestCase(GmpCreateTicketTestCase, Gmpv9TestCase):
    pass


class Gmpv9DeleteTicketTestCase(GmpDeleteTicketTestCase, Gmpv9TestCase):

    pass


class Gmpv9GetTicketTestCase(GmpGetTicketTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetTargetsTestCase(GmpGetTargetsTestCase, Gmpv9TestCase):
    pass


class Gmpv9GetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestCase, Gmpv9TestCase
):
    pass


class Gmpv9GetVulnerabilityTestCase(GmpGetVulnerabilityTestCase, Gmpv9TestCase):

    pass


class Gmpv9ModifyTestCase(GmpModifyTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyScheduleTestCase(GmpModifyScheduleTestCase, Gmpv9TestCase):
    pass


class Gmpv9ModifyTicketTestCase(GmpModifyTicketTestCase, Gmpv9TestCase):
    pass
