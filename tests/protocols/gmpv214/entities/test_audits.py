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

from ...gmpv208.entities.audits import (
    GmpCloneAuditTestMixin,
    GmpCreateAuditTestMixin,
    GmpDeleteAuditTestMixin,
    GmpGetAuditsTestMixin,
    GmpGetAuditTestMixin,
    GmpModifyAuditTestMixin,
    GmpResumeAuditTestMixin,
    GmpStartAuditTestMixin,
    GmpStopAuditTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214CloneAuditTestCase(GmpCloneAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateAuditTestCase(GmpCreateAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214DeleteAuditTestCase(GmpDeleteAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetAuditTestCase(GmpGetAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetAuditsTestCase(GmpGetAuditsTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyAuditTestCase(GmpModifyAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ResumeAuditTestCase(GmpResumeAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214StartAuditTestCase(GmpStartAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214StopAuditTestCase(GmpStopAuditTestMixin, Gmpv214TestCase):
    pass
