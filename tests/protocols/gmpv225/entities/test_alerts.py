# -*- coding: utf-8 -*-
# Copyright (C) 2023 Greenbone AG
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
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CloneAlertTestCase(GmpCloneAlertTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateAlertTestCase(GmpCreateAlertTestMixin, Gmpv225TestCase):
    pass


class Gmpv225DeleteAlertTestCase(GmpDeleteAlertTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetAlertTestCase(GmpGetAlertTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetAlertsTestCase(GmpGetAlertsTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyAlertTestCase(GmpModifyAlertTestMixin, Gmpv225TestCase):
    pass


class Gmpv225TestAlertTestCase(GmpTestAlertTestMixin, Gmpv225TestCase):
    pass


class Gmpv225TriggerAlertTestCase(GmpTriggerAlertTestMixin, Gmpv225TestCase):
    pass
