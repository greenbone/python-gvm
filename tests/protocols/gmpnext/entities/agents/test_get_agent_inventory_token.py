# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later


class GmpGetAgentInventoryTokenTestMixin:
    def test_get_agent_inventory_token(self):
        self.gmp.get_agent_inventory_token()

        self.connection.send.has_been_called_with(
            b"<get_agent_inventory_token/>"
        )
