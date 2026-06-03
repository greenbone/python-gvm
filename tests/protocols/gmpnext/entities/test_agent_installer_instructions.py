# SPDX-FileCopyrightText: 2023-2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .agent_installer_instructions.test_get_aget_installer_instruction import (
    GmpGetAgentInstallerInstructionTestMixin,
)


class GMPGetAgentInstallerInstructionTestCase(
    GmpGetAgentInstallerInstructionTestMixin, GMPTestCase
):
    pass
