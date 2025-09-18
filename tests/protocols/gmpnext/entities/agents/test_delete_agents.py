# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument


class GmpDeleteAgentsTestMixin:
    def test_delete_agents(self):
        self.gmp.delete_agents(agent_ids=["agent-123", "agent-456"])

        self.connection.send.has_been_called_with(
            b"<delete_agent>"
            b'<agents><agent id="agent-123"/><agent id="agent-456"/></agents>'
            b"</delete_agent>"
        )

    def test_delete_agents_without_ids(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.delete_agents(agent_ids=[])
