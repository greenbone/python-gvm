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
            origin_url="https://example.com",
        )

        self.connection.send.has_been_called_with(
            b"<get_agent_installer_instruction"
            b' scanner_id="scanner1"'
            b' language="en"'
            b' origin_url="https://example.com"/>'
        )

    def test_get_agent_installer_instruction_de(self):
        self.gmp.get_agent_installer_instruction(
            scanner_id="scanner1",
            language_type=AgentInstallerInstructionLanguageType.DE,
            origin_url="https://example.com",
        )

        self.connection.send.has_been_called_with(
            b"<get_agent_installer_instruction"
            b' scanner_id="scanner1"'
            b' language="de"'
            b' origin_url="https://example.com"/>'
        )

    def test_get_agent_installer_instruction_escapes_origin_url(self):
        self.gmp.get_agent_installer_instruction(
            scanner_id="scanner1",
            language_type=AgentInstallerInstructionLanguageType.EN,
            origin_url="https://example.com/path?foo=bar&value=test",
        )

        self.connection.send.has_been_called_with(
            b"<get_agent_installer_instruction"
            b' scanner_id="scanner1"'
            b' language="en"'
            b' origin_url="https://example.com/path?foo=bar&amp;value=test"/>'
        )

    def test_get_agent_installer_instruction_without_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_instruction(
                scanner_id=None,
                language_type=AgentInstallerInstructionLanguageType.EN,
                origin_url="https://example.com",
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_instruction(
                scanner_id="",
                language_type=AgentInstallerInstructionLanguageType.EN,
                origin_url="https://example.com",
            )

    def test_get_agent_installer_instruction_without_language_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_instruction(
                scanner_id="scanner1",
                language_type=None,
                origin_url="https://example.com",
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_instruction(
                scanner_id="scanner1",
                language_type="",
                origin_url="https://example.com",
            )

    def test_get_agent_installer_instruction_without_origin_url(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_instruction(
                scanner_id="scanner1",
                language_type=AgentInstallerInstructionLanguageType.EN,
                origin_url=None,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_instruction(
                scanner_id="scanner1",
                language_type=AgentInstallerInstructionLanguageType.EN,
                origin_url="",
            )
