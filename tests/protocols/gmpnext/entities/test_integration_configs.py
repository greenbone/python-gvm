# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .integration_configs.test_get_integration_config import (
    GmpGetIntegrationConfigTestMixin,
)
from .integration_configs.test_get_integration_configs import (
    GmpGetIntegrationConfigsTestMixin,
)
from .integration_configs.test_modify_integration_config import (
    GmpModifyIntegrationConfigTestMixin,
)


class GmpGetIntegrationConfigTestCase(
    GmpGetIntegrationConfigTestMixin, GMPTestCase
):
    pass


class GmpGetIntegrationConfigsTestCase(
    GmpGetIntegrationConfigsTestMixin, GMPTestCase
):
    pass


class GmpModifyIntegrationConfigTestCase(
    GmpModifyIntegrationConfigTestMixin, GMPTestCase
):
    pass
