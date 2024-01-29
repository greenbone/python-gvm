# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .alerts import (
    GmpCloneAlertTestMixin,
    GmpCreateAlertTestMixin,
    GmpDeleteAlertTestMixin,
    GmpGetAlertsTestMixin,
    GmpGetAlertTestMixin,
    GmpModifyAlertTestMixin,
    GmpTestAlertTestMixin,
    GmpTriggerAlertTestMixin,
)


class Gmpv208CloneAlertTestCase(GmpCloneAlertTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateAlertTestCase(GmpCreateAlertTestMixin, Gmpv208TestCase):
    pass


class Gmpv208DeleteAlertTestCase(GmpDeleteAlertTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetAlertTestCase(GmpGetAlertTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetAlertsTestCase(GmpGetAlertsTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyAlertTestCase(GmpModifyAlertTestMixin, Gmpv208TestCase):
    pass


class Gmpv208TestAlertTestCase(GmpTestAlertTestMixin, Gmpv208TestCase):
    pass


class Gmpv208TriggerAlertTestCase(GmpTriggerAlertTestMixin, Gmpv208TestCase):
    pass
