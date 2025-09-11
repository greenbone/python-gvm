# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .agents.test_delete_agents import (
    GmpDeleteAgentsTestMixin,
)
from .agents.test_get_agents import (
    GmpGetAgentsTestMixin,
)
from .agents.test_modify_agent_controller_scan_config import (
    GmpModifyAgentControllerScanConfigTestMixin,
)
from .agents.test_modify_agents import (
    GmpModifyAgentsTestMixin,
)


class GMPGetAgentsTestCase(GmpGetAgentsTestMixin, GMPTestCase):
    pass


class GMPModifyAgentsTestCase(GmpModifyAgentsTestMixin, GMPTestCase):
    pass


class GMPDeleteAgentsTestCase(GmpDeleteAgentsTestMixin, GMPTestCase):
    pass


class GMPModifyAgentControllerScanConfigTestCase(
    GmpModifyAgentControllerScanConfigTestMixin, GMPTestCase
):
    pass
