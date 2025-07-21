# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument


class GmpDeleteAgentGroupTestMixin:
    def test_delete_agent_group_soft(self):
        self.gmp.delete_agent_group(agent_group_id="group-1", ultimate=False)

        self.connection.send.has_been_called_with(
            b'<delete_agent_group agent_group_id="group-1" ultimate="0"/>'
        )

    def test_delete_agent_group_hard(self):
        self.gmp.delete_agent_group(agent_group_id="group-1", ultimate=True)

        self.connection.send.has_been_called_with(
            b'<delete_agent_group agent_group_id="group-1" ultimate="1"/>'
        )

    def test_delete_agent_group_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.delete_agent_group(agent_group_id=None)
