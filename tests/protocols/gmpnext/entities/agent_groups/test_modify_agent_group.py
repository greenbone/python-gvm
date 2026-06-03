# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument


class GmpModifyAgentGroupTestMixin:
    def test_modify_agent_group(self):
        self.gmp.modify_agent_group(
            agent_group_id="group-1",
            name="NewName",
            comment="Updated comment",
            scheduler_cron_time="0 */5 * * *",
            agent_ids=["agent-1", "agent-2"],
        )

        self.connection.send.has_been_called_with(
            b'<modify_agent_group agent_group_id="group-1">'
            b"<scheduler_cron_time>0 */5 * * *</scheduler_cron_time>"
            b"<name>NewName</name>"
            b"<comment>Updated comment</comment>"
            b'<agents><agent id="agent-1"/><agent id="agent-2"/></agents>'
            b"</modify_agent_group>"
        )

    def test_modify_agent_group_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_group(
                agent_group_id=None, scheduler_cron_time="0 */5 * * *"
            )

    def test_modify_agent_group_without_scheduler_cron_time(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_group(
                agent_group_id="group-1", scheduler_cron_time=None
            )

    def test_modify_agent_group_without_name(self):
        self.gmp.modify_agent_group(
            agent_group_id="group-1",
            comment="Updated comment",
            scheduler_cron_time="0 */5 * * *",
            agent_ids=["agent-1", "agent-2"],
        )

        self.connection.send.has_been_called_with(
            b'<modify_agent_group agent_group_id="group-1">'
            b"<scheduler_cron_time>0 */5 * * *</scheduler_cron_time>"
            b"<comment>Updated comment</comment>"
            b'<agents><agent id="agent-1"/><agent id="agent-2"/></agents>'
            b"</modify_agent_group>"
        )

    def test_modify_agent_group_without_comment(self):
        self.gmp.modify_agent_group(
            agent_group_id="group-1",
            name="NewName",
            scheduler_cron_time="0 */5 * * *",
            agent_ids=["agent-1", "agent-2"],
        )

        self.connection.send.has_been_called_with(
            b'<modify_agent_group agent_group_id="group-1">'
            b"<scheduler_cron_time>0 */5 * * *</scheduler_cron_time>"
            b"<name>NewName</name>"
            b'<agents><agent id="agent-1"/><agent id="agent-2"/></agents>'
            b"</modify_agent_group>"
        )

    def test_modify_agent_group_without_agent_ids(self):
        self.gmp.modify_agent_group(
            agent_group_id="group-1",
            name="NewName",
            comment="Updated comment",
            scheduler_cron_time="0 */5 * * *",
        )

        self.connection.send.has_been_called_with(
            b'<modify_agent_group agent_group_id="group-1">'
            b"<scheduler_cron_time>0 */5 * * *</scheduler_cron_time>"
            b"<name>NewName</name>"
            b"<comment>Updated comment</comment>"
            b"</modify_agent_group>"
        )
