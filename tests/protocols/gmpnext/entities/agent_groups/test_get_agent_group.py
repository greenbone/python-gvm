# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument


class GmpGetAgentGroupTestMixin:
    def test_get_agent_group(self):
        self.gmp.get_agent_group(agent_group_id="group-1")

        self.connection.send.has_been_called_with(
            b'<get_agent_groups agent_group_id="group-1"/>'
        )

    def test_get_agent_group_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_group(agent_group_id=None)
