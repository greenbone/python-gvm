# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later


class GmpGetAgentsTestMixin:
    def test_get_agents(self):
        self.gmp.get_agents()

        self.connection.send.has_been_called_with(b"<get_agents/>")

    def test_get_agents_with_filter_string(self):
        self.gmp.get_agents(filter_string="name=agent")

        self.connection.send.has_been_called_with(
            b'<get_agents filter="name=agent"/>'
        )

    def test_get_agents_with_filter_id(self):
        self.gmp.get_agents(filter_id="f1")

        self.connection.send.has_been_called_with(b'<get_agents filt_id="f1"/>')

    def test_get_agents_with_details_true(self):
        self.gmp.get_agents(details=True)

        self.connection.send.has_been_called_with(b'<get_agents details="1"/>')

    def test_get_agents_with_details_false(self):
        self.gmp.get_agents(details=False)

        self.connection.send.has_been_called_with(b'<get_agents details="0"/>')
