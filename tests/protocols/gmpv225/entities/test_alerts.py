# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.alerts import (
    GmpCloneAlertTestMixin,
    GmpCreateAlertTestMixin,
    GmpDeleteAlertTestMixin,
    GmpGetAlertsTestMixin,
    GmpGetAlertTestMixin,
    GmpModifyAlertTestMixin,
    GmpTestAlertTestMixin,
    GmpTriggerAlertTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225CloneAlertTestCase(GmpCloneAlertTestMixin, GMPTestCase):
    pass


class Gmpv225CreateAlertTestCase(GmpCreateAlertTestMixin, GMPTestCase):
    pass


class Gmpv225DeleteAlertTestCase(GmpDeleteAlertTestMixin, GMPTestCase):
    pass


class Gmpv225GetAlertTestCase(GmpGetAlertTestMixin, GMPTestCase):
    pass


class Gmpv225GetAlertsTestCase(GmpGetAlertsTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyAlertTestCase(GmpModifyAlertTestMixin, GMPTestCase):
    pass


class Gmpv225TestAlertTestCase(GmpTestAlertTestMixin, GMPTestCase):
    pass


class Gmpv225TriggerAlertTestCase(GmpTriggerAlertTestMixin, GMPTestCase):
    pass
