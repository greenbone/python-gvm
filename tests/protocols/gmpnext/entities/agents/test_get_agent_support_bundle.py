# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument


class GmpGetAgentSupportBundleTestMixin:
    def test_get_agent_support_bundle(self):
        self.gmp.get_agent_support_bundle(
            agent_id="agent-123",
            days=7,
        )

        self.connection.send.has_been_called_with(
            b'<get_agent_support_bundle agent_uuid="agent-123" days="7"/>'
        )

    def test_get_agent_support_bundle_without_days_uses_zero(self):
        self.gmp.get_agent_support_bundle(
            agent_id="agent-123",
        )

        self.connection.send.has_been_called_with(
            b'<get_agent_support_bundle agent_uuid="agent-123" days="0"/>'
        )

    def test_get_agent_support_bundle_with_none_days_uses_zero(self):
        self.gmp.get_agent_support_bundle(
            agent_id="agent-123",
            days=None,
        )

        self.connection.send.has_been_called_with(
            b'<get_agent_support_bundle agent_uuid="agent-123" days="0"/>'
        )

    def test_get_agent_support_bundle_with_zero_days(self):
        self.gmp.get_agent_support_bundle(
            agent_id="agent-123",
            days=0,
        )

        self.connection.send.has_been_called_with(
            b'<get_agent_support_bundle agent_uuid="agent-123" days="0"/>'
        )

    def test_get_agent_support_bundle_without_agent_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_support_bundle(
                agent_id=None,
                days=7,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.get_agent_support_bundle(
                agent_id="",
                days=7,
            )

    def test_get_agent_support_bundle_with_negative_days(self):
        with self.assertRaises(ValueError):
            self.gmp.get_agent_support_bundle(
                agent_id="agent-123",
                days=-1,
            )
