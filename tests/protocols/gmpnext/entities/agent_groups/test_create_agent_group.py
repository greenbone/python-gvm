# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument


class GmpCreateAgentGroupTestMixin:
    def test_create_agent_group(self):
        self.gmp.create_agent_group(
            name="ExampleGroup",
            agent_ids=["agent-1", "agent-2"],
            comment="Sample comment",
        )

        self.connection.send.has_been_called_with(
            b"<create_agent_group>"
            b"<name>ExampleGroup</name>"
            b"<comment>Sample comment</comment>"
            b'<agents><agent id="agent-1"/><agent id="agent-2"/></agents>'
            b"</create_agent_group>"
        )

    def test_create_agent_group_without_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_agent_group(name="", agent_ids=["agent-1"])

    def test_create_agent_group_without_agents(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_agent_group(name="Group", agent_ids=[])

    def test_create_agent_group_without_comment(self):
        self.gmp.create_agent_group(name="GroupX", agent_ids=["a1", "a2"])

        self.connection.send.has_been_called_with(
            b"<create_agent_group>"
            b"<name>GroupX</name>"
            b'<agents><agent id="a1"/><agent id="a2"/></agents>'
            b"</create_agent_group>"
        )
