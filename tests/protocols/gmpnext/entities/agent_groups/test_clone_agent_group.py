# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument


class GmpCloneAgentGroupTestMixin:
    def test_clone_agent_group(self):
        self.gmp.clone_agent_group(agent_group_id="group-1")

        self.connection.send.has_been_called_with(
            b"<create_agent_group><copy>group-1</copy></create_agent_group>"
        )

    def test_clone_agent_group_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_agent_group(agent_group_id=None)
