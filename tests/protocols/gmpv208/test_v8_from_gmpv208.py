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

from . import Gmpv208TestCase
from ..gmpv8.testcmds import *  # pylint: disable=unused-wildcard-import,wildcard-import


class Gmpv208CloneTicketTestCase(GmpCloneTicketTestCase, Gmpv208TestCase):
    pass


class Gmpv208CreateCredentialTestCase(
    GmpCreateCredentialTestCase, Gmpv208TestCase
):
    pass


class Gmpv208CreateScheduleTestCase(GmpCreateScheduleTestCase, Gmpv208TestCase):

    pass


class Gmpv208CreateTicketTestCase(GmpCreateTicketTestCase, Gmpv208TestCase):
    pass


class Gmpv208DeleteTicketTestCase(GmpDeleteTicketTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetTicketTestCase(GmpGetTicketTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetTargetsTestCase(GmpGetTargetsTestCase, Gmpv208TestCase):
    pass


class Gmpv208GetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestCase, Gmpv208TestCase
):
    pass


class Gmpv208GetVulnerabilityTestCase(
    GmpGetVulnerabilityTestCase, Gmpv208TestCase
):
    pass


class Gmpv208ModifyTestCase(GmpModifyTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyScheduleTestCase(GmpModifyScheduleTestCase, Gmpv208TestCase):
    pass


class Gmpv208ModifyTicketTestCase(GmpModifyTicketTestCase, Gmpv208TestCase):
    pass
