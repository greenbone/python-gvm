# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.errors import RequiredArgument


class GmpModifyAgentControllerScanConfigTestMixin:
    def test_modify_agent_control_scan_config_full(self):
        config = {
            "agent_defaults": {
                "agent_control": {
                    "retry": {
                        "attempts": 6,
                        "delay_in_seconds": 60,
                        "max_jitter_in_seconds": 10,
                    }
                },
                "agent_script_executor": {
                    "bulk_size": 1,
                    "bulk_throttle_time_in_ms": 100,
                    "indexer_dir_depth": 10,
                    "scheduler_cron_time": [
                        "0 23 * * *",
                        "0 22 * * *",
                    ],
                },
                "heartbeat": {
                    "interval_in_seconds": 600,
                    "miss_until_inactive": 1,
                },
            },
            "agent_control_defaults": {
                "update_to_latest": True,
            },
        }

        self.gmp.modify_agent_control_scan_config(
            "3b4be213-281f-49ee-b457-5a5f34f71510",
            config=config,
        )

        self.connection.send.has_been_called_with(
            b'<modify_agent_control_scan_config agent_control_id="3b4be213-281f-49ee-b457-5a5f34f71510">'
            b"<config_defaults>"
            b"<agent_defaults>"
            b"<agent_control>"
            b"<retry>"
            b"<attempts>6</attempts>"
            b"<delay_in_seconds>60</delay_in_seconds>"
            b"<max_jitter_in_seconds>10</max_jitter_in_seconds>"
            b"</retry>"
            b"</agent_control>"
            b"<agent_script_executor>"
            b"<bulk_size>1</bulk_size>"
            b"<bulk_throttle_time_in_ms>100</bulk_throttle_time_in_ms>"
            b"<indexer_dir_depth>10</indexer_dir_depth>"
            b'<scheduler_cron_time is_list="1">'
            b"<item>0 23 * * *</item>"
            b"<item>0 22 * * *</item>"
            b"</scheduler_cron_time>"
            b"</agent_script_executor>"
            b"<heartbeat>"
            b"<interval_in_seconds>600</interval_in_seconds>"
            b"<miss_until_inactive>1</miss_until_inactive>"
            b"</heartbeat>"
            b"</agent_defaults>"
            b"<agent_control_defaults>"
            b"<update_to_latest>1</update_to_latest>"
            b"</agent_control_defaults>"
            b"</config_defaults>"
            b"</modify_agent_control_scan_config>"
        )

    def test_modify_agent_control_scan_config_with_missing_element_raises(self):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                    "heartbeat": {
                        "interval_in_seconds": 300,
                        "miss_until_inactive": 1,
                    },
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
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
                    "config_defaults": {
                        "agent_defaults": {
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
                        "agent_control_defaults": {
                            "update_to_latest": True,
                        },
                    }
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
            "config_defaults": {
                "agent_defaults": {
                    "agent_control": "oops-not-a-mapping",
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
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_scheduler_empty_list_raises(self):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                    "heartbeat": {
                        "interval_in_seconds": 300,
                        "miss_until_inactive": 1,
                    },
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_scheduler_with_empty_item_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                    "heartbeat": {
                        "interval_in_seconds": 300,
                        "miss_until_inactive": 1,
                    },
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_agent_control_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
                    # "agent_control": missing
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
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_retry_block_raises(self):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
                    "agent_control": {
                        # "retry": {}
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
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_retry_attempts_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                    "heartbeat": {
                        "interval_in_seconds": 300,
                        "miss_until_inactive": 1,
                    },
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_retry_delay_raises(self):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                    "heartbeat": {
                        "interval_in_seconds": 300,
                        "miss_until_inactive": 1,
                    },
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_retry_max_jitter_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                    "heartbeat": {
                        "interval_in_seconds": 300,
                        "miss_until_inactive": 1,
                    },
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_agent_script_executor_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
                    "agent_control": {
                        "retry": {
                            "attempts": 6,
                            "delay_in_seconds": 60,
                            "max_jitter_in_seconds": 10,
                        }
                    },
                    # "agent_script_executor": missing,
                    "heartbeat": {
                        "interval_in_seconds": 300,
                        "miss_until_inactive": 1,
                    },
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_bulk_size_raises(self):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                    "heartbeat": {
                        "interval_in_seconds": 300,
                        "miss_until_inactive": 1,
                    },
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_bulk_throttle_time_in_ms_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                    "heartbeat": {
                        "interval_in_seconds": 300,
                        "miss_until_inactive": 1,
                    },
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_indexer_dir_depth_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                    "heartbeat": {
                        "interval_in_seconds": 300,
                        "miss_until_inactive": 1,
                    },
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_heartbeat_block_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                    # "heartbeat": missing,
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_heartbeat_interval_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_heartbeat_miss_until_inactive_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                },
                "agent_control_defaults": {
                    "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_agent_control_defaults_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                # "agent_control_defaults": missing,
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )

    def test_modify_agent_control_scan_config_missing_update_to_latest_raises(
        self,
    ):
        cfg = {
            "config_defaults": {
                "agent_defaults": {
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
                "agent_control_defaults": {
                    # "update_to_latest": True,
                },
            }
        }
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_agent_control_scan_config(
                "fb6451bf-ec5a-45a8-8bab-5cf4b862e51b", config=cfg
            )
