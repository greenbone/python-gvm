# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later


class GmpGetAgentGroupsTestMixin:
    def test_get_agent_groups(self):
        self.gmp.get_agent_groups()

        self.connection.send.has_been_called_with(b"<get_agent_groups/>")

    def test_get_agent_groups_with_filter_string(self):
        self.gmp.get_agent_groups(filter_string="name=group")

        self.connection.send.has_been_called_with(
            b'<get_agent_groups filter="name=group"/>'
        )

    def test_get_agent_groups_with_filter_id(self):
        self.gmp.get_agent_groups(filter_id="filter-1")

        self.connection.send.has_been_called_with(
            b'<get_agent_groups filt_id="filter-1"/>'
        )

    def test_get_agent_groups_with_trash(self):
        self.gmp.get_agent_groups(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_agent_groups trash="1"/>'
        )

    def test_get_agent_groups_with_trash_false(self):
        self.gmp.get_agent_groups(trash=False)

        self.connection.send.has_been_called_with(
            b'<get_agent_groups trash="0"/>'
        )

    def test_get_agent_groups_without_trash(self):
        self.gmp.get_agent_groups()

        self.connection.send.has_been_called_with(b"<get_agent_groups/>")
