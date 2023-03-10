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

from ...gmpv208.entities.alerts import (
    GmpCloneAlertTestMixin,
    GmpCreateAlertTestMixin,
    GmpDeleteAlertTestMixin,
    GmpGetAlertsTestMixin,
    GmpGetAlertTestMixin,
    GmpModifyAlertTestMixin,
    GmpTestAlertTestMixin,
    GmpTriggerAlertTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214CloneAlertTestCase(GmpCloneAlertTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateAlertTestCase(GmpCreateAlertTestMixin, Gmpv214TestCase):
    pass


class Gmpv214DeleteAlertTestCase(GmpDeleteAlertTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetAlertTestCase(GmpGetAlertTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetAlertsTestCase(GmpGetAlertsTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyAlertTestCase(GmpModifyAlertTestMixin, Gmpv214TestCase):
    pass


class Gmpv214TestAlertTestCase(GmpTestAlertTestMixin, Gmpv214TestCase):
    pass


class Gmpv214TriggerAlertTestCase(GmpTriggerAlertTestMixin, Gmpv214TestCase):
    pass
