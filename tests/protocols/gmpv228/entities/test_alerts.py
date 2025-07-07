# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
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
from ...gmpv227 import GMPTestCase


class GMPCloneAlertTestCase(GmpCloneAlertTestMixin, GMPTestCase):
    pass


class GMPCreateAlertTestCase(GmpCreateAlertTestMixin, GMPTestCase):
    pass


class GMPDeleteAlertTestCase(GmpDeleteAlertTestMixin, GMPTestCase):
    pass


class GMPGetAlertTestCase(GmpGetAlertTestMixin, GMPTestCase):
    pass


class GMPGetAlertsTestCase(GmpGetAlertsTestMixin, GMPTestCase):
    pass


class GMPModifyAlertTestCase(GmpModifyAlertTestMixin, GMPTestCase):
    pass


class GMPTestAlertTestCase(GmpTestAlertTestMixin, GMPTestCase):
    pass


class GMPTriggerAlertTestCase(GmpTriggerAlertTestMixin, GMPTestCase):
    pass
