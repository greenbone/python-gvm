#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetIntegrationConfigTestMixin:
    def test_get_integration_config(self):
        self.gmp.get_integration_config("uuid")

        self.connection.send.has_been_called_with(
            b'<get_integration_configs integration_config_id="uuid"/>'
        )
        self.gmp.get_integration_config(integration_config_id="uuid")

        self.connection.send.has_been_called_with(
            b'<get_integration_configs integration_config_id="uuid"/>'
        )

    def test_get_integration_config_without_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_integration_config(integration_config_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_integration_config("")

    def test_get_integration_config_with_details(self):
        self.gmp.get_integration_config(
            integration_config_id="uuid", details=True
        )

        self.connection.send.has_been_called_with(
            b'<get_integration_configs integration_config_id="uuid" details="1"/>'
        )

        self.gmp.get_integration_config(
            integration_config_id="uuid", details=False
        )

        self.connection.send.has_been_called_with(
            b'<get_integration_configs integration_config_id="uuid" details="0"/>'
        )
