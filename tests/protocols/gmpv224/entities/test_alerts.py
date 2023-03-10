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
from ...gmpv224 import Gmpv224TestCase


class Gmpv224CloneAlertTestCase(GmpCloneAlertTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateAlertTestCase(GmpCreateAlertTestMixin, Gmpv224TestCase):
    pass


class Gmpv224DeleteAlertTestCase(GmpDeleteAlertTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetAlertTestCase(GmpGetAlertTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetAlertsTestCase(GmpGetAlertsTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyAlertTestCase(GmpModifyAlertTestMixin, Gmpv224TestCase):
    pass


class Gmpv224TestAlertTestCase(GmpTestAlertTestMixin, Gmpv224TestCase):
    pass


class Gmpv224TriggerAlertTestCase(GmpTriggerAlertTestMixin, Gmpv224TestCase):
    pass
