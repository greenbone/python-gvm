# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument


class GmpModifyAgentControllerScanConfigTestMixin:
    def test_modify_agent_control_scan_config_full(self):
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

        self.gmp.modify_agent_control_scan_config(
            "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b",
            config=cfg,
        )

        self.connection.send.has_been_called_with(
            b'<modify_agent_control_scan_config agent_control_id="fb6451bf-ec5a-45a8-8bab-5cf4b862e51b">'
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
            b"</modify_agent_control_scan_config>"
        )

    def test_modify_agent_control_scan_config_with_missing_element_raises(self):
        cfg = {
            "agent_control": {
                "retry": {
                    "attempts": 6,
                    "delay_in_seconds": 60,
                    # max_jitter_in_seconds is missing
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b",
                config=cfg,
            )

    def test_modify_agent_control_scan_config_missing_id_raises(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "",  # missing id
                config={
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
                        "miss_until_inactive": 1,
                    },
                },
            )

    def test_modify_agent_control_scan_config_missing_config_raises(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b",
                config=None,  # missing config
            )

    def test_modify_agent_control_scan_config_config_not_mapping_raises(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=123
            )

    def test_modify_agent_control_scan_config_agent_control_not_mapping_raises(
        self,
    ):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_scheduler_empty_list_raises(self):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_scheduler_with_empty_item_raises(
        self,
    ):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_agent_control_raises(
        self,
    ):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_retry_block_raises(self):
        cfg = {
            "agent_control": {
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_retry_attempts_raises(
        self,
    ):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_retry_delay_raises(self):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_retry_max_jitter_raises(
        self,
    ):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_agent_script_executor_raises(
        self,
    ):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_bulk_size_raises(self):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_bulk_throttle_time_in_ms_raises(
        self,
    ):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_indexer_dir_depth_raises(
        self,
    ):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_heartbeat_block_raises(
        self,
    ):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_heartbeat_interval_raises(
        self,
    ):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_heartbeat_miss_until_inactive_raises(
        self,
    ):
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
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )
