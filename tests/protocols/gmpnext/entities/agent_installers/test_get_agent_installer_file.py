# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetAgentInstallerFileTestMixin:

    def test_get_agent_installer(self):
        self.gmp.get_agent_installer_file(agent_installer_id="installer1")

        self.connection.send.has_been_called_with(
            b'<get_agent_installer_file agent_installer_id="installer1"/>'
        )

    def test_get_agent_installer_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_file(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_installer_file("")
