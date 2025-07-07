# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv228 import GMPTestCase
from .agent_installers.test_get_agent_installer import (
    GmpGetAgentInstallerTestMixin,
)
from .agent_installers.test_get_agent_installer_file import (
    GmpGetAgentInstallerFileTestMixin,
)
from .agent_installers.test_get_agent_installers import (
    GmpGetAgentInstallersTestMixin,
)


class GMPGetAgentInstallerTestCase(GmpGetAgentInstallerTestMixin, GMPTestCase):
    pass


class GMPGetAgentInstallerFileTestCase(
    GmpGetAgentInstallerFileTestMixin, GMPTestCase
):
    pass


class GMPGetAgentInstallersTestCase(
    GmpGetAgentInstallersTestMixin, GMPTestCase
):
    pass
