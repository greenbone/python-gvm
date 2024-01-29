# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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
