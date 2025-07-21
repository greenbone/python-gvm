# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument


class GmpModifyAgentsTestMixin:
    def test_modify_agents_basic(self):
        self.gmp.modify_agents(agent_ids=["agent-123"])

        self.connection.send.has_been_called_with(
            b"<modify_agents>"
            b'<agents><agent id="agent-123"/></agents>'
            b"</modify_agents>"
        )

    def test_modify_agents_with_all_fields(self):
        self.gmp.modify_agents(
            agent_ids=["agent-123", "agent-456"],
            authorized=True,
            min_interval=300,
            heartbeat_interval=600,
            schedule="@every 6h",
            comment="Updated agents",
        )

        self.connection.send.has_been_called_with(
            b"<modify_agents>"
            b'<agents><agent id="agent-123"/><agent id="agent-456"/></agents>'
            b"<authorized>1</authorized>"
            b"<min_interval>300</min_interval>"
            b"<heartbeat_interval>600</heartbeat_interval>"
            b"<schedule>@every 6h</schedule>"
            b"<comment>Updated agents</comment>"
            b"</modify_agents>"
        )

    def test_modify_agents_without_ids(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=[])
