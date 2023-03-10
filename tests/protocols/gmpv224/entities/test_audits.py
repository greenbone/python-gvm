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
from ...gmpv224 import Gmpv224TestCase


class Gmpv224CloneAuditTestCase(GmpCloneAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateAuditTestCase(GmpCreateAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224DeleteAuditTestCase(GmpDeleteAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetAuditTestCase(GmpGetAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetAuditsTestCase(GmpGetAuditsTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyAuditTestCase(GmpModifyAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ResumeAuditTestCase(GmpResumeAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224StartAuditTestCase(GmpStartAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224StopAuditTestCase(GmpStopAuditTestMixin, Gmpv224TestCase):
    pass
