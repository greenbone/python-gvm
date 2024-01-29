# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
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
