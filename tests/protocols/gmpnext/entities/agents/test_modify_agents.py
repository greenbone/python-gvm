# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument


class GmpModifyAgentsTestMixin:
    def test_modify_agents_basic(self):
        self.gmp.modify_agents(agent_ids=["agent-123"])

        self.connection.send.has_been_called_with(
            b"<modify_agent>"
            b'<agents><agent id="agent-123"/></agents>'
            b"</modify_agent>"
        )

    def test_modify_agents_with_authorized_only(self):
        self.gmp.modify_agents(
            agent_ids=["agent-123", "agent-456"], authorized=True
        )

        self.connection.send.has_been_called_with(
            b"<modify_agent>"
            b'<agents><agent id="agent-123"/><agent id="agent-456"/></agents>'
            b"<authorized>1</authorized>"
            b"</modify_agent>"
        )

    def test_modify_agents_with_update_to_latest_only(self):
        self.gmp.modify_agents(
            agent_ids=["agent-123", "agent-456"], update_to_latest=True
        )

        self.connection.send.has_been_called_with(
            b"<modify_agent>"
            b'<agents><agent id="agent-123"/><agent id="agent-456"/></agents>'
            b"<update_to_latest>1</update_to_latest>"
            b"</modify_agent>"
        )

    def test_modify_agents_with_full_config_and_comment(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }

        self.gmp.modify_agents(
            agent_ids=["agent-123", "agent-456"],
            authorized=True,
            update_to_latest=True,
            config=cfg,
            comment="Updated agents",
        )

        self.connection.send.has_been_called_with(
            b"<modify_agent>"
            b'<agents><agent id="agent-123"/><agent id="agent-456"/></agents>'
            b"<authorized>1</authorized>"
            b"<update_to_latest>1</update_to_latest>"
            b"<config>"
            b"<agent_control>"
            b"<retry>"
            b"<attempts>6</attempts>"
            b"<delay_in_seconds>60</delay_in_seconds>"
            b"<max_jitter_in_seconds>10</max_jitter_in_seconds>"
            b"</retry>"
            b"</agent_control>"
            b"<agent_script_executor>"
            b"<bulk_size>2</bulk_size>"
            b"<bulk_throttle_time_in_ms>300</bulk_throttle_time_in_ms>"
            b"<indexer_dir_depth>100</indexer_dir_depth>"
            b"<scheduler_cron_time>"
            b"<item>0 */12 * * *</item>"
            b"</scheduler_cron_time>"
            b"</agent_script_executor>"
            b"<heartbeat>"
            b"<interval_in_seconds>300</interval_in_seconds>"
            b"<miss_until_inactive>1</miss_until_inactive>"
            b"</heartbeat>"
            b"</config>"
            b"<comment>Updated agents</comment>"
            b"</modify_agent>"
        )

    def test_modify_agents_with_full_config_with_missing_element(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                # scheduler_cron_time is missing
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(
                agent_ids=["agent-123", "agent-456"],
                authorized=True,
                config=cfg,
                comment="Updated agents",
            )

    def test_modify_agents_without_ids_raises(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=[])

    def test_modify_agents_scheduler_empty_list_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": [],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_scheduler_with_empty_item_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["", "   "],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_agent_control_raises(self):
        cfg = {
            # "agent_control": missing
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_retry_block_raises(self):
        cfg = {
            "agent_control": {  # retry missing
                # "retry": {}
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_retry_attempts_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    # "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_retry_delay_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    # "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_retry_max_jitter_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    # "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_agent_script_executor_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            # "agent_script_executor": missing
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_bulk_size_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                # "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_bulk_throttle_time_in_ms_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                # "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_indexer_dir_depth_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                # "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_heartbeat_block_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            # "heartbeat": missing
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_heartbeat_interval_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {
                # "interval_in_seconds": 300,
                "miss_until_inactive": 1,
            },
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_missing_heartbeat_miss_until_inactive_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    "max_jitter_in_seconds": 10,
                }
            },
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {
                "interval_in_seconds": 300,
                # "miss_until_inactive": 1,
            },
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)

    def test_modify_agents_config_not_mapping_raises(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(
                agent_ids=["agent-123"], config="not-a-mapping"
            )

    def test_modify_agents_agent_control_not_mapping_raises(self):
        cfg = {
            "agent_control": "oops-not-a-mapping",
            "agent_script_executor": {
                "bulk_size": 2,
                "bulk_throttle_time_in_ms": 300,
                "indexer_dir_depth": 100,
                "scheduler_cron_time": ["0 */12 * * *"],
            },
            "heartbeat": {"interval_in_seconds": 300, "miss_until_inactive": 1},
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agents(agent_ids=["agent-123"], config=cfg)
