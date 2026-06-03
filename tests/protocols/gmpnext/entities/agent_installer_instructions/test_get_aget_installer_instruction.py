# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.next import (
    AgentInstallerInstructionLanguageType,
)


class GmpGetAgentInstallerInstructionTestMixin:
    def test_get_agent_installer_instruction(self):
        self.gmp.get_agent_installer_instruction(
            scanner_id="scanner1",
            language_type=AgentInstallerInstructionLanguageType.EN,
        )

        self.connection.send.has_been_called_with(
            b'<get_agent_installer_instruction scanner_id="scanner1" language="en"/>'
        )

    def test_get_agent_installer_instruction_de(self):
        self.gmp.get_agent_installer_instruction(
            scanner_id="scanner1",
            language_type=AgentInstallerInstructionLanguageType.DE,
        )

        self.connection.send.has_been_called_with(
            b'<get_agent_installer_instruction scanner_id="scanner1" language="de"/>'
        )

    def test_get_agent_installer_instruction_without_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_instruction(
                scanner_id=None,
                language_type=AgentInstallerInstructionLanguageType.EN,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_instruction(
                scanner_id="",
                language_type=AgentInstallerInstructionLanguageType.EN,
            )

    def test_get_agent_installer_instruction_without_language_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_instruction(
                scanner_id="scanner1",
                language_type=None,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_instruction(
                scanner_id="scanner1",
                language_type="",
            )
